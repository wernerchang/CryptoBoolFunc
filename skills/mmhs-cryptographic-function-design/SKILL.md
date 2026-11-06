---
name: mmhs-cryptographic-function-design
description: |
  当用户设计或核验布尔函数、多输出密码函数、MM/GMM/PS/DS结构、谱支撑、正交序列或独立同偏差源校正器时使用。提供15项限定方法与精确小参数工具。研究试用版：一般DC存在性、完整HML/FAI求解器和混合阵列精确界不属于已验收能力；不用于普通代码布尔逻辑问答或直接保证密码系统安全。
metadata:
  cangjie.generated-by: cangjie-tools v2.5.0
  cangjie.variant: single
  cangjie.bundle-id: bundle.mmhs-update
  cangjie.capability-count: 15
  cangjie.entrypoint-count: 1
---
# 密码函数（限定范围研究试用版） — 全书能力入口

## 触发与不触发

**适用**：与本书能力域相关的咨询与任务（见下方路由表的意图列）。
**不适用**：
- 一般DC零谱兼容选择的存在性证明；完整HML及FAI优化求解器；3.37/3.41混合构造的一般精确界。
- 由高非线性度直接推出低差分、代数免疫最优、移位相关或系统安全。
- 本书之外的最新研究现状及新颖性查新；普通软件布尔表达式问题。

## 核心原则（常驻速览，概览类问题读到这里即可回答）

1. 先固定域多项式、基、位序和指标契约，再构造。
2. 多输出性质逐一核验全部2^m−1个非零分量。
3. 下界、精确值和极值见证分别记录。
4. 生成、证明、数值实例和应用模型分别验收。
5. 低重量谱逐点为零与同重量层谱和为零严格区分。
6. 以限定范围使用研究试用版；来源校勘及待核查不升级为已证定理。

## 能力路由（先读本表，按意图加载 1 张能力卡）

| 用户意图 | 先读 | 补读/备注 |
|---|---|---|
| 设计MM函数；核验单射、互补像集、弹性与SAC | references/capabilities/mm-spectrum.md | references/capabilities/vector-contract.md、references/capabilities/orthogonal-spectrum.md |
| 选择部分线性及Bent核组成的正交谱层 | references/capabilities/orthogonal-spectrum.md | references/capabilities/mm-spectrum.md、references/capabilities/gmm-budget.md |
| 为不同块尺寸生成不交完备前缀划分 | references/capabilities/prefix-partition.md | references/capabilities/gmm-budget.md |
| 为已给GMM块计算弹性和非线性度下界 | references/capabilities/gmm-budget.md | references/capabilities/prefix-partition.md、references/capabilities/mm-spectrum.md |
| 生成域乘法图码并核验不相交spread | references/capabilities/disjoint-codes.md | references/capabilities/ps-bent-labels.md、references/capabilities/vector-array.md |
| 寻找零谱平移基并转换为1阶弹性函数 | references/capabilities/zero-spectrum-transport.md | references/capabilities/vector-contract.md |
| 判定小维Bent函数正规性并剪枝陪集 | references/capabilities/normality-pruning.md | references/capabilities/vector-contract.md |
| 检查多输出指标契约、全部非零分量和参数可行性 | references/capabilities/vector-contract.md | references/capabilities/mm-spectrum.md、references/capabilities/corrector-layer-sums.md |
| 以spread和置换标签构造PS多输出Bent函数 | references/capabilities/ps-bent-labels.md | references/capabilities/disjoint-codes.md、references/capabilities/ps-recursive-balance.md |
| 在自由码递归嵌入函数以构造平衡多输出族 | references/capabilities/ps-recursive-balance.md | references/capabilities/ps-bent-labels.md |
| 在R_z=I子族内由AB置换及不相交支撑构造DS平衡半Bent函数 | references/capabilities/ds-semibent.md | references/capabilities/disjoint-codes.md、references/capabilities/vector-contract.md |
| 枚举并核验多输出阵列的单射/重量接口 | references/capabilities/vector-array.md | references/capabilities/disjoint-codes.md、references/capabilities/vector-contract.md |
| 将固定对齐的序列集相关转换成函数和的谱 | references/capabilities/sequence-spectrum.md | references/capabilities/vector-contract.md |
| 按重量层谱和判定独立同偏差输入的校正阶 | references/capabilities/corrector-layer-sums.md | references/capabilities/vector-contract.md、references/capabilities/double-code-corrector.md |
| 用两个不相交等距码构造高非线性多输出校正器 | references/capabilities/double-code-corrector.md | references/capabilities/corrector-layer-sums.md |

**非能力类查询**：
- 书名/作者/章节/整书概览 → references/overview.md
- 术语解释 → references/glossary.md
- 决策规则速查（不需要原文依据时） → references/cheatsheet.md
- 完整意图与关键词索引（本表未覆盖的意图先查这里） → references/capability-index.md

## 加载规则

- 每次任务先读本文件，再按路由表加载 **1** 张能力卡；任务明确跨域时最多加载 2 张。
- 概览/书名类问题不加载能力卡，用「核心原则」与 overview.md 回答。
- 路由表与 capability-index.md 都无法命中的意图，明确告知超出本书范围，不要硬套。

## 边界与判停

- 缺少域表示、输入表、核或合法参数时列出缺项；不静默填充。
- 若源式存在未隔离冲突、码距/单射/划分不满足或缺少极值证据，返回失败或仅报告已证下界。
- 超过资源声明的小参数计算上限时返回范围限制，并给出结构证明义务。
