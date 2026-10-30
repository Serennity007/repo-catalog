# PPT 与 CLI 工具维护 · 2026-10-30

## PPT 排版工具

[beiligong-ppt-skill 修复 e456978](https://github.com/Serennity007/beiligong-ppt-skill/commit/e456978)：统一检查输入、输出路径，拒绝覆盖源 PPT、配置、字号映射和 fit，也拒绝多个输出指向同一文件。相对路径和已有硬链接别名会一并核对；冲突返回退出码 2，发生在写文件或启动 Office 之前。`--deliver` 保留更新独立交付文件的用途。

原有 8 项加新增 6 项，共 14 项测试通过。使用的是合成 PPT 和假 COM 对象；未进行真实 PowerPoint 渲染或真实课件视觉验收。路径检查没有解决 fit 与课件指纹及完整覆盖的校验边界，原有说明仍保留。[维护说明](https://github.com/Serennity007/beiligong-ppt-skill/blob/master/CHANGELOG.md)。

## git-format

[修复 6b2c995](https://github.com/Serennity007/git-format/commit/6b2c995)：帮助、版本命令在访问 Git 前退出；未知参数报错，避免误提交。旧版在暂存区非空时，执行 `--help` 也会创建提交，本轮已在临时仓库复现并修复。

JSON 模式 stdout 只保留 JSON，提交日志放在 stderr；空暂存区也返回有效对象。使用 NUL 分隔读取文件名，保留中文、空白和特殊字符，并用参数数组调用 Git。非 Git 目录等读取错误返回非零状态。单独 `--json` 仍然提交，预览应使用 `--dry-run --json`。

验证：原有 14 项检查及 7 个真实 CLI 场景通过。[Actions 运行记录](https://github.com/Serennity007/git-format/actions/runs/40999157650)。

## ai-commit

[修复 bb09106](https://github.com/Serennity007/ai-commit/commit/bb09106)：JSON stdout 去除横幅，空暂存区返回有效 JSON；修正 `--no-verify` 与 Commander 参数的对应关系。临时仓库里的拒绝提交 hook 在默认模式下仍生效，显式 `--no-verify` 时才跳过。

提交消息通过 Git 参数按字面量传递，文件列表保留中文和空白。同步修正十种语言文档的 scoped npm 安装命令、仓库链接及锁文件中的包名/版本元数据。

验证：原有 40 项检查及 4 个真实 CLI 场景通过。[Actions 运行记录](https://github.com/Serennity007/ai-commit/actions/runs/40999165287)。

## 交付范围

上面列出的两个 GitHub Actions 运行均已完成并成功，对应本轮 CLI 修复提交。

共 79 项本地检查通过，环境为 Windows / Node.js 24.18.0 / Python 3.11。两个 CLI 分别打包为本地 npm tarball，在工作区独立目录安装后，入口命令检查通过。测试只使用临时 Git 仓库、合成课件和受控 hook，没有操作用户的实际开发仓库或课件。

三个项目的源码修复已推送到默认分支，导航快照同步更新。**npm 注册表版本没有发布**，本轮修复位于 GitHub 源码；两个 CHANGELOG 均标记为 Unreleased。日期按北京时间。
