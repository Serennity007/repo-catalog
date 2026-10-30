"""One public project manifest for the catalog, profile and static portfolio."""
import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- featured-projects:start -->'
END = '<!-- featured-projects:end -->'
GUIDE = 'https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md'


def load(snapshot):
    data = json.loads((ROOT / 'data/projects.json').read_text(encoding='utf-8'))
    if data['schema_version'] != 1:
        raise ValueError('Unsupported project manifest')
    date.fromisoformat(data['reviewed_on'])
    by_name = {r['name']: r for r in snapshot['repositories']}
    names, anchors = set(), set()
    for item in data['projects']:
        name, anchor = item['name'], item['anchor']
        repo = by_name.get(name)
        if name in names or anchor in anchors or not re.fullmatch(r'[a-z0-9-]+', anchor):
            raise ValueError('Duplicate project or invalid anchor')
        if not repo or repo['private'] is not False or repo['fork'] or repo['archived'] or repo['inspection']['state'] != 'content':
            raise ValueError(f'Featured project must be a public, unarchived source repository: {name}')
        for field in ('title', 'problem', 'inputs', 'outputs', 'contribution', 'environment', 'limits', 'expected'):
            if any(not isinstance(item[field].get(lang), str) or not item[field][lang].strip() for lang in ('en', 'zh')):
                raise ValueError(f'Missing bilingual field: {name}/{field}')
        for field in ('guide_url', 'evidence_url', 'try_url'):
            if field not in item:
                continue
            parts = urlsplit(item[field])
            if parts.scheme != 'https' or parts.netloc not in ('github.com', 'serennity007.github.io'):
                raise ValueError(f'Unexpected project link: {name}/{field}')
        if not item['commands'] or any(not isinstance(c, str) or '\n' in c or '```' in c for c in item['commands']):
            raise ValueError(f'Invalid first-run commands: {name}')
        names.add(name)
        anchors.add(anchor)
    if not 1 <= len(names) <= 6:
        raise ValueError('Choose one to six focus projects')
    return data


def priority(repo, names):
    if repo['name'] in names:
        return '重点 / Focus'
    if repo['fork'] or 'mirror' in (repo.get('description') or '').lower() or '转载' in (repo.get('description') or ''):
        return '参考 / Reference'
    if repo['inspection']['state'] in ('placeholder', 'empty'):
        return '待评估 / Pending'
    return '按需 / On demand'


def md(value):
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ')


def table(data, lang):
    rows = ['| Project | Purpose | Start |' if lang == 'en' else '| 项目 | 解决什么问题 | 开始使用 |', '| --- | --- | --- |']
    for p in data['projects']:
        rows.append(f'| [{p["name"]}](https://github.com/Serennity007/{p["name"]}) | {md(p["problem"][lang])} | [{"First run" if lang == "en" else "首次运行"}]({GUIDE}#{p["anchor"]}) |')
    return '\n'.join(rows)


def guide(data, snapshot):
    by_name = {r['name']: r for r in snapshot['repositories']}
    lines = ['# 六个代表项目 · First run', '', '[中文导航](../README.zh-CN.md) · [English navigator](../README.md) · [作品集 / Portfolio](https://serennity007.github.io/Serennity007-portfolio/#featured-projects) · [维护分级](lifecycle.md)', '',
             f'人工选定的维护重点；内容核对于 {data["reviewed_on"]}。重点不代表稳定性评级或固定响应期限。', '',
             'These are selected maintenance priorities, not stability ratings or a response-time guarantee.', '',
             '在新目录克隆源码。Python 项目建议先创建独立虚拟环境，并用该环境的 Python 执行命令；安装依赖需要网络。下列脚本演示不拉取实时行情，不需要付费 API。', '',
             'Clone into a new directory. For Python projects, create and activate a dedicated virtual environment first. Dependency installation needs network access. The listed demos do not fetch live prices or require paid APIs.', '', table(data, 'zh'), '']
    for p in data['projects']:
        branch = by_name[p['name']]['default_branch']
        lines += [f'<a id="{p["anchor"]}"></a>', '', f'## {p["title"]["zh"]} / {p["title"]["en"]}', '',
                  f'`{p["name"]}` · 默认分支 / default branch: `{branch}`', '',
                  '| 项目说明 / Field | 中文 | English |', '| --- | --- | --- |']
        for field, label in [('problem', '用途 / Purpose'), ('inputs', '输入 / Input'), ('outputs', '输出 / Output'), ('contribution', '具体实现 / Contribution'), ('environment', '环境 / Environment'), ('limits', '边界 / Limits')]:
            lines.append(f'| {label} | {md(p[field]["zh"])} | {md(p[field]["en"])} |')
        lines += ['', '```sh', f'git clone https://github.com/Serennity007/{p["name"]}.git', f'cd {p["name"]}', *p['commands'], '```', '',
                  f'**成功时 / Expected:** {p["expected"]["zh"]} {p["expected"]["en"]}', '',
                  f'[完整指南 / Guide]({p["guide_url"]}) · [验证及变更范围 / Evidence]({p["evidence_url"]})', '']
        if p.get('try_url'):
            lines += [f'[在线体验与案例 / Browser demo or case]({p["try_url"]})', '']
    return '\n'.join(lines)


def profile(data, lang):
    heading = '## Six projects to start with' if lang == 'en' else '## 从六个代表项目开始'
    note = 'Selected maintenance priorities. Open each first-run guide for inputs, outputs, environment and limits.' if lang == 'en' else '人工选定的维护重点。首次运行指南列出输入、输出、环境和适用边界。'
    return f'{heading}\n\n{note}\n\n{table(data, lang)}\n\n[Portfolio / 作品集](https://serennity007.github.io/Serennity007-portfolio/#featured-projects) · [All projects / 全量索引](https://github.com/Serennity007/repo-catalog)\n'


def website(data):
    out = ['<section class="focus-projects" id="featured-projects" aria-labelledby="focus-title">',
           '  <div class="focus-heading"><div><p class="focus-kicker">SELECTED OPEN SOURCE · 06</p><h3 id="focus-title">选一个项目，实际跑起来</h3><p>从输入、实现到结果，先用公开样例走通一次。</p></div>',
           f'  <a href="{GUIDE}">六项上手指南 ↗</a></div>', '  <div class="focus-grid">']
    for p in data['projects']:
        e = lambda key: escape(p[key]['zh'])
        extra = f'<a href="{escape(p["try_url"], quote=True)}">在线体验与案例</a>' if p.get('try_url') else ''
        out += [f'    <article class="focus-card" id="focus-{escape(p["anchor"])}">',
                f'      <div class="focus-card-top"><span>{escape(p["symbol"])}</span><span>重点维护</span></div>',
                f'      <h4>{e("title")}</h4><p class="focus-repo">{escape(p["name"])}</p><p class="focus-purpose">{e("problem")}</p>',
                '      <dl>', *[f'        <div><dt>{label}</dt><dd>{e(key)}</dd></div>' for key, label in [('inputs', '输入'), ('outputs', '产物'), ('contribution', '实现')]],
                f'      </dl><p class="focus-environment">{e("environment")}</p>',
                f'      <p class="focus-limits">{e("limits")}</p>',
                f'      <div class="focus-links"><a class="focus-start" href="{GUIDE}#{escape(p["anchor"])}">开始使用 ↗</a><a href="{escape(p["guide_url"], quote=True)}">源码与指南</a><a href="{escape(p["evidence_url"], quote=True)}">验证范围</a>{extra}</div>',
                '    </article>']
    out += ['  </div>', f'  <p class="focus-footnote">内容核对 {data["reviewed_on"]} · 重点为维护优先级，功能范围以各项目说明为准。<a href="https://github.com/Serennity007/repo-catalog/blob/main/docs/lifecycle.md">维护分级 ↗</a></p>', '</section>']
    return '\n'.join(out) + '\n'


def replace_block(text, body):
    if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
        raise ValueError('Expected exactly one ordered generated block; no file was written')
    return text[:text.index(START)] + START + '\n' + body.rstrip() + '\n' + text[text.index(END):]


def export(data, profile_root=None, portfolio_root=None, check=False):
    outputs = {}
    if profile_root:
        for name, lang in [('README.md', 'en'), ('README.zh.md', 'zh')]:
            path = Path(profile_root).resolve() / name
            outputs[path] = replace_block(path.read_text(encoding='utf-8'), profile(data, lang))
    if portfolio_root:
        path = Path(portfolio_root).resolve() / 'index.html'
        outputs[path] = replace_block(path.read_text(encoding='utf-8'), website(data))
    # Read and validate all destinations before writing any of them.
    changed = [p for p, body in outputs.items() if p.read_text(encoding='utf-8') != body]
    if not check:
        for path in changed:
            path.write_text(outputs[path], encoding='utf-8')
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path)
    parser.add_argument('--portfolio', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if not args.profile and not args.portfolio:
        parser.error('Choose --profile and/or --portfolio checkout')
    snapshot = json.loads((ROOT / 'data/repositories.json').read_text(encoding='utf-8'))
    changed = export(load(snapshot), args.profile, args.portfolio, args.check)
    print(('Out of date: ' if args.check else 'Updated: ') + ', '.join(str(p) for p in changed) if changed else 'Project displays match manifest')
    return int(args.check and bool(changed))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
