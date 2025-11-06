<div align="center">

# 🚀 CO-Benchmark-Datasets

**Comprehensive Benchmark Datasets for Reinforcement Learning in Combinatorial Optimization**

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/Boulea7/CO-Benchmark-Datasets)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Issues](https://img.shields.io/github/issues/Boulea7/CO-Benchmark-Datasets)](https://github.com/Boulea7/CO-Benchmark-Datasets/issues)
[![Size](https://img.shields.io/github/repo-size/Boulea7/CO-Benchmark-Datasets)](https://github.com/Boulea7/CO-Benchmark-Datasets)
[![Dataset Size](https://img.shields.io/badge/datasets-447%20files-orange.svg)]()

## 🎯 Research Focus: NP-Hard Combinatorial Optimization Problems

**Specialized benchmark datasets for advancing reinforcement learning algorithms in classical NP-Hard problems**

</div>

---

## 📋 Abstract

This repository provides a comprehensive collection of standardized, high-quality benchmark datasets specifically designed for evaluating reinforcement learning algorithms on classical combinatorial optimization problems. Our benchmark suite focuses on three fundamental NP-Hard problems that serve as critical testbeds for algorithmic innovation:

- 🔄 **Graph Partitioning** - Minimize cut edges while maintaining balance constraints
- 🎨 **Graph Coloring** - Minimize chromatic number while avoiding adjacent conflicts
- 🔢 **Number Partitioning** - Balance subset assignments to minimize maximum completion time

These datasets are meticulously curated from multiple authoritative sources, processed into unified formats, and optimized for machine learning workflows, providing the research community with essential tools for developing and evaluating next-generation RL algorithms.

## 📋 问题定义与数学建模

### 图划分 (Graph Partitioning)
**问题定义**: 将图 $G = (V, E)$ 的顶点集 $V$ 分割成 $k$ 个互不相交的子集 $V_1, V_2, \dots, V_k$

**核心目标**:
- **最小化切割边**: 最小化连接不同划分的边的数量或总权重
- **平衡约束**: 要求每个划分的大小相近，确保工作负载均衡

**归一化切割公式**:
$$\text{NCut}(A, B) = \frac{\text{cut}(A, B)}{\text{vol}(A)} + \frac{\text{cut}(A, B)}{\text{vol}(B)}$$

### 图着色 (Graph Coloring)
**问题定义**: 为图 $G=(V, E)$ 的每个顶点分配颜色，使得相邻顶点具有不同颜色

**主要目标**: 最小化所使用颜色的总数，即图的**色数** $\chi(G)$

**等价表述**: 将顶点集 $V$ 划分为最少数目的**独立集**

### 数值划分 (Number Partitioning)
**问题定义**: 将正整数多重集 $S$ 分割成 $k$ 个子集 $S_1, S_2, \dots, S_k$

**优化目标**: 最小化**最大完工时间**
$$\min \left( \max_{i=1, \dots, k} \sum_{x \in S_i} x \right)$$

**等价问题**: 并行机调度问题，目标是最小化所有任务完成的总时间

## 📚 Table of Contents

- [Abstract](#-abstract)
- [问题定义与数学建模](#-问题定义与数学建模)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Dataset Overview](#-dataset-overview)
- [Algorithm Baselines](#-algorithm-baselines)
- [Data Sources](#-data-sources)
- [Usage Guidelines](#-usage-guidelines)
- [Performance Benchmarks](#-performance-benchmarks)
- [Repository Structure](#-repository-structure)
- [Code Standards](#-代码规范)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## ✨ Key Features

### 🔧 **Technical Excellence**
- **Unified Format Standard**: All datasets converted to consistent text format following RLSolver competition specifications
- **Scalable Size Classification**: Systematic categorization (tiny/small/medium/large/xlarge) for progressive algorithm development
- **High Compression Ratio**: Average 88.9% compression efficiency while maintaining data integrity
- **Rich Metadata Infrastructure**: Comprehensive problem specifications, source provenance, and difficulty annotations

### 🚀 **ML-Ready Infrastructure**
- **Automated Data Loading**: Intelligent loaders with format detection and preprocessing capabilities
- **LFS Integration**: Git Large File Storage support for efficient version control of large datasets
- **Batch Processing Support**: Optimized for training pipelines with parallel loading capabilities
- **Cross-Platform Compatibility**: Python 3.8+ support with minimal dependencies

### 📊 **Research-Grade Quality**
- **Multiple Authoritative Sources**: Datasets from DIMACS challenges, academic benchmarks, and real-world networks
- **Balanced Problem Distribution**: Careful selection across difficulty spectra and structural characteristics
- **Reproducible Results**: Deterministic loading and processing ensuring experimental consistency

## 📁 项目结构

```
CO-Benchmark-Datasets/
├── processed/                      # 处理后的数据集
│   ├── graph_partitioning/        # 图划分数据
│   ├── graph_coloring/            # 图着色数据
│   └── number_partitioning/       # 数值划分数据
├── scripts/                       # 数据处理脚本
│   ├── unified_loader.py          # 统一数据加载器（推荐使用）
│   ├── compress_datasets_parallel.py  # 并行压缩脚本
│   └── example_usage.py           # 使用示例脚本
└── README.md                      # 项目说明文档
```

## 🚀 快速开始

### 推荐方法：统一数据加载器

```python
from scripts.unified_loader import load_graph_txt, load_npp_txt, load_instance

# 加载图数据（自动处理索引转换、去重和去自环）
graph = load_graph_txt('processed/graph_partitioning/compressed/tiny/dolphins.txt.xz')

# 加载数值划分数据
numbers = load_npp_txt('processed/number_partitioning/compressed/small/n025d12e00.txt.xz')

# 自动识别并加载任何类型的数据集
instance = load_instance('processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz')
```

### 命令行使用

```bash
# 使用统一加载器加载并显示数据信息
python3 scripts/unified_loader.py processed/graph_partitioning/compressed/tiny/dolphins.txt.xz --verbose

# 运行完整的使用示例
python3 scripts/example_usage.py
```

## 📊 数据集概览

| 问题类型 | 数据集数量 | 压缩比 | 规模分类 |
|----------|------------|--------|------------|
| 图划分 | 69 | 98.4% | tiny/small/medium/large/xlarge |
| 图着色 | 79 | 82.9% | tiny/small |
| 数值划分 | 300 | 83.3% | tiny/small/medium/large |

## 🤖 算法基准

### 图划分 (Graph Partitioning)

#### 核心算法
- **[GNN-A2C 多级优化方法](https://www.jmlr.org/papers/volume23/21-0644/21-0644.pdf)** (JMLR 2022)
  - 结合经典多级框架和A2C算法，使用GraphSAGE GNN进行局部优化
  - MDP建模：状态通过GNN编码，动作选择边界节点移动，奖励与NCut改善相关

- **[Revolver](https://arxiv.org/abs/1907.06768)** (IEEE CLOUD 2018)
  - 去中心化的多智能体方法，每个顶点作为独立智能体
  - 基于Learning Automaton和标签传播的并行框架

#### 前沿算法
- **[NeuroCUT](https://arxiv.org/abs/2310.11787)** (2023)
  - 支持任意k路划分和非可微目标的GNN+RL框架
  - 参数空间与划分数量解耦，可泛化到未见过的划分数量

- **[PR-GPT](https://arxiv.org/abs/2409.00670)** (2024)
  - 预训练-微调范式，在小图上预训练，通过归纳推理快速泛化到大规模图

- **[Graph RL Survey](https://arxiv.org/html/2404.06492v1)** (2024)
  - 图强化学习在组合优化问题上的统一视角和系统性综述

### 图着色 (Graph Coloring)

#### 核心算法
- **[ReLCol](https://arxiv.org/abs/2304.04051)** (2023)
  - 使用DQN+GNN学习构造式启发策略，学习顶点着色顺序
  - MDP建模：状态为部分着色方案，动作选择下一个着色顶点，奖励基于新颜色数量

- **[LOMAC](https://openreview.net/pdf?id=49a2a85d60c6055f0607ba775a412c10a87aa7a0)** (ICLR 2024)
  - 通过状态空间重构将复杂度从O(K^N)降至O(N²)
  - 使用伪节点增强GNN和基于势能的奖励函数

#### 相关算法
- **[GNN + DQN](https://arxiv.org/pdf/1903.04598)** (2019)
  - 结合深度Q学习和GNN的启发式生成方法

- **[MCTS + DRL](https://link.springer.com/article/10.1007/s10878-025-01338-8)** (2025)
  - 蒙特卡洛树搜索与深度强化学习混合框架

- **[Deep Learning + Memetic](https://www.sciencedirect.com/science/article/pii/S0950705122010796)** (2022)
  - 深度学习指导模因算法的交叉操作

### 数值划分 (Number Partitioning)

#### 算法框架
- **顺序决策模型**
  - 按降序排列数字，训练RL智能体分配到子集
  - 等价于并行机调度问题，目标是最小化最大完工时间

#### 适用算法
- **策略梯度方法**: REINFORCE, PPO
  - 策略网络接收当前子集和状态，输出划分概率分布

- **Q-Learning方法**: DQN
  - Q网络学习数字分配到各划分的长期价值

#### 相关论文
- **[Neural CO with RL](https://arxiv.org/abs/1704.01916)** (2017)
  - 神经组合优化的开创性工作，适用于数值划分等场景

- **[RL for CO Survey](https://arxiv.org/abs/2003.03600)** (2020)
  - RL在组合优化问题中的应用前景综述

- **[RL for NP-hard](https://arxiv.org/abs/1905.06393)** (2019)
  - 使用RL处理NP困难问题的通用方法

## 📚 数据集来源

### 图划分 (Graph Partitioning)

| 数据集集合 | 描述 | 链接 |
|-----------|------|------|
| **[DIMACS10 图集](http://www.cc.gatech.edu/dimacs10/index.shtml)** | 第十届DIMACS实施挑战赛官方数据集，评估图划分与聚类算法的黄金标准 | [下载页面](https://www.cc.gatech.edu/dimacs10/downloads.shtml) |
| **[HypergraphPartitioning](https://github.com/TILOS-AI-Institute/HypergraphPartitioning)** | VLSI芯片设计领域的超图/图划分基准，包含ISPD98和Titan23测试集 | [GitHub仓库](https://github.com/TILOS-AI-Institute/HypergraphPartitioning) |
| **[开放图基准 (OGB)](https://ogb.stanford.edu/)** | 现代化大规模图数据集，专为图机器学习设计 | [官方网站](https://ogb.stanford.edu/) |
| **[SuiteSparse](https://sparse.tamu.edu/)** | 科学计算中的稀疏矩阵结构图，数千个来自不同应用领域的矩阵 | [官方网站](https://sparse.tamu.edu/) |
| **[SNAP 数据集](https://snap.stanford.edu/data/)** | 斯坦福网络分析项目的真实世界网络图，包含社交网络、引文网络等 | [官方网站](https://snap.stanford.edu/data/) |
| **[Graph-Partitioning-Benchmark](https://github.com/dbafemi/graph-partitioning-benchmark)** | 专为分布式图数据库划分算法评估设计，包含合成图生成器 | [GitHub仓库](https://github.com/dbafemi/graph-partitioning-benchmark) |

### 图着色 (Graph Coloring)

| 数据集集合 | 描述 | 链接 |
|-----------|------|------|
| **[DIMACS & COLOR02/03/04](https://mat.tepper.cmu.edu/COLOR/instances.html)** | 图着色算法性能评估最权威标准，包含随机图、几何图、寄存器分配图等 | [CMU官方页面](https://mat.tepper.cmu.edu/COLOR/instances.html) |
| **[ROARS Benchmark](https://roars.dev/npbench/graphcoloring.html)** | 格式齐全的图着色基准，提供多种经典实例 | [ROARS页面](https://roars.dev/npbench/graphcoloring.html) |
| **[Network Repository](https://networkrepository.com/dimacs.php)** | 真实世界和合成网络数据仓库，包含DIMACS图着色子集 | [DIMACS子集](https://networkrepository.com/dimacs.php) |
| **[Graph Coloring with RL](https://github.com/gpdwatkins/graph_colouring_with_RL)** | 专为RL图着色研究提供的数据集和代码仓库 | [GitHub仓库](https://github.com/gpdwatkins/graph_colouring_with_RL) |

### 数值划分 (Number Partitioning)

| 数据集/生成器 | 描述 | 链接 |
|-------------|------|------|
| **[Pedroso & Kubo NPP](https://www.dcc.fc.up.pt/~jpp/partition/readme.html)** | 基于"易-难-易"相变现象生成的标准实例，分为easy和hard两类 | [数据源](https://www.dcc.fc.up.pt/~jpp/partition/readme.html) |
| **[Mertens (2003) 理论](https://arxiv.org/pdf/cond-mat/0310317)** | 数值划分问题难度相变现象的理论分析，指导生成有意义的测试实例 | [论文链接](https://arxiv.org/pdf/cond-mat/0310317) |
| **[Tracer NPP](http://tracer.lcc.uma.es/problems/npp/npp.html)** | 程序化生成器说明，提供问题描述和生成思路 | [问题说明](http://tracer.lcc.uma.es/problems/npp/npp.html) |
| **[程序化生成器](https://github.com/Boulea7/CO-Benchmark-Datasets/blob/main/processed/number_partitioning/generate_npp_instances.py)** | 本项目内置生成器，支持自定义参数生成整数集 | [生成器代码](scripts/generate_npp_instances.py) |

## 📖 使用指南

详细的使用指南和文档：

- [`processed/README.md`](processed/README.md)：处理后数据集的详细说明
- [`scripts/README.md`](scripts/README.md)：脚本使用说明
- [`processed/graph_partitioning/README.md`](processed/graph_partitioning/README.md)：图划分数据集说明
- [`processed/graph_coloring/README.md`](processed/graph_coloring/README.md)：图着色数据集说明
- [`processed/number_partitioning/README.md`](processed/number_partitioning/README.md)：数值划分数据集说明

## 💻 代码规范

### 注释语言标准
本项目统一使用**中文**作为所有代码注释和文档的语言，确保：

- **可读性**：中文注释便于中文开发者理解和维护代码
- **一致性**：所有Python脚本、Shell脚本和文档都采用中文注释
- **专业性**：保持技术术语的准确性，同时使用中文进行说明

#### 注释示例
```python
def mk_data(n, nbits):
    """生成数值划分的随机数据：使用具有 'nbits' 位的整数"""
    data = []
    for i in range(n):
        # 构建具有指定位数的随机整数
        value = 0
        for b in range(nbits):
            if random.random() >= 0.5:
                value += 2**b
        data.append(value)
    return data
```

```bash
#!/bin/bash
# 数据集压缩脚本
# 使用多进程并行处理以提高效率

echo "开始压缩数据集..."
```

### 贡献者须知
当向本项目贡献代码时，请确保：
1. 所有函数和类的docstring使用中文
2. 行内注释使用中文说明代码逻辑
3. 脚本文件的头部说明使用中文
4. 保持与现有代码风格的一致性

## 📄 许可证

本项目采用MIT许可证。

## 🙏 致谢

感谢以下数据集和算法的提供者：

### 数据集提供者
- **DIMACS实施挑战赛**：提供图划分和图着色领域的权威基准数据集
- **SNAP网络数据集**：斯坦福网络分析项目的真实世界网络图
- **SuiteSparse矩阵集合**：科学计算中的稀疏矩阵结构图
- **开放图基准(OGB)**：为图机器学习设计的现代化大规模数据集
- **ROARS项目**：提供多种经典图着色基准实例
- **HypergraphPartitioning项目**：专为VLSI芯片设计领域的超图划分基准

### 算法和论文作者
- **Gatti et al.**：GNN-A2C多级优化方法的提出者
- **Mofrad et al.**：Revolver多智能体方法的开发者
- **Lemos et al.**：ReLCol图着色算法的作者
- **LOMAC团队**：状态空间重构方法的创新者
- **所有神经组合优化和强化学习在组合优化领域应用的研究者们**

---

<div align="center">

**当前版本：1.0.1 (2025-11-06)**

详细变更记录请参考：[`NextList.md`](NextList.md)

</div>