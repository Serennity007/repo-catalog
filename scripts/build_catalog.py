#!/usr/bin/env python3
"""Refresh public repository evidence, or render/check a saved snapshot offline."""
import argparse
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
OWNER = 'Serennity007'
SNAPSHOT = ROOT / 'data/repositories.json'
CN_TIME = timezone(timedelta(hours=8))
STATES = {'content': '✅ 文件内容', 'docs': '📖 README 文档', 'placeholder': '🟡 占位', 'empty': '⚪ 空仓库'}
GROUPS = [
    ('markets', '股票 · 期货 · 量化', r'stock|quant|trading|invest|a-share|a-stock|ibkr|tushare|qlib|openbb|moneyprinter|daily_stock|uzi|bitsoul|futures|crude-oil|gold-research|ec-shipping'),
    ('reading', 'Obsidian · RSS · 精选阅读', r'obsidian|rss|picks|vault|sync|note|feishu-finance'),
    ('security', '安全 · 审计 · 逆向', r'xss|security|cyber|bug-bounty|ctf|forensic|exploit|hacking|malware|osint|pentest|reverse|vuln|ghosttrack'),
    ('research', '科研 · 论文 · 演示文稿', r'paper|research-figure|scientific-figure|beiligong|ppt|origin-figure|citation'),
    ('cli', '命令行与 npm 工具', r'^cli-|^git-|^ai-commit$|^vibe-check$|^agent-trace$|^token-meter$|-cli$|toml-validator|base64|calculator|color-picker|cron-parser|csv-parser|diff-viewer|hash-generator|http-client|json-|lorem|markdown-preview|password-gen|uuid|weather|file-converter|dim-light'),
    ('agents', 'AI 编码 · Agent · Skills', r'agent|skill|prompt|cursor|claude|copilot|llm|^ai-|awesome-ai|mcp-|npm-audit'),
    ('learning', '学习路线 · 速查表 · 备考', r'^learn-|cheatsheet|ielts|exam|guizhou|leetcode|roadmap|myielts|study|graduation'),
    ('infra', '后端 · 基础设施 · 数据', r'docker|kubernetes|devops|terraform|nginx|serverless|monitor|github-actions|data-pipeline|database|microservice|event-driven|api|system-design|postgres|redis|template'),
    ('frontend', '前端 · 设计 · 图形 · 视频', r'react|vue|svelte|nextjs|astro|tailwind|figma|canva|adobe|sketch|blender|godot|unity|unreal|threejs|shader|webgl|frontend|design|portfolio|resume|video|image|food-map|student-progress|blog|website'),
    ('languages', '语言与运行时生态', r'^awesome-(go|rust|python|typescript|deno|bun|functional|zig|java|dotnet|linux|macos|windows|terminal|vim|zsh|tmux|git-aliases|npm-packages)'),
    ('resources', '开发者资源索引', r'^awesome-'),
    ('other', '其他', r'.*'),
]
EXTRA_GROUPS = [('mirrors', '转载 · 镜像'), ('forks', 'Fork · 上游项目'), ('home', '个人主页 · 导航')]
EXPLICIT = {'serenity-stock-rss': 'reading', 'feishu-finance-digest': 'reading', 'paper-builder-system': 'frontend', 'chatgpt-plus-china-guide': 'resources'}


def api(path):
    """Never turn transport/auth/rate-limit failures into empty repository evidence."""
    for attempt in range(3):
        proc = subprocess.run(['gh', 'api', path], capture_output=True)
        if proc.returncode == 0:
            return json.loads(proc.stdout)
        if attempt < 2:
            time.sleep(attempt + 1)
    raise RuntimeError(f'GitHub request failed: {path}\n{proc.stderr.decode("utf-8", "replace")}')


def all_repos():
    out = []
    page = 1
    while True:
        batch = api(f'users/{OWNER}/repos?type=owner&per_page=100&page={page}')
        if not isinstance(batch, list):
            raise ValueError('Expected a repository list')
        out.extend(r for r in batch if not r.get('private') and r.get('visibility', 'public') == 'public')
        if len(batch) < 100:
            break
        page += 1
    if not out:
        raise ValueError('Refusing to replace the catalog with an empty API result')
    if len({r['name'] for r in out}) != len(out):
        raise ValueError('Duplicate repositories across API pages; retry the refresh')
    return out


def meaningful_readme(text):
    body = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    body = re.split(r'^#{1,2}\s+(?:license|许可证)\b', body, flags=re.I | re.M)[0]
    body = re.sub(r'^\s*#+[^\n]*', '', body, flags=re.M)
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    return len(body.strip()) >= 400 and len(lines) >= 5


def inspect_tree(tree, readme=''):
    if tree.get('truncated'):
        raise ValueError('Truncated Git tree; refusing an incomplete classification')
    if 'tree' not in tree or 'sha' not in tree:
        raise ValueError('Missing Git tree evidence')
    paths = sorted(t['path'] for t in tree['tree'] if t['type'] == 'blob')
    boiler = {'license', 'license.md', 'license.txt', 'copying', '.gitignore', '.gitattributes', 'changelog.md', 'contributing.md', 'code_of_conduct.md', '.banner.svg'}
    real = [p for p in paths if not p.startswith('.github/') and Path(p).name.lower() not in boiler and not (('/' not in p) and p.lower().startswith('readme'))]
    state = 'content' if real else ('docs' if meaningful_readme(readme) else ('placeholder' if paths else 'empty'))
    return {'state': state, 'files': len(paths), 'tree_sha': tree['sha'], 'evidence': real[:5], 'readme_path': next((p for p in paths if p.lower() == 'readme.md'), None)}


def group_for(repo):
    name = repo['name']
    desc = (repo.get('description') or '').lower()
    if repo['fork']:
        return 'forks'
    if name.startswith('mirror-') or desc.startswith('unofficial mirror') or 'for personal learning; all credit' in desc:
        return 'mirrors'
    if name in (OWNER, 'repo-catalog'):
        return 'home'
    if name in EXPLICIT:
        return EXPLICIT[name]
    for key, _, pattern in GROUPS:
        if re.search(pattern, name.lower()):
            return key
    raise AssertionError(name)


def refresh():
    def one(repo):
        name = repo['name']
        base = f'repos/{OWNER}/{name}'
        # GitHub size is not reliable evidence of an empty repository.
        # Only an explicit API empty-repository response counts as empty.
        proc = subprocess.run(['gh', 'api', f'{base}/git/trees/{quote(repo["default_branch"], safe="")}?recursive=1'], capture_output=True)
        if proc.returncode and b'Git Repository is empty' in proc.stdout:
            inspection = {'state': 'empty', 'files': 0, 'tree_sha': None, 'evidence': [], 'readme_path': None}
        else:
            tree = json.loads(proc.stdout) if proc.returncode == 0 else api(f'{base}/git/trees/{quote(repo["default_branch"], safe="")}?recursive=1')
            inspection = inspect_tree(tree)
            if inspection['state'] == 'placeholder' and inspection['readme_path']:
                blob = next(t for t in tree['tree'] if t['path'] == inspection['readme_path'])
                data = api(f'{base}/git/blobs/{blob["sha"]}')
                readme = base64.b64decode(data['content']).decode('utf-8', 'replace')
                inspection = inspect_tree(tree, readme)
        return {'name': name, 'url': repo['html_url'], 'description': repo.get('description') or '', 'private': False, 'fork': repo['fork'], 'archived': repo['archived'], 'default_branch': repo['default_branch'], 'pushed_at': repo['pushed_at'], 'stars': repo['stargazers_count'], 'language': repo.get('language'), 'inspection': inspection}
    with ThreadPoolExecutor(max_workers=8) as pool:
        repos = list(pool.map(one, all_repos()))
    return {'schema_version': 1, 'owner': OWNER, 'checked_on': datetime.now(CN_TIME).date().isoformat(), 'repositories': sorted(repos, key=lambda r: r['name'].lower())}


def validate(snapshot):
    if snapshot['schema_version'] != 1 or snapshot['owner'] != OWNER:
        raise ValueError('Unexpected snapshot schema or owner')
    names = set()
    if not snapshot['repositories']:
        raise ValueError('Empty snapshot')
    for repo in snapshot['repositories']:
        name = repo['name']
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or name in names:
            raise ValueError(f'Invalid or duplicate repository: {name}')
        names.add(name)
        if repo.get('private') is not False or repo['url'] != f'https://github.com/{OWNER}/{name}':
            raise ValueError(f'Non-public or unexpected repository: {name}')
        if repo['inspection']['state'] not in STATES:
            raise ValueError(f'Unknown content state: {name}')
    return snapshot


def cell(text):
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\r', ' ').replace('\n', ' ')


def render(snapshot):
    validate(snapshot)
    from featured_projects import load, guide, table, priority
    projects = load(snapshot)
    focus_names = {p['name'] for p in projects['projects']}
    repos = snapshot['repositories']
    date = snapshot['checked_on']
    counts = Counter(r['inspection']['state'] for r in repos)
    featured = json.loads((ROOT / 'data/featured.json').read_text(encoding='utf-8'))
    by_name = {r['name']: r for r in repos}
    outputs = {'docs/projects.md': guide(projects, snapshot)}
    for english, filename in ((True, 'README.md'), (False, 'README.zh-CN.md')):
        lines = ['[English](README.md) · [简体中文](README.zh-CN.md)', '', '# Serennity007 · Repository Navigator' if english else '# Serennity007 · 开源项目导航', '',
                 'Find a tool by task, then browse the complete public repository index.' if english else '按用途找工具，查看重点项目与全部公开仓库。', '',
                 f'[Profile](https://github.com/{OWNER}) · [Portfolio](https://serennity007.github.io/Serennity007-portfolio/) · [Full index / 全量索引](docs/catalog.md) · [Maintenance / 维护说明](docs/maintenance.md)', '',
                 f'> Checked: **{date} (Asia/Shanghai)** · **{len(repos)} public repositories** · {counts["content"]} with files · {counts["docs"]} README guides · {counts["placeholder"]} placeholders · {counts["empty"]} empty.' if english else f'> 核对日期：**{date}（北京时间）** · **{len(repos)} 个公开仓库** · {counts["content"]} 个含文件内容 · {counts["docs"]} 个 README 文档库 · {counts["placeholder"]} 个占位 · {counts["empty"]} 个空仓库。', '',
                 '## Start with a task' if english else '## 按用途直达', '',
                 '| Task | Project | Entry |' if english else '| 用途 | 项目 | 入口 |', '| --- | --- | --- |']
        position = lines.index('## Start with a task' if english else '## 按用途直达')
        lines[position:position] = ['## Six focus projects' if english else '## 六个重点项目', '', table(projects, 'en' if english else 'zh'), '', '[Inputs, outputs and first runs / 输入、输出与首次运行](docs/projects.md) · [Maintenance priorities / 维护分级](docs/lifecycle.md)', '']
        for item in featured:
            name = item['name']
            if name not in by_name or by_name[name]['inspection']['state'] in ('placeholder', 'empty'):
                continue
            lang = 'en' if english else 'zh'
            lines.append(f'| {cell(item[lang])} | [{name}]({by_name[name]["url"]}) | [{cell(item["entry_label"])}]({item["entry"]}) |')
        lines += ['', '## Browse by topic' if english else '## 按主题浏览', '', '| Topic / 主题 | Repositories / 仓库 | Content / 有内容 |', '| --- | ---: | ---: |']
        for key, label in [(k, label) for k, label, _ in GROUPS] + EXTRA_GROUPS:
            items = [r for r in repos if group_for(r) == key]
            if items:
                useful = sum(r['inspection']['state'] in ('content', 'docs') for r in items)
                lines.append(f'| [{label}](docs/catalog.md#{key}) | {len(items)} | {useful} |')
        lines += ['', '## Recently updated' if english else '## 最近更新', '', '| Project / 项目 | Pushed / 推送日期（北京时间） |', '| --- | --- |']
        recent = [r for r in repos if group_for(r) not in ('forks', 'mirrors', 'home') and r['inspection']['state'] in ('content', 'docs')]
        for repo in sorted(recent, key=lambda r: r['pushed_at'], reverse=True)[:8]:
            pushed = datetime.fromisoformat(repo['pushed_at'].replace('Z', '+00:00')).astimezone(CN_TIME).date()
            lines.append(f'| [{repo["name"]}]({repo["url"]}) | {pushed} |')
        lines += ['', '## Update and verify' if english else '## 更新与校验', '', '```bash', 'python scripts/build_catalog.py             # GitHub API → snapshot + navigation', 'python scripts/build_catalog.py --offline --check', 'python -m unittest discover -s tests -v', '```', '',
                  'Python 3.11+ and authenticated GitHub CLI (`gh auth login`) are needed for a refresh; offline rendering and tests use only the Python standard library. [Refresh workflow template and classification rules](docs/maintenance.md).' if english else '在线更新需要 Python 3.11+ 和已登录的 GitHub CLI（`gh auth login`）；离线生成和测试只用 Python 标准库。[更新工作流模板与分类规则](docs/maintenance.md)。', '',
                  'Content labels describe file evidence, not software quality, test coverage or an endorsement. Forks and declared mirrors are listed separately. Only public repository metadata is collected.' if english else '内容状态只描述文件证据，不代表质量、测试通过或推荐评级。Fork 与自述转载单列；数据只采集公开仓库元信息。', '']
        outputs[filename] = '\n'.join(lines)
    lines = ['# 全量公开仓库索引', '', '[导航首页](../README.zh-CN.md) · [English](../README.md) · [分类规则与维护](maintenance.md) · [维护优先级](lifecycle.md)', '', f'核对日期：{date}（北京时间）。共 {len(repos)} 个公开仓库；在页面内搜索仓库名即可定位。', '', '✅ 含文件内容 · 📖 README 文档库 · 🟡 占位 · ⚪ 空仓库；🔗 Fork · 🪞 自述转载。文件数不代表功能已验证。', '']
    for key, label in [(k, label) for k, label, _ in GROUPS] + EXTRA_GROUPS:
        items = [r for r in repos if group_for(r) == key]
        if not items:
            continue
        lines += [f'<a id="{key}"></a>', '', f'## {label}', '', f'{len(items)} 个仓库。', '', '| 仓库 | 内容状态 | 维护优先级 | 说明 |', '| --- | --- | --- | --- |']
        for repo in sorted(items, key=lambda r: (r['inspection']['state'] in ('placeholder', 'empty'), r['name'].lower())):
            state = STATES[repo['inspection']['state']]
            state += ' · 🔗' if repo['fork'] else (' · 🪞' if key == 'mirrors' else '')
            state += ' · 已归档' if repo['archived'] else ''
            desc = cell(repo['description'][:180] or '—')
            lines.append(f'| [{repo["name"]}]({repo["url"]}) | {state} | {priority(repo, focus_names)} | {desc} |')
        lines += ['']
    outputs['docs/catalog.md'] = '\n'.join(lines)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true', help='Render the committed public snapshot without API calls')
    parser.add_argument('--check', action='store_true', help='Compare without writing; use --offline for reproducible CI')
    args = parser.parse_args()
    snapshot = json.loads(SNAPSHOT.read_text(encoding='utf-8')) if args.offline else refresh()
    outputs = render(snapshot)
    if args.check:
        changed = [name for name, body in outputs.items() if not (ROOT / name).exists() or (ROOT / name).read_text(encoding='utf-8') != body]
        print('Out of date: ' + ', '.join(changed) if changed else 'Navigation matches snapshot')
        return int(bool(changed))
    if not args.offline:
        SNAPSHOT.parent.mkdir(exist_ok=True)
        SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, body in outputs.items():
        (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / name).write_text(body, encoding='utf-8')
    print(f'Rendered {len(snapshot["repositories"])} public repositories')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, ValueError, KeyError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
