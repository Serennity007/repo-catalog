# 导航维护说明 / Maintenance

This catalog stores public metadata and file evidence. English and Chinese landing pages and the full index are generated from the same committed snapshot.

导航只采集公开元信息和文件证据。中英文首页与全量索引来自同一个已提交快照。

[2026-10-30 检查范围、修改与验证记录](maintenance-2026-10-30.md)

## 更新

在仓库根目录运行，先安装 Python 3.11+ 与 GitHub CLI 并执行 `gh auth login`：

```bash
python scripts/build_catalog.py
python -m unittest discover -s tests -v
python scripts/build_catalog.py --offline --check
git diff --stat
```

`data/featured.json` 保存人工挑选的用途、项目与入口；`data/repositories.json` 保存 API 快照及检查日期。修改推荐项后执行 `python scripts/build_catalog.py --offline` 即可生成文档，无需网络。

生成文件：`README.md`（英语）、`README.zh-CN.md`（中文）、`docs/catalog.md`（全量主题索引）。`--check` 不写文件；`--offline --check` 根据已提交快照比对，不受 GitHub 实时计数或当前日期影响。

## 内容状态

| 状态 | 证据 | 不代表什么 |
| --- | --- | --- |
| ✅ 含文件内容 | Git tree 中存在 README、许可证、常见协作文件和 `.github/` 元文件以外的文件 | 不代表功能完备、原创性或测试通过 |
| 📖 README 文档库 | 没有上述文件，但 README 去除标题、注释和许可证尾部后至少 400 字符、5 个非空行 | 只说明文档有正文，不是资料质量评分 |
| 🟡 占位 | 只有许可证、简短 README 或元文件 | 不推断未来计划，也不删除仓库 |
| ⚪ 空仓库 | API 明确返回仓库没有 Git 提交，或有效文件树没有 blob | 不把网络失败视为空仓库 |

Fork 按 GitHub `fork` 字段单列；描述自述转载/镜像的仓库单列。其他分类是导航主题，不构成原创认证。静态站点、演示应用与源码项目通过描述说明用途；首页只挑选已有内容的公开项目。

分类按仓库名匹配，并对阅读器、命令行、安全、科研与市场项目设置优先顺序。需要纠正特例时修改脚本中的 `EXPLICIT`；新增主题时同步 `GROUPS`。全量索引为主题设置稳定英文锚点，避免中文标题变化破坏导航。

## 失败处理与数据边界

- 所有分页必须成功。鉴权失败、限流、网络故障或不完整 Git tree 会终止生成，不覆盖已有索引。
- 内容判定使用 Git tree，不依赖会滞后的仓库 `size`；README 正文按该文件树里的 blob SHA 读取。
- API 只请求该账号的公开仓库；快照在写出前再次校验公开状态、仓库名、归属与重复项。不记录私有仓库名称、数量、路径或访问凭据。
- `checked_on` 与最近更新栏均使用北京时间。快照保留 GitHub 原始 UTC 时间，便于核查。推送时间可能包含非默认分支活动，不等同于软件版本发布日期。
- 文件证据是一次快照；使用项目之前以对应仓库的 README、Release 和验证记录为准。

## GitHub Actions 模板

校验和每周刷新模板位于 [workflows/catalog.yml](workflows/catalog.yml)。当前维护凭据没有 `workflow` scope，所以模板未写入 `.github/workflows/`，自动刷新尚未启用。

有工作流写入权限后，将该文件复制为 `.github/workflows/catalog.yml` 并推送到默认分支。模板在普通 push/PR 时离线校验；每周一北京时间 09:20 或手动运行时在线刷新。刷新成功且有实际改动才提交，任何 API/测试错误都会停止推送。工作流仅向本仓库写入生成的快照与导航文件。

GitHub 对长期无活动的公开仓库可能停用定时运行；工作流的最近成功记录才是实际刷新证据。
