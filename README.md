<div align="center">

# 🚀 CO-Benchmark-Datasets

**强化学习在组合优化问题中的综合基准数据集**

[![版本](https://img.shields.io/badge/版本-1.0.1-blue.svg)](https://github.com/Boulea7/CO-Benchmark-Datasets)
[![许可证](https://img.shields.io/badge/许可证-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![问题](https://img.shields.io/github/issues/Boulea7/CO-Benchmark-Datasets)](https://github.com/Boulea7/CO-Benchmark-Datasets/issues)
[![大小](https://img.shields.io/github/repo-size/Boulea7/CO-Benchmark-Datasets)](https://github.com/Boulea7/CO-Benchmark-Datasets)
[![数据集](https://img.shields.io/badge/数据集-447%20个文件-orange.svg)]()

## 🎯 研究重点：NP-Hard组合优化问题

**专为推进强化学习算法在经典NP-Hard问题中的应用而设计的专业基准数据集**

</div>

---

## 📋 摘要

本仓库提供了一套全面的标准化、高质量基准数据集，专门用于评估强化学习算法在经典组合优化问题上的性能。我们的基准测试套件专注于三个基本的NP-Hard问题，这些问题是算法创新的关键测试平台：

- 🔄 **图划分** - 在保持平衡约束的同时最小化切割边
- 🎨 **图着色** - 最小化色数同时避免相邻冲突
- 🔢 **数值划分** - 平衡子集分配以最小化最大完成时间

这些数据集经过精心策划，来自多个权威来源，处理成统一格式，并为机器学习工作流程进行了优化，为研究和评估下一代强化学习算法提供了重要工具。


## 📚 目录

- [摘要](#-摘要)
- [主要特点](#-主要特点)
- [安装](#-安装)
- [快速开始](#-快速开始)
- [数据集概览](#-数据集概览)
- [算法基准](#-算法基准)
- [数据集来源](#-数据集来源)
- [使用指南](#-使用指南)
- [项目结构](#-项目结构)
- [许可证](#-许可证)
- [致谢](#-致谢)

## ✨ 主要特点

### 🔧 **技术卓越**
- **统一格式标准**：所有数据集转换为符合RLSolver竞赛规范的一致文本格式
- **可扩展规模分类**：系统性分类（tiny/small/medium/large/xlarge），便于渐进式算法开发
- **高压缩比**：平均88.9%的压缩效率，同时保持数据完整性
- **丰富元数据基础**：全面的问题规范、来源证明和难度标注

### 🚀 **机器学习就绪基础设施**
- **自动数据加载**：具有格式检测和预处理能力的智能加载器
- **LFS集成**：Git大文件存储支持，高效版本控制大型数据集
- **批处理支持**：为训练管道优化，支持并行加载
- **跨平台兼容性**：Python 3.8+支持，依赖最少

### 📊 **研究级质量**
- **多个权威来源**：来自DIMACS挑战赛、学术基准和真实世界网络的数据集
- **平衡问题分布**：精心选择跨越难度谱和结构特征的问题
- **可重现结果**：确定性加载和处理确保实验一致性

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

### 图划分
- **[GNN-A2C 多级优化方法](https://www.jmlr.org/papers/volume23/21-0644/21-0644.pdf)** (JMLR 2022)
- **[Revolver](https://arxiv.org/abs/1907.06768)** (IEEE CLOUD 2018)
- **[NeuroCUT](https://arxiv.org/abs/2310.11787)** (2023)
- **[PR-GPT](https://arxiv.org/abs/2409.00670)** (2024)

### 图着色
- **[ReLCol](https://arxiv.org/abs/2304.04051)** (2023)
- **[LOMAC](https://openreview.net/pdf?id=49a2a85d60c6055f0607ba775a412c10a87aa7a0)** (ICLR 2024)
- **[GNN + DQN](https://arxiv.org/pdf/1903.04598)** (2019)
- **[MCTS + DRL](https://link.springer.com/article/10.1007/s10878-025-01338-8)** (2025)

### 数值划分
- **[Neural CO with RL](https://arxiv.org/abs/1704.01916)** (2017)
- **[RL for CO Survey](https://arxiv.org/abs/2003.03600)** (2020)
- **[RL for NP-hard](https://arxiv.org/abs/1905.06393)** (2019)

## 📚 数据集来源

### 图划分
- **[DIMACS10 图集](http://www.cc.gatech.edu/dimacs10/index.shtml)** - 第十届DIMACS实施挑战赛官方数据集
- **[HypergraphPartitioning](https://github.com/TILOS-AI-Institute/HypergraphPartitioning)** - VLSI芯片设计领域基准
- **[开放图基准 (OGB)](https://ogb.stanford.edu/)** - 现代化大规模图数据集
- **[SuiteSparse](https://sparse.tamu.edu/)** - 科学计算稀疏矩阵结构图
- **[SNAP 数据集](https://snap.stanford.edu/data/)** - 真实世界网络图

### 图着色
- **[DIMACS & COLOR02/03/04](https://mat.tepper.cmu.edu/COLOR/instances.html)** - 图着色算法权威标准
- **[ROARS Benchmark](https://roars.dev/npbench/graphcoloring.html)** - 格式齐全的图着色基准
- **[Network Repository](https://networkrepository.com/dimacs.php)** - 真实世界和合成网络

### 数值划分
- **[Pedroso & Kubo NPP](https://www.dcc.fc.up.pt/~jpp/partition/readme.html)** - 基于相变现象的标准实例
- **[Mertens (2003) 理论](https://arxiv.org/pdf/cond-mat/0310317)** - 难度相变现象理论分析

## 📖 使用指南

详细的使用指南和文档：

- [`processed/README.md`](processed/README.md)：处理后数据集的详细说明
- [`scripts/README.md`](scripts/README.md)：脚本使用说明
- [`processed/graph_partitioning/README.md`](processed/graph_partitioning/README.md)：图划分数据集说明
- [`processed/graph_coloring/README.md`](processed/graph_coloring/README.md)：图着色数据集说明
- [`processed/number_partitioning/README.md`](processed/number_partitioning/README.md)：数值划分数据集说明

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