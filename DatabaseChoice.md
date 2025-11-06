# 图划分（Graph Partitioning）— 数据集取舍

**优先纳入（强烈建议作为核心）：**

* **DIMACS10**：领域黄金标准、类型多、规模梯度自然，最适合做你要的“从小到大综合数据集”的骨架；易于转成统一`.txt`边表/邻接格式并在头部写明`k`与平衡因子。✅ 推荐作为训练/验证/测试三套的共同基线。
* **SNAP（精选子集）**：真实网络（社交/引文/道路等），补足“真实分布”场景；需要统一为无向/去重并补充`weighted=0/1`等头部字段。✅ 建议挑选中小图 + 若干大图做泛化/鲁棒性验证。
* **SuiteSparse（精选子集）**：来自稀疏矩阵的结构图，能检验在数值模拟/HPC风格图上的稳定性；注意从矩阵到图的规则（对称化、去自环）。✅ 以“小-中-大”三档做补充。

**可以纳入（作为扩展/合成来源）：**

* **Graph-Partitioning-Benchmark**：含合成器与若干真实图，利于你统一生成不同规模与分布的实例，补齐“参数可控”的训练集。🟨 作为补充训练/消融数据源。
* **OGB（少量大图做压力/泛化测试）**：超大规模，更像“应力测试”；不宜一开始全量收录。🟨 选1–2个数据集（如`ogbn-arxiv/products`）放到“Large”桶即可。

**暂缓/不纳入（避免无效工作）：**

* **HypergraphPartitioning（ISPD98/Titan23）**：这是**超图**划分基准；若你的本期目标是**图**划分，强行用clique/star等投影会改变目标与分布，评测含义也不再一致。❌ 本轮先不做；若后续要扩展到**超图划分模块**，再单独建一个轨道。

# 数值划分（Number Partitioning）— 数据集取舍

**优先纳入（核心）：**

* **Pedroso & Kubo 实例集（easy/hard）**：少见的“难度分相”标准基准，非常适合做从易到难的综合数据集主干；统一成`.txt`时注意原始位数/进制与数值范围，头部写`k`、`n_numbers`、`range`与`distribution`。✅ 强烈建议。

**作为生成规则/补充来源：**

* **Mertens (2003) 相变理论**：不是数据集，但直接指导你**在临界区间**程序化生成“最难”的实例，用于验证RL/启发式的上限表现。🟨 用来设计生成器参数，不作为静态基准直接纳入。
* **Tracer NPP 生成思路**：同样更像说明/脚手架。🟨 建议实现你自己的生成器（可控`k`、数量级、分布、是否有重复），产出的**合成样本**再进入统一流程。

> 结论：NPP的综合数据集= **Pedroso&Kubo（核心） + 你自建合成器（按easy/critical/hard段落分布）**。避免把“说明页/论文”本身当作可下载数据源处理。

# 图着色（Graph Coloring）— 数据集取舍

**优先纳入（核心）：**

* **DIMACS & COLOR02/03/04**：权威与使用最广的基准，覆盖随机/几何/寄存器分配等多图族，规模层次清晰。✅ 作为主干最合适；统一为边表`.txt`，头部可含`known_chi`（若有）、`class=DSJC/…`。

**可以纳入（增广，但要去重）：**

* **ROARS Graph Coloring Instances**：便于使用、但与DIMACS存在交集。🟨 作为增广来源时要**去重**（以文件名/图统计签名判重）。
* **graph_colouring_with_RL（GitHub 仓库数据）**：更偏“研究代码随附样本”，规模多为小中图。🟨 可做训练/预热集，不建议当主评测基准。

**暂缓/不纳入（避免重复）：**

* **Network Repository 的 DIMACS 子集**：主要是**聚合/镜像**，与上面核心集重复。❌ 当前无需单独纳入，除非用于补缺文件。

---

# 统一格式与处理要点（避免返工）

* **头部元信息建议**（模仿RLSolver思路）：

  * `problem=GP|NPP|GC`，`n`，`m`，`k`，`weighted=0/1`，`directed=0/1`，`objective=mincut|ncut|makespan|min_colors`，`balance_nu`（GP）、`known_chi`（GC, 可选）、`n_numbers`/`range`/`distribution`（NPP）。
* **内容体**：

  * **GP/GC**：无向边表（1-index或0-index固定一种），可选权重列；
  * **NPP**：首行`k`与`n_numbers`后跟一列/多列的元素值（十进制统一）。
* **去重与分桶**：对GC（DIMACS/ROARS）做重叠检测；三问题都按**Small/Medium/Large**分桶，确保每桶有真实/合成/结构化三类的覆盖。
* **异常与转换**：GP中需**对SNAP/OGB做无向化与去自环**；SuiteSparse从矩阵到图需统一对称化规则；NPP注意大整数精度（统一为Python `int`范围的十进制文本）。

---

# 公认RL算法（精简清单，便于你立刻对齐baseline）

**图划分（GP）：**

* **GNN-A2C（JMLR 2022, Gatti et al.）**：多级框架+RL优化（GraphSAGE做A/C）；可替代贪心后处理。
* **Revolver（IEEE CLOUD 2018）**：顶点级多智能体+标签传播指导，天然并行。
* **NeuroCUT（2023）**：GNN+RL，支持任意k路与非可微目标。
* **PR-GPT（2024）**：小图预训练+大图归纳推断，加速划分。

**数值划分（NPP）：**

* 静态NPP专向RL较少；常用**REINFORCE/PPO或DQN**把“当前最大数放入哪个桶”建模为顺序决策；可参考**Neural Combinatorial Optimization with RL（2017）**等通用框架。

**图着色（GC）：**

* **ReLCol（2023）**：DQN+GNN学习**顶点选择顺序**，再用First-Fit上色。
* **LOMAC（ICLR 2024）**：状态空间重构到O(N²)，可扩至大图；伪结点GNN+势能奖励。
* 还有MCTS+DRL、DL引导模因框架等混合型方法可做扩展对照。

---

## 一键执行清单（避免无用功）

1. **GP**：先做 **DIMACS10+SNAP(精选)+SuiteSparse(精选)** 的统一转换；生成一批 **Graph-Partitioning-Benchmark** 合成图补充“规模梯度”。
2. **NPP**：统一 **Pedroso&Kubo**；并按**Mertens临界区**写生成器，产出easy/critical/hard三段合成样本。
3. **GC**：主干用 **DIMACS/COLOR**；用 **ROARS** 做增广但先去重；GitHub样本仅作训练预热集，不进主评测。
4. **写统一loader**：先支持上述“核心三套”，通过后再接入“可选/扩展”。