# 精确小参数工具输入约定

仅依赖Python标准库，建议Python 3.10+。执行 `python math_tool.py COMMAND --input input.json --output result.json`。成功退出0、非法条件或缺项退出2并返回JSON错误；输出父目录须已存在。脚本不访问网络、不修改输入文件。首次执行前阅读脚本和卡中条件。

真值表按整数x递增，输入bit i=(x>>i)&1。标量table是0/1数组；多输出整数bit i表示第i输出分量。m≤6、完整表n≤12是资源限制，不是数学定理的维数限制。谱用未归一化整数Walsh；非线性度取所有非零分量最小值。degree=最小分量次数，另报max_degree。resilience=-1表示不平衡；corrector_order仅适用于独立同偏差模型，报告的是该实例实际最小阶。

## 命令输入

| 命令 | 必需JSON字段 | 说明 |
|---|---|---|
| inspect | table；多输出加m | 每分量ANF、完整谱、层和、SAC等；不计算AI/FAI或DDT |
| mm | k,phi；可选h,require_sac | phi数组长度是选择器空间大小，须单射；SAC模式要求像互补闭合；h默认为零 |
| prefix | n,layers:[{u,count}] | u自由变量数；按大到小构造连续对齐柱状块，必须恰好覆盖 |
| gmm | n,t,blocks:[{u,prefix,coefficient,constant?}] | 同层系数不重复且重量>t；块完整不交；常数默认为0 |
| codes | k,poly | 生成GF(2^k)图码spread及自由码；k≤4；poly整数表示二进制多项式 |
| ps | mode,m；bent模式:k,poly；recursive模式:seed,polys | bent模式输出低m位标签；recursive每次输入维数翻倍，seed须置换且满足原构造非线性度阈值 |
| ds | k,s,seed,poly | 奇数k≥3，s≥k，n=2s+k≤12；seed为AB置换；本工具使用R_z=I子族 |
| d-array | u,m,t,poly | 使用前m个连续幂列、固定多项式基；u≤10，m≤6；逐行检查全部非零组合 |
| zero-transport | table | 遍历零谱δ寻找平移零谱完整基，输出R和变换表；失败报告no_full_basis |
| normality | table | 仅偶数n≤6且Bent；去重span枚举与陪集剪枝，非特定GJB实现 |
| sequence | f,g；可选a,b标签数组 | 默认标签[0]；最多4096对固定对齐相关，不计算循环移位 |
| corrector | m,u,poly,basis1,basis2 | 两组m个u位基向量；两码满秩、不相交且非零字等重量；m+u≤12 |

poly如11表示x³+x+1，67表示x⁶+x+1，37表示x⁵+x²+1，47表示x⁵+x³+x²+x+1。工具会核验x的乘法阶；不能用任意不可约多项式替代本原元证书。

## 示例

MM输入：`{"k":3,"phi":[3,4],"h":[1,0],"require_sac":true}`。

PS递归输入：`{"mode":"recursive","m":3,"seed":[0,1,3,4,5,6,7,2],"polys":[11,67]}`。

DS输入：`{"k":3,"s":3,"seed":[0,1,3,4,5,6,7,2],"poly":11}`。

双码校正器输入：`{"m":3,"u":7,"poly":11,"basis1":[116,58,29],"basis2":[23,46,92]}`。此处选择器y_i从整数[Y]的高位到低位读取，而输出i存整数bit i；此约定须与卡中向量式一致。

通用工具不把HML、DC一般存在性、FAI求解或混合阵列精确界设为命令。相关失败记录和来源校勘应随研究结果保留。具体研究问题允许使用更大参数实现，但不能将本工具有限实例当作一般证明。
