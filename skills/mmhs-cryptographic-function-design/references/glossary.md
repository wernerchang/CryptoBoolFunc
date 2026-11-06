# 共享术语词典（阶段1提取，后续能力共用）

# 关键术语提取候选

日期2026-11-04。定义以原书为准；下列author_definition均为限定性转述，未加引号的内容不作逐字引文。数学上标统一还原；原文符号疑点单列，不静默替换。该词典为共享参考，不独立成skill。

```yaml
- id: g01
  term: Walsh变换/频谱
  type: term
  source_chapter: 2.1，定义2.4，p.55
  author_definition: W_f(a)=Σ_x(-1)^{f(x)+a·x}；按向量十进制顺序排列全部值形成有序频谱。
  key_distinction: 本书使用未归一化的整数谱；频谱分布只保留值与重数，频谱本身保留频率位置。
  why_it_matters: 非线性度、弹性、SAC相关恒等式与应用谱预算都依赖同一缩放及位序。
  tags: [term, spectral-normalization]

- id: g02
  term: 非线性度
  type: term
  source_chapter: 2.1，引理2.7，p.57；3.1定义3.5，p.169
  author_definition: 单输出为到全部仿射函数的最小汉明距离，等于2^{n-1}-max|W_f|/2；多输出取所有非零分量非线性度的最小值。
  key_distinction: 高次数不是高非线性度；多输出不能取坐标平均值或只看最佳坐标。
  why_it_matters: 构造验收需统一最坏分量及谱到距离的换算。
  tags: [term, nonlinearity]

- id: g03
  term: 平衡
  type: term
  source_chapter: 2.1引理2.5，p.55；3.1引理3.1，p.167
  author_definition: 单输出0、1各出现一半，等价W_f(0)=0；多输出每个m位输出出现2^{n-m}次，等价所有非零分量平衡。
  key_distinction: 所有坐标分别平衡仍不足以保证联合输出均匀；n=m时平衡就是置换。
  why_it_matters: 防止把逐坐标测试误当联合分布验证。
  tags: [term, balanced]

- id: g04
  term: 相关免疫/线性统计独立
  type: term
  source_chapter: 2.1，定理2.9，p.58
  author_definition: 输出与任意不超过t个输入变量的选择统计独立，对应1≤wt(a)≤t时W_f(a)=0。
  key_distinction: 不要求W_f(0)=0，故相关免疫不自动平衡。
  why_it_matters: 与弹性的差别恰为零频条件，不能遗漏。
  tags: [term, correlation-immunity]

- id: g05
  term: 弹性函数
  type: term
  source_chapter: 2.1定理2.10，p.58；3.1定义3.3及引理3.4，p.168—169
  author_definition: 平衡且t阶相关免疫；所有0≤wt(a)≤t处谱为0。多输出对每个c≠0的c·F均要求这一性质。
  key_distinction: t=0表示平衡；正阶弹性依赖输入坐标，通常不由任意可逆输入变换保持。
  why_it_matters: 目标t必须含零频，且在改变变量后重新验证低重量球。
  tags: [term, resilience]

- id: g06
  term: Plateaued/Bent/半Bent
  type: term
  source_chapter: 2.1定义2.12及相关定义，p.59；3.1，p.169—170
  author_definition: Plateaued具有固定非零幅值的三值Walsh谱；Bent在偶数n下全谱幅值2^{n/2}；本书半Bent的幅值随n奇偶分别为2^{(n+1)/2}或2^{n/2+1}。
  key_distinction: Bent通常不平衡；偶数维半Bent与奇数维半Bent幅值不同；多输出Bent要求所有非零分量为Bent且m≤n/2。
  why_it_matters: 不能把Bent直接当平衡核，也不能把奇数维公式照搬到偶数维。
  tags: [term, spectral-class]

- id: g07
  term: 几乎最优/严格几乎最优
  type: term
  source_chapter: 2.1；3.1式3.6，p.169
  author_definition: 按n奇偶，以2^{n-1}-2^{(n-1)/2}或2^{n-1}-2^{n/2}为非线性度阈值；达到阈值称几乎最优，严格超过称严格几乎最优。
  key_distinction: 这是书中专门阈值术语，不表示已证明全局最优，也不是工程上的笼统评价。
  why_it_matters: 参数表和比较结论必须按同一阈值解释。
  tags: [term, threshold]

- id: g08
  term: 正交谱函数集
  type: term
  source_chapter: 2.3定义2.30，p.69
  author_definition: 对任意频率a，不同函数的Walsh值逐点乘积为0。
  key_distinction: 意味非零谱支撑不相交，强于把两个频谱向量的普通内积要求为0；也不等同于序列正交。
  why_it_matters: 只有逐点排他性才能保证级联谱中至多一个块贡献。
  tags: [term, disjoint-spectrum]

- id: g09
  term: 部分线性函数
  type: term
  source_chapter: 2.3定义2.28，p.69
  author_definition: 将变量划成U、V，表示成c·U+h(V)，其中U是r维线性部分。
  key_distinction: 不是说整体函数为线性；非线性核在另一组互不重叠变量上。
  why_it_matters: 决定谱切片δ=c及弹性与核性质的组合方式。
  tags: [term, partially-linear]

- id: g10
  term: MM型/广义级联GMM
  type: term
  source_chapter: 2.2定义2.21，p.63；2.4定义2.41/2.43，p.81—83
  author_definition: MM以同尺寸仿射函数级联，f(Y,X)=φ(Y)·X+h(Y)；GMM允许在不同前缀柱状块上级联不同变元数的仿射函数。
  key_distinction: 广义级联本身可用任意布尔核，但书中GMM专指相应仿射零件结构；不同块尺寸要求显式划分。
  why_it_matters: 生成器不能只接收核列表而遗漏位置、长度、不重叠和全覆盖证书。
  tags: [term, MM, GMM]

- id: g11
  term: 残缺布尔函数/残缺Walsh变换
  type: term
  source_chapter: 2.6定义2.60、引理2.61/2.62，p.99—100
  author_definition: 仅在非空子集S上定义的函数f_S及FW(a)=Σ_{x∈S}(-1)^{f_S(x)+a·x}。
  key_distinction: 未定义位置不是补0；谱仍对整个n维频率空间取值。能量为2^n|S|。
  why_it_matters: 防止把缺失真值表位置当函数值0，导致局部谱和全谱相加错误。
  tags: [term, fragmentary-Walsh]

- id: g12
  term: 不相交码集合
  type: term
  source_chapter: 2.7，p.119—124
  author_definition: 一组线性码两两交集仅为零向量；常以(u,m,d)记码长、维数及最小距离要求。
  key_distinction: 线性码都含0，因此不是集合交为空；去零后才两两不交。书中M(u,m,d)容量是该构造方法的口径，非自动全局最大值。
  why_it_matters: 非零支撑的排他性和容量估计都依赖正确除零。
  tags: [term, disjoint-code]

- id: g13
  term: 自由码
  type: term
  source_chapter: 3.2，p.173
  author_definition: PS型spread中可在支撑中整体加入或去除、用于局部修改及递归嵌入的那一特殊码；本书可取{0^{n/2}}×F2^{n/2}。
  key_distinction: 不是任意不相交码都可随意改值；用途与PS型构造的支撑安排绑定。
  why_it_matters: 递归平衡计数及谱扰动界需要明确局部修改范围。
  tags: [term, free-code, PS]

- id: g14
  term: 多输出分量函数
  type: term
  source_chapter: 3.1，p.167—169
  author_definition: f_c=c·F，其中c为任意非零m位向量，包括坐标函数及它们的所有非零线性组合。
  key_distinction: 分量共2^m-1个；“坐标函数”仅m个，不能同义替换。
  why_it_matters: 平衡、弹性、Bent、非线性度及次数验收必须覆盖正确量词。
  tags: [term, vectorial-components]

- id: g15
  term: deg(F)与Deg(F)
  type: term
  source_chapter: 3.1定义3.5，p.169
  author_definition: deg(F)=min_{c≠0}deg(c·F)，Deg(F)=max_{c≠0}deg(c·F)。书中将前者简称代数次数。
  key_distinction: 一些其他文献/软件用最大坐标次数表示向量函数次数；本书小写deg是最坏分量最小次数。
  why_it_matters: 同一“次数”数字若口径不同，构造比较会失真；须同时报告min/max。
  tags: [term, degree-convention]

- id: g16
  term: 差分均匀度/PN/APN/AB
  type: term
  source_chapter: 3.1定义3.6，p.170
  author_definition: δ_F=max_{a≠0,b}#{x:F(x+a)+F(x)=b}；PN达到2^{n-m}；m=n时APN为δ=2；奇数维APN且具有规定非线性度者称AB。
  key_distinction: AB的谱性质和置换性要按构造需要分别检查；高非线性不自动低差分，平衡也不自动APN。
  why_it_matters: DS种子与S盒应用不能只以名称代替各项实际条件。
  tags: [term, differential, AB]

- id: g17
  term: 差分最大偏差/差分标准差
  type: term
  source_chapter: 3.1定义3.7，p.170
  author_definition: 以δ(a,b)相对2^{n-m}的最大绝对偏差及按全部a≠0、b平均的均方根偏差衡量差分分布。
  key_distinction: 记号δ(F)不是δ_F；标准差比较应固定n和m，不可跨不同维数直接排序。
  why_it_matters: 新型多输出函数的多指标比较需保留归一化分母与维数。
  tags: [term, differential-statistics]

- id: g18
  term: 正规Bent函数
  type: term
  source_chapter: 2.9，p.135—139
  author_definition: 在某个n/2维仿射子空间上取常值的n元Bent函数。
  key_distinction: 子空间上的平衡限制与常值限制不同；正规性不是非线性度等级，也非整个函数线性。
  why_it_matters: 算法2.91的剪枝依据为陪集能量耗尽，而非只看一个零点或一个平衡陪集。
  tags: [term, normality]

- id: g19
  term: SAC/PC(k)/自相关
  type: term
  source_chapter: 2.1定义2.16，p.61
  author_definition: C_f(a)=Σ_x(-1)^{f(x)+f(x+a)}；1≤wt(a)≤k时均为0称PC(k)，k=1为SAC。
  key_distinction: SAC只要求单位差分，不意味着所有非零差分均平衡，也不由三值谱自动推出。
  why_it_matters: MM互补配对条件与单射条件负责不同结论，测试应分开。
  tags: [term, SAC, autocorrelation]

- id: g20
  term: 正交序列集/互相关
  type: term
  source_chapter: 4.1，p.220—226
  author_definition: 布尔函数以(-1)^f对应±1序列；集内不同序列内积0称正交；集合间相关按相应序列内积绝对值的最大值度量。
  key_distinction: 谱支撑不相交与序列正交为不同条件；本节对齐内积不自动给出任意时移的相关性质。
  why_it_matters: 从Walsh谱转工程序列时必须确认相关定义和对齐/时移要求。
  tags: [term, orthogonal-sequence]

- id: g21
  term: 校正器/校正阶
  type: term
  source_chapter: 4.4定义4.24，引理4.25/4.26，p.257—258
  author_definition: 在输入独立且同偏差e的模型下，平衡函数输出偏差Δ_f(e)的最低非零次幂至少t+1时称t阶校正器；等价每个0至t重量层Walsh和为0。
  key_distinction: 与t阶弹性的逐点谱零条件不同；“是t阶”通常是至少t，不意味着恰为t；不能推广为任意有偏/相关源的通用提取器。
  why_it_matters: 需要检验层和、全部非零输出组合及源模型，避免重复父任务初版的恰阶断言错误。
  tags: [term, corrector, source-model]

- id: g22
  term: 等距码
  type: term
  source_chapter: 4.4定义4.31，p.260
  author_definition: "[u,m,t]线性码的每一个非零码字的汉明重量都恰为t。"
  key_distinction: 最小距离至少t的普通码不能代替等距码；双码校正器还要求两码交集仅零。
  why_it_matters: 同重量层的符号抵消依赖全部系数恰处同一层，而非仅有重量下界。
  tags: [term, equidistant-code]

- id: g23
  term: AI/FAI
  type: term
  source_chapter: 2.1定义2.15及后续讨论，p.60—61；3.1定义3.5，p.169
  author_definition: AI取f或f+1的非零零化子最小次数；FAI涉及寻找低次数g与h使fg=h并控制次数和；多输出AI取所有非零分量的最小值。
  key_distinction: 高次数只给AI的必要空间，不证明AI最优；FAI还需固定g、h非零及deg(g)范围，不能只用次数和值比较代替定义检查。
  why_it_matters: 不能依据MM/GMM名称或高非线性推断抗代数攻击性质；AI/FAI计算须单独验证。
  tags: [term, algebraic-immunity]
```

## 符号校勘与使用规则

- p.257在Pr(x_i=0)=1/2+e及Δ=(P0-P1)/2约定下，引理4.23的印刷符号与Walsh反演冲突；使用父任务已重建的正号系数展开，保留原版本疑点。每层乘以非零符号不改变零和判据。
- 编码实现必须保存位序、GF基、谱顺序、矩阵行向量约定；脚本输出不得仅写“按通常约定”。
- 未检索外部文献更新，本词典仅澄清本书用法，不将书中现状描述升级为2026年现状。
