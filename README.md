[English](README.md) · [简体中文](README.zh-CN.md)

# Serennity007 · Repository Navigator

Find a tool by task, then browse the complete public repository index.

[Profile](https://github.com/Serennity007) · [Portfolio](https://serennity007.github.io/Serennity007-portfolio/) · [Full index / 全量索引](docs/catalog.md) · [Maintenance / 维护说明](docs/maintenance.md)

> Checked: **2026-10-30 (Asia/Shanghai)** · **351 public repositories** · 106 with files · 3 README guides · 242 placeholders · 0 empty.

## Start with a task

| Task | Project | Entry |
| --- | --- | --- |
| Financial screening, consensus ranking and backtesting | [awesome-stock-quant-skills](https://github.com/Serennity007/awesome-stock-quant-skills) | [Quick start](https://github.com/Serennity007/awesome-stock-quant-skills/blob/main/docs/quickstart.md) |
| Sector-based futures research and reproducible examples | [taotao-futures-research](https://github.com/Serennity007/taotao-futures-research) | [README](https://github.com/Serennity007/taotao-futures-research) |
| Gold, silver and macro context | [gold-research-skill](https://github.com/Serennity007/gold-research-skill) | [README](https://github.com/Serennity007/gold-research-skill) |
| A-share index breadth and market style | [a-share-index-research-skill](https://github.com/Serennity007/a-share-index-research-skill) | [README](https://github.com/Serennity007/a-share-index-research-skill) |
| Static source review with desktop, CLI and browser tools | [xss-audit-desktop](https://github.com/Serennity007/xss-audit-desktop) | [Releases](https://github.com/Serennity007/xss-audit-desktop/releases) |
| Translate paper PDFs into Chinese with layout guidance | [paper-zh-translation](https://github.com/Serennity007/paper-zh-translation) | [README](https://github.com/Serennity007/paper-zh-translation) |
| Batch PowerPoint formatting and measured font sizing | [beiligong-ppt-skill](https://github.com/Serennity007/beiligong-ppt-skill) | [README](https://github.com/Serennity007/beiligong-ppt-skill) |
| Finance RSS in Obsidian; derived from Qiaomu AI RSS | [serenity-stock-rss](https://github.com/Serennity007/serenity-stock-rss) | [Releases](https://github.com/Serennity007/serenity-stock-rss/releases) |
| Curated agent research reading | [zhengtao-picks](https://github.com/Serennity007/zhengtao-picks) | [README](https://github.com/Serennity007/zhengtao-picks) |
| Local coding-agent session usage analytics | [agent-trace](https://github.com/Serennity007/agent-trace) | [README](https://github.com/Serennity007/agent-trace) |
| Public-resource checks; extended upstream fork | [GhostTrack](https://github.com/Serennity007/GhostTrack) | [Releases](https://github.com/Serennity007/GhostTrack/releases) |
| Selected projects and bilingual resumes | [Serennity007-portfolio](https://github.com/Serennity007/Serennity007-portfolio) | [Portfolio](https://serennity007.github.io/Serennity007-portfolio/) |

## Browse by topic

| Topic / 主题 | Repositories / 仓库 | Content / 有内容 |
| --- | ---: | ---: |
| [股票 · 期货 · 量化](docs/catalog.md#markets) | 9 | 8 |
| [Obsidian · RSS · 精选阅读](docs/catalog.md#reading) | 7 | 7 |
| [安全 · 审计 · 逆向](docs/catalog.md#security) | 12 | 2 |
| [科研 · 论文 · 演示文稿](docs/catalog.md#research) | 7 | 7 |
| [命令行与 npm 工具](docs/catalog.md#cli) | 65 | 6 |
| [AI 编码 · Agent · Skills](docs/catalog.md#agents) | 40 | 20 |
| [学习路线 · 速查表 · 备考](docs/catalog.md#learning) | 43 | 3 |
| [后端 · 基础设施 · 数据](docs/catalog.md#infra) | 26 | 1 |
| [前端 · 设计 · 图形 · 视频](docs/catalog.md#frontend) | 27 | 8 |
| [语言与运行时生态](docs/catalog.md#languages) | 19 | 0 |
| [开发者资源索引](docs/catalog.md#resources) | 43 | 6 |
| [其他](docs/catalog.md#other) | 18 | 6 |
| [转载 · 镜像](docs/catalog.md#mirrors) | 16 | 16 |
| [Fork · 上游项目](docs/catalog.md#forks) | 17 | 17 |
| [个人主页 · 导航](docs/catalog.md#home) | 2 | 2 |

## Recently updated

| Project / 项目 | Pushed / 推送日期（北京时间） |
| --- | --- |
| [xss-audit-desktop](https://github.com/Serennity007/xss-audit-desktop) | 2026-10-30 |
| [paper-zh-translation](https://github.com/Serennity007/paper-zh-translation) | 2026-10-30 |
| [awesome-stock-quant-skills](https://github.com/Serennity007/awesome-stock-quant-skills) | 2026-10-30 |
| [Serennity007-portfolio](https://github.com/Serennity007/Serennity007-portfolio) | 2026-10-26 |
| [a-share-index-research-skill](https://github.com/Serennity007/a-share-index-research-skill) | 2026-10-26 |
| [ec-shipping-research-skill](https://github.com/Serennity007/ec-shipping-research-skill) | 2026-10-26 |
| [crude-oil-research-skill](https://github.com/Serennity007/crude-oil-research-skill) | 2026-10-26 |
| [gold-research-skill](https://github.com/Serennity007/gold-research-skill) | 2026-10-26 |

## Update and verify

```bash
python scripts/build_catalog.py             # GitHub API → snapshot + navigation
python scripts/build_catalog.py --offline --check
python -m unittest discover -s tests -v
```

Python 3.11+ and authenticated GitHub CLI (`gh auth login`) are needed for a refresh; offline rendering and tests use only the Python standard library. [Refresh workflow template and classification rules](docs/maintenance.md).

Content labels describe file evidence, not software quality, test coverage or an endorsement. Forks and declared mirrors are listed separately. Only public repository metadata is collected.
