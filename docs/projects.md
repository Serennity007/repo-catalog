# 六个代表项目 · First run

[中文导航](../README.zh-CN.md) · [English navigator](../README.md) · [作品集 / Portfolio](https://serennity007.github.io/Serennity007-portfolio/#featured-projects) · [维护分级](lifecycle.md)

人工选定的维护重点；内容核对于 2026-10-30。重点不代表稳定性评级或固定响应期限。

These are selected maintenance priorities, not stability ratings or a response-time guarantee.

在新目录克隆源码。Python 项目建议先创建独立虚拟环境，并用该环境的 Python 执行命令；安装依赖需要网络。下列脚本演示不拉取实时行情，不需要付费 API。

Clone into a new directory. For Python projects, create and activate a dedicated virtual environment first. Dependency installation needs network access. The listed demos do not fetch live prices or require paid APIs.

| 项目 | 解决什么问题 | 开始使用 |
| --- | --- | --- |
| [awesome-stock-quant-skills](https://github.com/Serennity007/awesome-stock-quant-skills) | 把财务筛选、共识排序和含成本回测串成可复核的研究流程。 | [首次运行](https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md#quant) |
| [xss-audit-desktop](https://github.com/Serennity007/xss-audit-desktop) | 让安全审查保留源码位置、有限流向证据和人工复核结论。 | [首次运行](https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md#audit) |
| [agent-trace](https://github.com/Serennity007/agent-trace) | 从编码 Agent 的本地日志查看 token、工具调用和成本估算。 | [首次运行](https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md#agent-trace) |
| [paper-zh-translation](https://github.com/Serennity007/paper-zh-translation) | 在保留论文版面坐标的前提下，把已有中文译文写回 PDF 并检查。 | [首次运行](https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md#paper) |
| [beiligong-ppt-skill](https://github.com/Serennity007/beiligong-ppt-skill) | 把字号、底色、标题与院标调整变成可复跑的课件改版流程。 | [首次运行](https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md#ppt) |
| [taotao-futures-research](https://github.com/Serennity007/taotao-futures-research) | 在共同区间、信息时点与样本覆盖明确的条件下比较产业板块。 | [首次运行](https://github.com/Serennity007/repo-catalog/blob/main/docs/projects.md#futures) |

<a id="quant"></a>

## 股票与量化研究工具链 / Stock and quant research tools

`awesome-stock-quant-skills` · 默认分支 / default branch: `main`

| 项目说明 / Field | 中文 | English |
| --- | --- | --- |
| 用途 / Purpose | 把财务筛选、共识排序和含成本回测串成可复核的研究流程。 | Connect financial screening, consensus ranking and cost-aware backtest arithmetic. |
| 输入 / Input | 内置合成 CSV；实际研究另行准备财务和行情数据。 | Bundled synthetic CSVs; real research needs separately prepared market and financial data. |
| 输出 / Output | REPORT.md、排名 CSV、持仓、成本与输入哈希。 | REPORT.md, rank CSVs, holdings, costs and input hashes. |
| 具体实现 / Contribution | 原创 Skills 与脚本，含多框架合成和回测核算；第三方合集另有来源说明。 | Original Skills and scripts for consensus and backtest arithmetic; third-party collections retain attribution. |
| 环境 / Environment | Python 3.11+；演示依赖 NumPy、pandas。 | Python 3.11+ with NumPy and pandas for the demo. |
| 边界 / Limits | 演示是两个独立合成场景；计算通过不代表投资效果。 | Two independent synthetic scenarios; successful arithmetic does not establish investment performance. |

```sh
git clone https://github.com/Serennity007/awesome-stock-quant-skills.git
cd awesome-stock-quant-skills
python -m pip install -r requirements-demo.txt
python scripts/run_demo.py
```

**成功时 / Expected:** 终端打印 PASS 和新的 output/demo/run-…/REPORT.md 路径。 The terminal prints PASS and a new output/demo/run-…/REPORT.md path.

[完整指南 / Guide](https://github.com/Serennity007/awesome-stock-quant-skills/blob/main/docs/quickstart.md) · [验证及变更范围 / Evidence](https://github.com/Serennity007/awesome-stock-quant-skills/blob/main/docs/validation.md)

[在线体验与案例 / Browser demo or case](https://serennity007.github.io/Serennity007-portfolio/project-quant.html)

<a id="audit"></a>

## 源码静态审计工作台 / Static source review workbench

`xss-audit-desktop` · 默认分支 / default branch: `main`

| 项目说明 / Field | 中文 | English |
| --- | --- | --- |
| 用途 / Purpose | 让安全审查保留源码位置、有限流向证据和人工复核结论。 | Keep source locations, bounded flow evidence and human decisions together. |
| 输入 / Input | 本地源码、公开仓库快照或内置 demo-project。 | Local source, public repository snapshots or the bundled demo-project. |
| 输出 / Output | 审查信号、覆盖情况与 HTML / SARIF 等报告。 | Review signals, coverage information and HTML / SARIF reports. |
| 具体实现 / Contribution | 基于 xss-audit 方法扩展扫描引擎、AST 分析、桌面与浏览器复核界面。 | Extend the xss-audit playbook with a scanner, AST analysis and desktop/browser review interfaces. |
| 环境 / Environment | 源码 Python 3.11+；Windows 便携包与浏览器版另有入口。 | Python 3.11+ for source; separate Windows portable and browser entrypoints. |
| 边界 / Limits | 信号需人工确认；浏览器和桌面覆盖不同，源码复验不等于重测发布包。 | Signals need human confirmation. Browser/desktop coverage differs; source checks do not revalidate published binaries. |

```sh
git clone https://github.com/Serennity007/xss-audit-desktop.git
cd xss-audit-desktop
python -m pip install .
python -m xss_audit.cli examples/demo-project --format html -o demo-review.html
```

**成功时 / Expected:** 生成 demo-review.html，列出合成示例的审查信号及覆盖情况。只扫描示例，不执行其源码。 demo-review.html lists review signals and coverage for the synthetic fixture. Scan it without executing its source.

[完整指南 / Guide](https://github.com/Serennity007/xss-audit-desktop/blob/main/README.md) · [验证及变更范围 / Evidence](https://github.com/Serennity007/xss-audit-desktop/blob/main/docs/verification/2026-10-30-source.json)

[在线体验与案例 / Browser demo or case](https://serennity007.github.io/xss-audit-desktop/)

<a id="agent-trace"></a>

## Agent 本地会话分析 / Local agent session analysis

`agent-trace` · 默认分支 / default branch: `main`

| 项目说明 / Field | 中文 | English |
| --- | --- | --- |
| 用途 / Purpose | 从编码 Agent 的本地日志查看 token、工具调用和成本估算。 | Inspect tokens, tool calls and estimated costs from local coding-agent logs. |
| 输入 / Input | 指定目录的受支持日志；首次运行使用公开合成样本。 | Supported logs in an explicit directory; use the public synthetic fixture first. |
| 输出 / Output | 终端汇总或可解析的 JSON。 | Terminal summaries or parseable JSON. |
| 具体实现 / Contribution | 多种日志解析器、会话与工具统计、终端及 JSON 输出。 | Agent log parsers, session/tool statistics and terminal/JSON output. |
| 环境 / Environment | Node.js 18+、npm；源码安装需要包源访问。 | Node.js 18+ and npm; dependency installation needs registry access. |
| 边界 / Limits | 日志格式覆盖有限；价格使用内置估算，不是账单。源码修复未发布到 npm。 | Log-format coverage is limited. Built-in price estimates are not invoices. Source fixes are not published to npm. |

```sh
git clone https://github.com/Serennity007/agent-trace.git
cd agent-trace
npm ci --ignore-scripts
node bin/cli.js examples/session-demo -a opencode --json
```

**成功时 / Expected:** 输出一个 session 为 synthetic-demo 的 JSON 对象；不会读取个人会话。 Print one JSON object with session synthetic-demo without reading personal sessions.

[完整指南 / Guide](https://github.com/Serennity007/agent-trace/blob/main/docs/first-run.md) · [验证及变更范围 / Evidence](https://github.com/Serennity007/agent-trace/blob/main/CHANGELOG.md)

<a id="paper"></a>

## 论文 PDF 中文排版流程 / Chinese PDF translation workflow

`paper-zh-translation` · 默认分支 / default branch: `main`

| 项目说明 / Field | 中文 | English |
| --- | --- | --- |
| 用途 / Purpose | 在保留论文版面坐标的前提下，把已有中文译文写回 PDF 并检查。 | Write supplied Chinese translations into the paper's PDF coordinates and inspect the result. |
| 输入 / Input | 有文本层的 PDF、逐段译文 JSON 与中文字体。 | A text-layer PDF, translated segment JSON and Chinese fonts. |
| 输出 / Output | 中文 PDF、可复跑的译文工程和五项版面检查。 | A Chinese PDF, reproducible translation inputs and five layout checks. |
| 具体实现 / Contribution | 整理六阶段 Skill、提取/回写/质检脚本和共享输入校验。 | A six-stage Skill, extraction/build/QA scripts and shared input validation. |
| 环境 / Environment | Python 3.11+、PyMuPDF、fonttools 及可用中文字体。 | Python 3.11+, PyMuPDF, fonttools and available Chinese fonts. |
| 边界 / Limits | 脚本不自动生成译文；扫描件需先 OCR，合成自检不代表真实论文翻译质量。 | Scripts do not generate translations. Scans need OCR; a synthetic check does not validate real-paper translation quality. |

```sh
git clone https://github.com/Serennity007/paper-zh-translation.git
cd paper-zh-translation
python -m pip install -r requirements.txt
python tests/smoke_test.py
```

**成功时 / Expected:** 合成 PDF 完成提取、写入与质检，五项问题数为 0；临时文件自动清理。 The synthetic PDF passes extraction, build and QA with five zero issue counts; temporary files are cleaned up.

[完整指南 / Guide](https://github.com/Serennity007/paper-zh-translation/blob/main/README.md) · [验证及变更范围 / Evidence](https://github.com/Serennity007/paper-zh-translation/blob/main/CHANGELOG.md)

<a id="ppt"></a>

## 已有 PPTX 批量改版 / Batch formatting for existing PPTX

`beiligong-ppt-skill` · 默认分支 / default branch: `master`

| 项目说明 / Field | 中文 | English |
| --- | --- | --- |
| 用途 / Purpose | 把字号、底色、标题与院标调整变成可复跑的课件改版流程。 | Turn font, background, title and logo changes into a repeatable slide workflow. |
| 输入 / Input | 已有 PPTX 和按课件调整的配置；首次运行用合成单页。 | An existing PPTX with deck-specific configuration; begin with a synthetic slide. |
| 输出 / Output | 分版本 PPTX、字号映射和扫描 JSON；完整流程另含实测与审计。 | Versioned PPTX files, font-size mappings and scan JSON; the full workflow adds measurement and audit. |
| 具体实现 / Contribution | 课件改版 Skill、批处理脚本、PowerPoint 实测回退与输出路径保护。 | A slide workflow, batch scripts, PowerPoint measurement/fallback and output-path guards. |
| 环境 / Environment | 基础演示只需 Python 3.10+ 与 python-pptx；实测/导出需 Windows PowerPoint。 | The basic demo needs Python 3.10+ and python-pptx; measurement/export needs Windows PowerPoint. |
| 边界 / Limits | 无 Office 演示只验证扫描和字号映射，不证明排版可交付；fit 未绑定课件指纹。 | The Office-free demo checks scanning and size mapping, not deliverable layout. Fit data is not bound to a deck fingerprint. |

```sh
git clone https://github.com/Serennity007/beiligong-ppt-skill.git
cd beiligong-ppt-skill
python -m pip install "python-pptx>=1.0.2,<2"
python examples/run_demo.py
```

**成功时 / Expected:** 打印 PASS 和新的 _build/demo-… 目录，含 source.pptx、enlarged.pptx、scan.json、size_map.json。 Print PASS and a new _build/demo-… directory with source.pptx, enlarged.pptx, scan.json and size_map.json.

[完整指南 / Guide](https://github.com/Serennity007/beiligong-ppt-skill/blob/master/README.md) · [验证及变更范围 / Evidence](https://github.com/Serennity007/beiligong-ppt-skill/blob/master/CHANGELOG.md)

<a id="futures"></a>

## 期货分板块研究工作台 / Sector-based futures research desk

`taotao-futures-research` · 默认分支 / default branch: `main`

| 项目说明 / Field | 中文 | English |
| --- | --- | --- |
| 用途 / Purpose | 在共同区间、信息时点与样本覆盖明确的条件下比较产业板块。 | Compare sectors with explicit common windows, information cutoffs and sample coverage. |
| 输入 / Input | 内置合成配置，或用户准备并注明来源的市场与产业数据。 | Bundled synthetic configuration or user-supplied, source-labelled market and industry data. |
| 输出 / Output | 中英文 HTML / Markdown、JSON、冻结输入与 SHA-256 清单。 | English/Chinese HTML and Markdown, JSON, frozen inputs and SHA-256 manifests. |
| 具体实现 / Contribution | 八个专项 Skills 的统一工作台、数据契约、证据与风险核算工具。 | A shared desk for eight specialist Skills, data contracts, evidence handling and risk arithmetic. |
| 环境 / Environment | Python 3.10+；基础离线命令只用标准库。 | Python 3.10+; base offline commands use the standard library. |
| 边界 / Limits | 样例使用合成数据与虚构规则；研究计算不构成已验证交易策略。 | Fixtures use synthetic data and fictional rules; research calculations are not validated trading strategies. |

```sh
git clone https://github.com/Serennity007/taotao-futures-research.git
cd taotao-futures-research
python scripts/run_desk.py run --config examples/desk-demo/ferrous/config.json --out output
```

**成功时 / Expected:** 新输出目录包含中英文报告、JSON 和可校验的输入/输出清单。 A new output directory contains bilingual reports, JSON and verifiable input/output manifests.

[完整指南 / Guide](https://github.com/Serennity007/taotao-futures-research/blob/main/README.zh-CN.md) · [验证及变更范围 / Evidence](https://github.com/Serennity007/taotao-futures-research/blob/main/docs/maintenance-2026-10-30.md)
