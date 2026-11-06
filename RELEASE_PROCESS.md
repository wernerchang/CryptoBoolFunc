# 固定版本更新与 GitHub 上传流程

本流程由维护者2026-11-04要求建立。后续涉及本项目的版本整理和上传沿用此流程；仅在用户授权当前更新/上传范围内执行。查核日以每次实际操作为准，不声称存在一项名为“最新上传规范”的统一强制标准。

1. **读取远端与本地状态。** 查看默认分支、最新提交、已有AGENTS/CONTRIBUTING、保护规则或ruleset；不要覆盖他人提交，不绕过保护。空仓库首次可先提交最小README建立main，再走主题分支。
2. **固定版本与范围。** 更新VERSION、CHANGELOG、RELEASE_NOTES，明确研究试用/正式级别、修复与未解项；不移动已发布版本所指内容。新增版本按1.0.1/1.1.0等编号。
3. **保留单一数学来源。** 只在skills或能力事实源修改，两个宿主安装包由同一技能内容生成；安装位置与宿主配置分开。
4. **先完成资料和验证。** TeX、PDF、代码、示例、测试、校勘、贡献者说明和日志齐备后才上传。运行tests/run_checks.py；编译两个教程并逐页渲染检查；记录未测账户/宿主。
5. **筛选公开内容。** 使用明确文件清单；不上传原始整书PDF、全文抽取、密钥、个人绝对路径、.env、缓存、编译临时文件。保留必要出处、来源哈希与公开许可说明。
6. **构建并校验。** 运行scripts/package_release.py生成两个ZIP、SHA256SUMS与manifest，校验ZIP字节/CRC；提交前检查变更清单和文件大小。
7. **主题分支提交。** 使用codex/v<版本>-<主题>，提交说明包含具体变化、验证与保留限制。README、CONTRIBUTORS记录Codex的AI协作贡献；只对已核实身份使用Co-authored-by邮箱。
8. **上传并创建PR。** 推送主题分支/创建Git提交树，然后打开指向默认分支的PR。说明新行为、验证、数学范围和未测项。空仓库初始化README是一次性例外，日志记录。
9. **复核与合并。** 读取远端提交SHA与文件树，核对上传哈希、检查状态及规则。当前用户已明确授权该次上传且规则允许时完成合并；需审批/失败检查时保持PR并报告具体条件，不强推或绕过。
10. **验证发布结果。** 重新读取main/合并提交及PDF、ZIP等文件条目，记录PR URL、提交SHA和核验状态。仓库releases/v版本目录是本项目版本资产；GitHub Release/标签只有确实创建后才能称已发布Release。

官方依据：[创建PR](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)、[Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)、[防止凭据误提交](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)。若上游规则改变，先更新核查记录和本流程，再执行当前版本。
