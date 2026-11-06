# CryptoBoolFunc 第一版

**版本 1.0.0 · 第一版研究试用版 · 2026-11-05**

利用仓颉 cangjie-skill 方法，将《密码函数》中的限定构造方法整理为可调用、可复算、可审查的技能与研究资料。保留 **1 个入口、15 张能力卡、23 个术语和精确小参数工具**。

## 从这里开始

| 目标 | 文件 |
|---|---|
| Codex 安装与使用 | [保姆级教程 PDF](docs/tutorial-codex-v1.pdf) / [TeX 源码](docs/tutorial-codex-v1.tex) |
| DeepSeek Harness 安装与使用 | [保姆级教程 PDF](docs/tutorial-deepseek-v1.pdf) / [TeX 源码](docs/tutorial-deepseek-v1.tex) |
| 下载两种安装版本 | [Codex 第一版 ZIP](releases/v1.0.0/CryptoBoolFunc-v1.0.0-codex.zip) / [DeepSeek 第一版 ZIP](releases/v1.0.0/CryptoBoolFunc-v1.0.0-deepseek.zip) |
| 了解设计思想 | [蒸馏精华](docs/research/DIGEST.md)、[章节理解](docs/research/BOOK_OVERVIEW.md)、[证明档案](docs/research/PROOF_DOSSIERS.md) |
| 查校勘与边界 | [来源核查](docs/research/SOURCE_CORRECTIONS.md)、[测试报告](docs/research/test-results.md)、[第一版说明](RELEASE_NOTES.md) |
| 后续贡献和发布 | [贡献者](CONTRIBUTORS.md)、[贡献流程](CONTRIBUTING.md)、[固定更新流程](RELEASE_PROCESS.md) |

## 安装速查

先按教程安装完整仓颉目录并验证，再安装本项目；Python 3.10+。以下命令在仓库根目录运行：

```powershell
python scripts/install.py --host codex --scope user --dry-run
python scripts/install.py --host codex --scope user
# 或使用 DeepSeek Harness：
python scripts/install.py --host deepseek --scope user
python tests/run_checks.py
```

Codex 当前用户目录为 `~/.agents/skills`；DeepSeek Harness 为 `${DSH_HOME:-~/.dsh}/skills`。第二种面向 **DeepSeek Harness 宿主**，需要本地技能服务与模型配置；网页聊天界面不能通过复制目录获得本地执行能力。完整操作、成功标志及排错见对应PDF。

## 研究范围

MM、正交谱、前缀划分、GMM谱预算、不相交码、零谱搬运、正规性、全分量指标、PS标签与递归平衡、**DS 的 R=I 子族**、向量阵列、对齐相关、校正阶与双等距码校正器。

一般DC存在性、完整HML/FAI求解器、混合阵列一般精确界等继续隔离。DS任意可逆R分支已由明确反例排除，未作为可用能力交付。高非线性度不自动保证低差分或系统安全。完整表工具主要限 n≤12、m≤6，具体子命令限制见输入指南。

独立任务测试：正常15/15、边界语义15/15；原严格字段28/30，差异保留。路由18/18。第一版编号表示发布快照，不表示所有数学或宿主均完成正式验收；未执行需要私人账户的在线DeepSeek/Codex全新安装会话测试。

## 贡献与来源

维护者：[wernerchang](https://github.com/wernerchang)。**AI 协作贡献者：Codex（OpenAI）**，详细贡献见[贡献者说明](CONTRIBUTORS.md)。仓颉为上游蒸馏框架，使用其官方安装包；本仓库不分发原始整书PDF或全文提取。
