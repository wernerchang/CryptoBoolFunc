# 安装与上传流程的核查来源

核查日期2026-11-04。页面可能演进；教程给出可检查的成功标志，未把目录复制测试当作在线宿主验收。

- [OpenAI 官方技能指南](https://learn.chatgpt.com/docs/build-skills)：Codex本地扫描、完整目录、调用与重载。
- [OpenAI Codex 快速开始](https://developers.openai.com/codex/quickstart)：宿主安装/登录入口。
- [仓颉上游仓库](https://github.com/kangarooking/cangjie-skill)：完整安装包、Python/PyYAML和doctor。
- [仓颉v2.5.0附件](https://github.com/kangarooking/cangjie-skill/releases/tag/v2.5.0)：使用2026-09-13刷新附件及SHA256，自动Source code归档不含刷新说明中的全部变化。
- [DeepSeek Harness官方README](https://github.com/deepseek-ai/deepseek-harness)：Node启动命令；开发预览。
- [DeepSeek本地技能Provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)：一层目录发现、用户/项目扫描根。
- [DeepSeek Web UI](https://deepseek-harness.github.io/deepseek-harness/en/guide/quickstart)：模型配置、工作区选择、开始任务。
- [DeepSeek API](https://api-docs.deepseek.com/)：官方模型/API来源；不在教程中固化未核实的模型别名。
- [GitHub PR流程](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)、[Release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)：版本资产与仓库上传的区别。

本仓库采用这些指南制定项目流程，不将建议性实践称作GitHub统一强制规范。DeepSeek根文档旧链接未含/deepseek-harness路径时可能404，本教程采用已打开的有效入口。
