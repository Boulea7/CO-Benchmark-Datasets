# 一、执行摘要（保留关键要点）

* **格式基线**：遵循 RLSolver 图实例格式——首行 `n m`，其后每行 `u v w`（无向图、1-based、合成图 `w=1`）作为**硬标准**；我们在其上加**可选头部（注释行）**，既便于统一元信息，又不破坏兼容性（加载器忽略以 `#` 开头行）([rlsolver-competition.readthedocs.io][1])。
* **三套“综合数据集”建议**：

  * **Graph Partitioning（图划分）**：主力用 **DIMACS10**（含 Walshaw 集）+ 真实网络 **SNAP** +（可选）**SuiteSparse** 的图派生边集；必要时补充 **GSET**（与 Max-Cut 同族）以做交叉验证。都应纳入，体量跨度大、来源权威、复用广。([sites.cc.gatech.edu][2])
  * **Graph Coloring（图着色）**：以 **DIMACS/COLOR 实例（.col 标准）** 为主，辅以 **ROARS/npbench** 和社区集合（gc_instances）。这三路都建议纳入，覆盖经典难例与现代整理版。([mat.tepper.cmu.edu][3])
  * **Number Partitioning（数值划分）**：以 **Pedroso & Kubo** 的 easy/hard 系列为锚，再按 **Mertens** 相变设定自建随机实例做尺度扩展。两者都应纳入（易/难梯度 + 可控规模）。([dcc.fc.up.pt][4])
* **RL 算法基线（按问题归类）**：

  * **图划分 / Max-Cut 家族**：S2V-DQN（Dai+2017）、ECO-DQN（Barrett+2019/AAAI’20 DLG）、近年 A2C 分治划分（JMLR 2022）、NeuroCUT（KDD’24）作为主线参考；RLSolver 自带方法页也将 ECO/S2V/MCPG/iSCO 作为内置流派。建议把 S2V-DQN 与 ECO-DQN 作为首批对标基线。([arxiv.org][5])
  * **图着色**：近期可复现的 RL 代表有 **ReLCol**（DQN+GNN，2023）与 **LOMAC**（ICLR 2024）。建议二者入选对标基线（小中型图验证）。([arxiv.org][6])
  * **数值划分**：可将 NPP 写成 QUBO/Ising，再用**RL-MCMC/Policy Gradient**等范式；RLSolver 竞赛任务 2 明确给出 **“Ising + RL-MCMC”** 方向，可直接复用思路做 NPP 的 RL 基线原型。([github.com][7])

> 结论：**上述所有来源都值得进入下一步的下载与统一处理**。唯一需要控制的是**规模配比与去重**（避免同图/同实例以不同格式重复）。

---

# 二、统一数据规范（RLSolver 风格 + 头部）

> 目标：**一个 `.txt` 统一读取**；图类完全兼容 RLSolver，数值划分与着色也沿用“首行规模 + 条目行”的极简风格。

## 2.1 头部（可选，注释行，加载器忽略）

```
# problem: graph_partitioning | graph_coloring | number_partitioning
# name: DIMACS10/walshaw/4elt | COLOR/queen5_5 | PK/easy_n100_01
# n: <nodes or numbers>      # 对图=节点数；对NPP=元素个数
# m: <edges>                 # 仅图类
# k: <partitions or colors>  # 可留空或0（未知），训练时可作hint/目标
# weighted: 0|1              # 图边是否有权
# directed: 0|1              # 图是否有向（建议0）
```

## 2.2 图划分 / 着色（Graph类）

* **文件体**：严格遵循 RLSolver 图实例：

  * 第 1 行：`n m`
  * 第 2 行起：`u v w`（1-based；无向；若无权则 `w=1`）([rlsolver-competition.readthedocs.io][1])
* **示例（graph_partitioning）**：

```
# problem: graph_partitioning
# name: DIMACS10/walshaw/4elt
# n: 15606
# m: 45878
# k: 2
15606 45878
1 2 1
1 3 1
...
```

* **示例（graph_coloring）**（由 .col 转换而来）：

```
# problem: graph_coloring
# name: COLOR/queen5_5
# n: 25
# m: 320
# k: 0
25 320
1 2 1
1 6 1
...
```

> 说明：.col 为 DIMACS 标准（`p edge n m` + `e u v`），转换时去掉 `p/e` 语句，合并为 RLSolver 体裁（三元组权重置 1）([mat.tepper.cmu.edu][3])。

## 2.3 数值划分（NPP）

* **文件体**：

  * 第 1 行：`n`（元素个数）
  * 第 2 行起：每行一个正整数权值（或空格分隔的一行 n 个数，加载器两种都支持）
* **示例**：

```
# problem: number_partitioning
# name: PK/easy_n100_01
# n: 100
# k: 2
100
13749
932
...
```

> 来源包含 Pedroso & Kubo 的 easy/hard 系列；我们再按 Mertens 相变比值生成随机实例补齐规模带。([dcc.fc.up.pt][4])

---

# 三、推荐数据源清单（并标注是否纳入综合集）

## 3.1 Graph Partitioning

* **DIMACS10（含 Walshaw）**：经典划分基准，规模跨度大，强烈建议纳入为**主干**；原始格式需转成 `n m + (u v w)`。([sites.cc.gatech.edu][2])
* **SNAP**：真实网络（社交/通信/引文等），补充非合成图的泛化能力，建议纳入。([snap.stanford.edu][8])
* **SuiteSparse**：由稀疏矩阵派生图（对称模式当无向图），建议纳入**子集**（注意去重与连通性）。([sparse.tamu.edu][9])
* **GSET（Max-Cut）**：与“割/划分”同族，做交叉验证/消融可选。见 RLSolver 数据页。([rlsolvers.readthedocs.io][10])

## 3.2 Graph Coloring

* **DIMACS/COLOR .col**：**主干**，标准格式、难例集中。([mat.tepper.cmu.edu][3])
* **ROARS/npbench（Graph Coloring）** 与 **gc_instances**：现代整理，含加权/规约版本，建议纳入作**扩展难例**。([roars.dev][11])

## 3.3 Number Partitioning

* **Pedroso & Kubo**：提供 easy/hard 基准与程序，**必纳**。([dcc.fc.up.pt][4])
* **随机实例生成（Mertens 相变）**：控制 `m/n` 比例以覆盖易/难段，**建议纳入**。([link.aps.org][12])

---

# 四、RL 基线与论文指引（按问题）

* **图划分 / Max-Cut 系**

  * **S2V-DQN**（Dai et al., 2017）——图嵌入 + DQN 的里程碑，覆盖 MVC/Max-Cut 等。([arxiv.org][5])
  * **ECO-DQN**（Barrett et al., 2019/AAAI’20 workshop）——在 Max-Cut 上提升显著，可与 S2V-DQN 对标。([arxiv.org][13])
  * **A2C 递归划分（JMLR 2022）**——提出 RL+GNN 的多级递归划分，和 METIS/SCOTCH 对比；实证基线很有参考价值。([jmlr.org][14])
  * **NeuroCUT（KDD’24）**——自回归 GNN+RL，适配多目标与任意 K，值得作为现代强基线。([arxiv.org][15])
  * **RLSolver 方法页**：收录 ECO-DQN、S2V-DQN、MCPG、iSCO、Jumanji 等范式。([rlsolvers.readthedocs.io][16])

* **图着色**

  * **ReLCol（2023）**——DQN+GNN 生成式启发式。([arxiv.org][6])
  * **LOMAC（ICLR 2024）**——面向大图的 DRL 框架，可选为进阶基线。([OpenReview][17])

* **数值划分（NPP）**

  * **Ising/QUBO + RL-MCMC 路线**：RLSolver 竞赛 Task2 明确此范式，可直接迁移到 NPP。([github.com][7])

---

# 五、目录与分割建议（train/val/test）

```
datasets/
  graph_partitioning/
    dimacs10/...   # 统一为 .txt (n m + edges)
    snap/...
    suitesparse/...
    gset/...
  graph_coloring/
    color_dimacs/...
    roars/...
    gc_instances/...
  number_partitioning/
    pedroso_kubo/
      easy/...     # 原始 -> 统一 .txt
      hard/...
    random_mertens/...
splits/
  graph_partitioning/{train.txt,val.txt,test.txt}
  graph_coloring/{train.txt,val.txt,test.txt}
  number_partitioning/{train.txt,val.txt,test.txt}
```

* **划分规则**：按规模与来源**分层分布式抽样**（小/中/大；合成/真实），避免“训练仅合成、测试全真实”的域偏移。DIMACS10/SNAP/SuiteSparse 等建议各自留出测试份额。([sites.cc.gatech.edu][2])

---

# 六、通用加载器（最小可用骨架）

> 兼容：跳过 `#` 头部；图类读取 `n m` + 三元组（1-based→0-based）；NPP 读取 `n` + n 个整数（逐行或一行）。

```python
from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterator
import io

Header = dict[str, str]

def _iter_lines(fp: io.TextIOBase) -> Iterator[str]:
    for line in fp:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        yield line

def parse_header(raw: str) -> Header:
    h: Header = {}
    for ln in raw.splitlines():
        if ln.startswith("#"):
            kv = ln[1:].strip().split(":", 1)
            if len(kv) == 2:
                h[kv[0].strip().lower()] = kv[1].strip()
    return h

@dataclass
class GraphInstance:
    name: str
    n: int
    m: int
    edges: List[Tuple[int,int,int]]  # 0-based, (u,v,w)
    meta: Header

def load_graph_txt(path: str) -> GraphInstance:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    meta = parse_header(raw)
    f = io.StringIO(raw)
    lines = list(_iter_lines(f))
    # first non-comment line: "n m"
    n, m = map(int, lines[0].split()[:2])
    edges = []
    for ln in lines[1:]:
        u, v, *rest = ln.split()
        w = int(rest[0]) if rest else 1
        # 1-based -> 0-based
        u = int(u) - 1
        v = int(v) - 1
        if u == v:  # 防自环
            continue
        if u > v:   # 规范化无向边顺序
            u, v = v, u
        edges.append((u, v, w))
    # 去重
    edges = list({(u, v): (u, v, w) for (u, v, w) in edges}.values())
    return GraphInstance(meta.get("name", path), n, len(edges), edges, meta)

@dataclass
class NPPInstance:
    name: str
    n: int
    values: List[int]
    meta: Header

def load_npp_txt(path: str) -> NPPInstance:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    meta = parse_header(raw)
    f = io.StringIO(raw)
    it = _iter_lines(f)
    n = int(next(it))
    # 兼容逐行或单行
    vals: List[int] = []
    for ln in it:
        parts = ln.split()
        vals.extend(map(int, parts))
        if len(vals) >= n:
            break
    vals = vals[:n]
    return NPPInstance(meta.get("name", path), n, vals, meta)
```

---

# 七、数据清洗与自动校验清单（强烈建议脚本化）

* **图类**：

  * 1-based→0-based、去重、去自环、强制无向（规范 `min(u,v),max(u,v)`）；**核对首行 m** 与实际边数一致。
  * 若源为矩阵（SuiteSparse），用**结构对称模式**抽边（忽略值，权置 1）；检查连通分量分布。([sparse.tamu.edu][9])
* **.col→RLSolver**：识别 `p edge n m` 与 `e u v`，映射为 `n m` + `(u v 1)`。([mat.tepper.cmu.edu][3])
* **NPP**：剔除非正整数、去重与排序可选；对自建随机实例，按 **Mertens** 相变区间采样（覆盖易/难）。([link.aps.org][12])

---

# 八、依赖裁剪与代码重构建议（贴合你计划）

* **最小依赖集合**：`python>=3.10`, `numpy`, （图相关如需基准转换时用 `networkx` 仅限数据预处理脚本），训练侧只保留 `torch` + 你要跑的 RL 实现。
* **ECO / S2V 最小 MVP**：优先实现**数据管线 + 单环境 + 单策略**的可跑版本（对 Max-Cut/Partition 家族），随后再扩展到 Coloring/NPP。RLSolver 方法页与竞赛资料可作接口风格参考。([rlsolvers.readthedocs.io][16])

---

# 九、下一步落地清单（可以直接执行）

1. **下载与转格式**：按上表三类来源批量拉取 → 统一转为本文规范；生成 `splits/*.txt`。
2. **跑校验脚本**：完成规模、边数、连通性、重复检查；NPP 检查取值范围与难度带分布。
3. **基线跑通**：先在**小/中尺度**上用 **S2V-DQN / ECO-DQN** 对 Max-Cut/划分类跑通，之后对 Coloring（ReLCol/LOMAC）与 NPP（Ising+RL-MCMC）补齐。([arxiv.org][5])

---

## 参考来源（关键）

* **RLSolver 格式与方法**：Graph Instance 文件格式与示例；方法综述页（ECO/S2V/MCPG/iSCO/Jumanji）。([rlsolver-competition.readthedocs.io][1])
* **数据源**：DIMACS10（含 Walshaw）、SNAP、SuiteSparse、COLOR（DIMACS .col）、ROARS/npbench、gc_instances。([sites.cc.gatech.edu][2])
* **NPP 基准与相变**：Pedroso & Kubo 数据与说明；Mertens 相变工作。([dcc.fc.up.pt][4])
* **RL 论文**：S2V-DQN（2017）、ECO-DQN（2019/AAAI20）、JMLR’22 A2C 划分、NeuroCUT（KDD’24）、ReLCol（2023）、LOMAC（ICLR’24）。([arxiv.org][5])

[1]: https://rlsolver-competition.readthedocs.io/en/latest/rlsolver_contest_2025/graph_instance.html "Graph Instance — RLSolver Contest Documentation 1.0 documentation"
[2]: https://sites.cc.gatech.edu/dimacs10/downloads.shtml?utm_source=chatgpt.com "10th DIMACS Implementation Challenge - gatech.edu"
[3]: https://mat.tepper.cmu.edu/COLOR/instances.html?utm_source=chatgpt.com "Graph Coloring Instances - Carnegie Mellon University"
[4]: https://www.dcc.fc.up.pt/~jpp/partition/readme.html?utm_source=chatgpt.com "Tree search for the Number Partitioning Problem"
[5]: https://arxiv.org/abs/1704.01665?utm_source=chatgpt.com "Learning Combinatorial Optimization Algorithms over Graphs"
[6]: https://arxiv.org/abs/2304.04051?utm_source=chatgpt.com "Generating a Graph Colouring Heuristic with Deep Q-Learning and Graph Neural Networks"
[7]: https://github.com/Open-Finance-Lab/RLSolver_Contest_2025 "GitHub - Open-Finance-Lab/RLSolver_Contest_2025"
[8]: https://snap.stanford.edu/data/?utm_source=chatgpt.com "Stanford Large Network Dataset Collection"
[9]: https://sparse.tamu.edu/?utm_source=chatgpt.com "SuiteSparse Matrix Collection"
[10]: https://rlsolvers.readthedocs.io/Datasets/graph.html "Graph Datasets — RLSolver 0.0.1 documentation"
[11]: https://roars.dev/npbench/graphcoloring.html?utm_source=chatgpt.com "Graph Coloring Benchmark Instances - GitHub Pages"
[12]: https://link.aps.org/doi/10.1103/PhysRevLett.81.4281?utm_source=chatgpt.com "Phase Transition in the Number Partitioning Problem"
[13]: https://arxiv.org/abs/1909.04063?utm_source=chatgpt.com "Exploratory Combinatorial Optimization with Reinforcement Learning"
[14]: https://jmlr.org/papers/volume23/21-0644/21-0644.pdf?utm_source=chatgpt.com "Graph Partitioning and Sparse Matrix Ordering using Reinforcement ..."
[15]: https://arxiv.org/pdf/2310.11787?utm_source=chatgpt.com "NeuroCUT: A Neural Approach for Robust Graph Partitioning"
[16]: https://rlsolvers.readthedocs.io/Methods/RL_methods.html "RL Methods — RLSolver 0.0.1 documentation"
[17]: https://openreview.net/forum?id=yG2WrLenxd&utm_source=chatgpt.com "LOMAC: GNN-based Deep Reinforcement Learning with One-Way Markov..."
