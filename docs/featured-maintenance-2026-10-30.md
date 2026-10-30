# 2026-10-30 · 六个代表项目与维护分级

[作品集](https://serennity007.github.io/Serennity007-portfolio/#featured-projects) · [个人主页](https://github.com/Serennity007) · [六项首次运行](projects.md) · [维护分级](lifecycle.md)

## 展示和维护

- 六个维护重点：`awesome-stock-quant-skills`、`xss-audit-desktop`、`agent-trace`、`paper-zh-translation`、`beiligong-ppt-skill`、`taotao-futures-research`。
- `data/projects.json` 保存双语用途、输入、输出、具体实现、环境、适用边界、上手命令与证据链接。导航、首次运行指南、个人主页精选和作品集卡片共用这份清单。
- 351 个公开仓库分别显示重点、按需、参考或待评估。文件内容状态保持独立；本轮未自动归档、删除或转移仓库。
- 导出脚本只替换已标记区域，缺失/重复/倒置标记在写文件前报错。同步仍由维护者执行和分别提交，未启用跨仓库自动推送。
- 作品集更新旧的量化实现数量，链接带日期的 60 项测试记录；该历史数字不计入本轮测试。现有 PDF 简历保留为历史存档。

## 使用问题修复

- Agent Trace 的目录参数此前未传到发现逻辑，指定样本目录仍可能扫描个人日志。现在显式目录覆盖发现根目录，不存在的目录非零退出。
- Agent Trace 的 JSON 此前混有横幅与状态文本，多会话走终端汇总。现在 stdout 为单个 JSON 文档：单会话保留原字段与会话 ID，零/多会话使用数组；诊断进入 stderr。不额外输出原始对话正文。
- 修正十种语言的 npm 安装包名，统一 scoped package 和 lock 根信息；增加公开合成日志、源码首次运行指南与四个实际 CLI 集成场景。未发布 npm 新版本。
- PPT 新增无需 Office 的合成单页演示：扫描、字号放大与映射、源文件保留。每次创建独立输出目录；不把这项检查说成已完成 Office 实测或真实课件验收。

## 本地验证

| 范围 | 结果 |
| --- | --- |
| 导航、公开清单、导出保护与维护分级 | 25 项测试通过；离线渲染与跨仓库导出检查通过 |
| 作品集原有动效、开场与交互计算 | 45 项测试通过 |
| Agent Trace | 原有 12 项检查和 4 项实际 CLI 场景通过；实际 npm tarball 独立安装后入口与合成样例通过 |
| PPT | 原有 14 项回归通过，新增合成演示打印 PASS |
| 量化 | 两个独立合成场景打印 PASS，生成报告、CSV、持仓、成本与输入记录 |
| 期货 | 黑色合成 desk 状态 complete，保存中英文报告与清单 |
| 论文 PDF | 合成单页提取、写回与 QA 通过，五项问题数均为 0 |
| 源码审计 | 已安装的源码环境扫描 2 个示例文件，生成含 11 个审查信号的 HTML |
| 页面布局 | 320px 手机宽度为单栏，1200px 桌面宽度为双栏，均未发现横向溢出；六个开始使用链接与生成锚点一致 |

共 100 项本地自动检查，六条首次运行路径另行验证。未运行真实论文翻译、Office 渲染、实时行情研究，未重建桌面发布包或更新 npm 已发布版本。

GitHub 个人主页的六项 README 精选不等于账户的 Pinned 设置。网页未登录，本轮未修改置顶栏。

## 已发布源码与远端检查

| 仓库 | 本轮源码提交 |
| --- | --- |
| Agent Trace | [33d3a6a：目录与 JSON 修复](https://github.com/Serennity007/agent-trace/commit/33d3a6a29d81f3871e817c6e36ab2c0eb2168ffa)；[9d8a644：旧版 CI 测试清理兼容](https://github.com/Serennity007/agent-trace/commit/9d8a64463dd262ce1246d89f588fdede8e4187fb) |
| PPT | [3329348：无 Office 合成上手演示](https://github.com/Serennity007/beiligong-ppt-skill/commit/3329348) |
| Profile | [f705f62：六项精选与首次运行入口](https://github.com/Serennity007/Serennity007/commit/f705f62) |
| Portfolio | [25392e9：六项静态展示与旧数量校正](https://github.com/Serennity007/Serennity007-portfolio/commit/25392e93a4f18ea1ee523faf227ed9c9d0c93acb) |
| Catalog | [cfbe60f：统一清单、上手指南与维护分级](https://github.com/Serennity007/repo-catalog/commit/cfbe60f) |

[Agent Trace CI](https://github.com/Serennity007/agent-trace/actions/runs/41075644602) 在 Node 16 / 18 / 20 三个既有任务上通过；首次失败来自旧 Node 16 不支持测试清理钩子，后改成 `try/finally`，未跳过场景或修改工作流。上手环境仍建议 Node 18+。

[作品集 Pages 部署](https://github.com/Serennity007/Serennity007-portfolio/actions/runs/41075382585)成功；已在公开网址看到六个入口。导航本轮执行的是本地离线检查，不把未启用的导航工作流模板称为 CI 通过。
