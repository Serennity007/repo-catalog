# 维护优先级 / Maintenance priorities

[六个代表项目与首次运行](projects.md) · [全量索引](catalog.md)

这是仓库展示和后续投入的分级，不是发布稳定性、质量认证或固定维护承诺。不会自动归档、删除、转移仓库或向项目提交 Issue。

These labels guide presentation and future work. They are not software maturity ratings or response-time guarantees. They do not archive, delete, transfer or open issues in repositories.

| 优先级 / Priority | 如何确定 / Selection | 维护方式 / Work |
| --- | --- | --- |
| 重点 / Focus | `data/projects.json` 人工选定的六个公开源码项目 | 优先修复可复现问题，核对安装与合成示例、说明限制，重要变更保留验证记录。Prioritize reproducible defects, first runs and evidence. |
| 按需 / On demand | 其他含源码文件或正文文档的项目，排除 Fork / 镜像 | 有实际使用需求、缺陷或依赖变化时维护。Maintain when use, defects or dependency changes justify it. |
| 参考 / Reference | GitHub 标记的 Fork，或描述注明镜像 / 转载 | 保留上游与改动说明，按需同步，不把收录当原创成果。Retain upstream attribution and explain local changes. |
| 待评估 / Pending | 占位或空仓库，未进入上述类别 | 不占重点展示位；逐项判断是否补充、合并或归档。No focus placement; assess individually before further action. |

最新创建的仓库优先检查“是否能运行、入口是否清楚”。GitHub 推送时间可能只是文档或非默认分支变更，不能据此认定功能更新或成熟度。

Review new repositories for runnable behavior and a clear entrypoint. A recent push can be documentation or non-default-branch activity; it does not establish a feature release or maturity.

维护顺序：影响使用的缺陷 → 安装与首次运行 → 示例和验证记录 → 发布包 → 展示文字。通过项目相关检查后结束该项，不为刷新日期制造提交。

Work order: user-facing defects → installation/first run → examples/evidence → release packaging → presentation. Stop when relevant checks pass; do not commit merely to refresh a date.

`data/repositories.json` 保存公开文件证据；`data/projects.json` 保存人工精选的用途、输入、输出、环境、贡献、限制和上手命令。内容状态和维护优先级是两个独立维度。
