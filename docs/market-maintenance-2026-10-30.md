# 期货与股指研究仓库维护 · 2026-10-30

本轮检查期货主仓库、股指、黄金、原油和欧线 EC 五个近期项目。原有 231 项测试全部通过，随后修复了发布导出流程的文件过滤问题。

## 已修复

[期货研究主仓库提交 b788557](https://github.com/Serennity007/taotao-futures-research/commit/b788557)：导出暂存和直接压缩现在使用同一过滤规则，排除 `.env`、`.env.*`、`.venv`、`venv` 及原有 Git、依赖、缓存文件。此前用假配置文件复现了这些本地文件被打入 ZIP，以及本地设置变化导致 ZIP 字节变化的问题。

新增 3 项回归测试检查单个 ZIP、八个专项加主仓库及组合套件的完整导出、哈希清单、原始文件保留和确定性。没有据此认定旧版已发布附件中含真实凭据；本轮只更新源码导出器，不替换旧 Release 附件。

## 复验结果

| 仓库 | 通过测试 |
| --- | ---: |
| taotao-futures-research | 101 |
| a-share-index-research-skill | 36 |
| gold-research-skill | 26 |
| crude-oil-research-skill | 35 |
| ec-shipping-research-skill | 36 |
| 合计 | 234 |

实际源码导出得到 10 个 ZIP，校验清单和路径检查通过。在工作区临时目录安装 9 个 Skill 后，8 个专项示例均完成，并未修改宿主实际 Skill 目录。五个仓库的共享计算核心逐文件哈希一致；四个独立仓库无需改运行代码，冻结示例未改动。

测试和演示使用构造数据、假设日历和费用规则；本轮未获取实时行情或验证投资表现。检查日期按北京时间。

[主仓库详细记录](https://github.com/Serennity007/taotao-futures-research/blob/main/docs/maintenance-2026-10-30.md) · [机器可读结果](https://github.com/Serennity007/taotao-futures-research/blob/main/docs/verification/2026-10-30-export.json)
