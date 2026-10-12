#!/usr/bin/env python3
"""build_catalog.py — 从 GitHub API 生成仓库分类索引 README.md。

用法:
    python scripts/build_catalog.py            # 生成 README.md
    python scripts/build_catalog.py --check     # 只比对，不写文件（CI 用）

分类靠逐个仓库读 git tree 判定「有内容 / 只有占位」，不靠 size 字段
（size 会滞后：新推送的仓库可能仍报 0）。
"""
import argparse
import concurrent.futures
import io
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date

OWNER = os.environ.get("CATALOG_OWNER", "Serennity007")
PLACEHOLDER_README = re.compile(r"^\s*#\s+\S+\s+(developer resource\.?|)\s*$", re.I | re.M)


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True)
    if r.returncode:
        return None
    try:
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return None


def gh_private_count():
    """私有仓库数量。只有以仓库所有者身份认证时取得到，取不到就返回 None（不写这行）。"""
    r = subprocess.run(["gh", "repo", "list", OWNER, "--limit", "500", "--visibility", "private",
                        "--json", "name", "--jq", ".|length"], capture_output=True)
    if r.returncode:
        return None
    try:
        return int(r.stdout.decode("utf-8", "replace").strip())
    except ValueError:
        return None


def all_repos():
    out, page = [], 1
    while page <= 10:
        arr = gh(f"users/{OWNER}/repos?per_page=100&page={page}")
        if not arr:
            break
        out += arr
        if len(arr) < 100:
            break
        page += 1
    seen, uniq = set(), []
    for x in out:
        if x["full_name"] not in seen:
            seen.add(x["full_name"])
            uniq.append(x)
    return uniq


def inspect(x):
    """Return (has_content, note) determined from the actual file tree."""
    tree = gh(f"repos/{OWNER}/{x['name']}/git/trees/HEAD?recursive=1")
    if tree is None:
        return False, "空仓库（无提交）"
    blobs = [t for t in tree.get("tree", []) if t["type"] == "blob"]
    paths = [b["path"] for b in blobs]
    if not blobs:
        return False, "空仓库（无提交）"
    boiler = {"LICENSE", "README.md", ".gitignore", "CHANGELOG.md", "CONTRIBUTING.md",
              "CODE_OF_CONDUCT.md", ".banner.svg", "README.zh.md", "README.en.md"}
    real = [p for p in paths if os.path.basename(p) not in boiler]
    if not real:
        # README-only: is it a placeholder stub?
        rm = [p for p in paths if p.lower().startswith("readme")]
        if rm:
            data = gh(f"repos/{OWNER}/{x['name']}/readme")
            if data:
                import base64
                text = base64.b64decode(data["content"]).decode("utf-8", "replace")
                body = re.sub(r"#.*|## License.*|\[MIT\].*|\[GPL.*", "", text, flags=re.S).strip()
                if len(text) < 200 or PLACEHOLDER_README.search(text) or body in ("", "Developer resource."):
                    return False, "占位（仅 LICENSE/README）"
        return False, "占位（仅 LICENSE/README）"
    top = sorted({p.split("/")[0] for p in real})
    return True, f"{len(blobs)} 个文件｜{', '.join(top[:4])}"


GROUPS = [
    ("股票 · 量化 · 投资", r"stock|quant|trading|invest|a-share|a-stock|ibkr|tushare|qlib|openbb|moneyprinter|daily_stock|uzi|bitsoul|claude-trading|feishu-finance|finance-digest|earnings"),
    ("AI 编码 · Agent · 技能包", r"agent|skill|prompt|cursor|claude|copilot|llm|ai-|awesome-ai|mcp-|vibe|git-ai|npm-audit|paper-grill|token-meter|codeburn|git-diff|learn-ai"),
    ("Obsidian · RSS · 阅读与知识管理", r"obsidian|rss|picks|zhengtao|vault|sync|note"),
    ("安全 · 渗透 · 逆向", r"security|cyber|bug-bounty|ctf|forensic|exploit|hacking|malware|osint|pentest|reverse|vuln|faraday|havoc|empire|breachweave|cvs|yinvuln"),
    ("学习路线 · 速查表 · 备考", r"^learn-|cheatsheet|ielts|exam|guizhou|leetcode|roadmap|myielts|study|graduation"),
    ("命令行与 npm 工具", r"^cli-|-cli$|^ai-commit$|^git-format$|^vibe-check$|^agent-trace$|toml-validator|base64|calculator|color-picker|cron-parser|csv-parser|diff-viewer|hash-generator|http-client|json-|lorem|markdown-preview|password-gen|timer|todo-cli|uuid|weather|file-converter|dim-light"),
    ("后端 · 基础设施 · 数据", r"docker|kubernetes|devops|terraform|nginx|serverless|monitor|github-actions|data-pipeline|database|microservice|event-driven|api|rest-api|vector-db|system-design|postgres|redis|template"),
    ("前端 · 设计 · 图形 · 视频", r"react|vue|svelte|nextjs|astro|tailwind|figma|canva|adobe|sketch|blender|godot|unity|unreal|threejs|shader|webgl|frontend|design|portfolio|resume|video|image|food-map|paper-builder|zuograd|student-progress|blog|website"),
    ("语言与运行时生态", r"^awesome-(go|rust|python|typescript|deno|bun|functional|zig|java|dotnet|linux|macos|windows|terminal|vim|zsh|tmux|git-aliases|npm-packages)"),
    ("开发者资源索引", r"^awesome-"),
]


def classify(x):
    n = x["name"]
    d = (x.get("description") or "").lower()
    if x["fork"]:
        return "Fork · 上游项目"
    if n.startswith("mirror-"):
        return "镜像备份 · 他人项目"
    # 描述自陈 "Unofficial mirror of ..." 的是他人项目的公开转载，不能与原创混在一起。
    if d.startswith("unofficial mirror") or "for personal learning; all credit" in d:
        return "他人项目转载 · 非原创"
    if n == OWNER:
        return "主页"
    hay = (n + " " + d).lower()
    for label, pat in GROUPS:
        if re.search(pat, hay):
            return label
    return "其他"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    repos = all_repos()
    print(f"取到 {len(repos)} 个仓库，逐个判定内容状态...", file=sys.stderr)
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        flags = list(ex.map(inspect, repos))
    buckets = defaultdict(list)
    for x, (has, note) in zip(repos, flags):
        buckets[classify(x)].append((x, has, note))

    total = len(repos)
    real = sum(1 for h, _ in flags if h)
    priv = gh_private_count()
    lines = [
        "# 仓库总索引",
        "",
        f"共 **{total}** 个公开仓库：**{real} 个有实际内容**，{total - real} 个是只有 LICENSE/README 的占位仓库"
        "（早期批量创建的主题坑位）。状态按仓库真实文件构成判定，不靠 size 字段"
        "（size 会滞后，新推送的仓库可能仍报 0）。",
        "",
    ]
    if priv is not None:
        lines.append(f"另有 **{priv}** 个私有仓库不在本索引内（含第三方项目的私有镜像备份，不适合公开列出）。")
        lines.append("")
    lines += [
        "标记说明：✅ 有内容｜🟡 占位（主题已定、内容待填）｜🪞 他人项目转载（非原创）｜🔗 Fork",
        "",
        f"> 本文件由 `python scripts/build_catalog.py` 自动生成，最后更新 {date.today().isoformat()}。",
        "",
        "## 目录",
        "",
    ]
    order = [g for g, _ in GROUPS] + ["其他", "他人项目转载 · 非原创", "Fork · 上游项目", "镜像备份 · 他人项目", "主页"]
    for g in dict.fromkeys(order):
        if g in buckets:
            n = len(buckets[g])
            r = sum(1 for _, h, _ in buckets[g] if h)
            lines.append(f"- {g} — {n} 个（{r} 有内容）")
    lines.append("")

    for g in order:
        if g not in buckets:
            continue
        items = sorted(buckets[g], key=lambda t: (not t[1], t[0]["name"]))
        r = sum(1 for _, h, _ in items if h)
        lines += [f"## {g}", "", f"{len(items)} 个仓库，其中 {r} 个有内容。", "", "| 仓库 | 状态 | 说明 |", "|---|---|---|"]
        for x, has, note in items:
            if x["fork"]:
                mark = "🔗"
            elif x["name"].startswith("mirror-"):
                mark = "📦"
            elif g == "他人项目转载 · 非原创":
                mark = "🪞"
            else:
                mark = "✅" if has else "🟡"
            desc = (x.get("description") or "—").replace("|", "｜")
            if len(desc) > 110:
                desc = desc[:108] + "…"
            lines.append(f"| [`{x['name']}`](https://github.com/{OWNER}/{x['name']}) | {mark} | {desc} |")
        lines.append("")

    text = "\n".join(lines) + "\n"
    if args.check:
        old = io.open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else ""
        strip = lambda s: re.sub(r"最后更新 \d{4}-\d{2}-\d{2}。", "最后更新 。", s)
        same = strip(old) == strip(text)
        print("catalog 与现有 README 一致" if same else "catalog 有变化，需重新生成")
        return 0 if same else 1
    io.open("README.md", "w", encoding="utf-8").write(text)
    print(f"README.md 已生成：{total} 个仓库 / {real} 个有内容 / {len(buckets)} 个分类", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
