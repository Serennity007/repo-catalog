# 最新仓库维护 · 2026-10-30

按北京时间核对了公开仓库的新建和推送时间，本轮重点维护最新新建的 [paper-zh-translation](https://github.com/Serennity007/paper-zh-translation) 与近期持续更新的 [xss-audit-desktop](https://github.com/Serennity007/xss-audit-desktop)。

## 论文翻译 Skill：修复输入错误被忽略

旧版本会接受 `p0b9999` 等不存在的段落 ID，跨 JSON 文件出现同一 ID 时后面的译文会覆盖前面的内容。在短英文合成 PDF 上，即使译文 ID 不存在、中文完全没有写进 PDF，旧质检也可能返回零问题。

[修复提交 fb365b2](https://github.com/Serennity007/paper-zh-translation/commit/fb365b2) 让构建和质检共享输入校验：

- 拒绝未知 ID、重复 JSON 键、条目放错页面、非文本译文和无效的合并目标。
- 检查页码范围和所选页是否含译文，输入错误在字体准备与 PDF 写出前终止，保留已有输出。
- 保留局部翻译、合法的空字符串合并片段；支持 UTF-8 BOM。
- 同步中英文说明、Skill 流程与 JSON 格式说明。

验证：新增 14 项回归测试通过；合成双栏 PDF 的提取 → 构建 → 质检端到端自检通过，5 类问题计数均为 0。合成数据只验证程序行为，没有重译或复核真实论文。详见[变更记录](https://github.com/Serennity007/paper-zh-translation/blob/main/CHANGELOG.md)。

## 审计工具：重新验证安装和当前源码

按项目声明的依赖在新的 Python 3.11.9 虚拟环境中安装，成功构建并安装 wheel。隔离导入已安装的包后，附带样例扫描读取 2 个文件、生成 11 条待复核线索，未报告扫描不完整。

完整源码测试发现 148 项：145 项通过，3 项因 Windows 符号链接创建权限跳过，失败和错误均为 0。第一次直接使用全局 Python 时缺少 AST 依赖；装齐项目依赖后原有测试正常，因此没有据此修改扫描逻辑。

[维护提交 4e486de](https://github.com/Serennity007/xss-audit-desktop/commit/4e486de) 修正中英文 README 沿用的 v0.3.0 测试数字，补充[本次源码复验记录](https://github.com/Serennity007/xss-audit-desktop/blob/main/docs/verification/2026-10-30-source.json)和总导航入口。本轮未重建 Windows EXE、修改浏览器应用或调用付费模型；Release 中原有的 17 项打包 CLI 检查是此前 v0.4.0 的记录。

两个项目已发布到各自的 `main`。导航快照和最近更新列表同步本次维护后的公开元信息。
