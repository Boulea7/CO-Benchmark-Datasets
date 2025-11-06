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

## 📚 Table of Contents

- [Abstract](#-abstract)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Dataset Overview](#-dataset-overview)
- [Algorithm Baselines](#-algorithm-baselines)
- [Data Sources](#-data-sources)
- [Usage Guidelines](#-usage-guidelines)
- [Performance Benchmarks](#-performance-benchmarks)
- [Repository Structure](#-repository-structure)
- [Contributing](#-contributing)
- [Citation](#-citation)
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

### 图划分

- **GNN-A2C 多级优化方法**：结合经典多级框架和A2C算法，使用GNN进行局部优化
- **Revolver**：去中心化的多智能体方法，将每个顶点视为一个智能体
- **NeuroCUT (2023)**：支持任意k路划分和非可微目标的GNN+RL框架
- **PR-GPT (2024)**：采用预训练-微调范式，加速大规模图的划分

### 图着色

- **ReLCol**：使用DQN和GNN学习构造式启发策略
- **LOMAC (2024)**：通过状态空间重构实现可扩展着色，复杂度降至O(N²)
- **混合框架**：结合深度学习与蒙特卡洛树搜索或模因算法

### 数值划分

- **顺序决策模型**：按降序排列数字，训练RL智能体分配到子集
- **适用算法**：策略梯度方法（REINFORCE, PPO）和Q-Learning方法（DQN）

## 📚 数据集来源

### 图划分
- **DIMACS10 图集**：第十届DIMACS实施挑战赛官方数据集
- **HypergraphPartitioning**：VLSI芯片设计领域的超图/图划分基准
- **开放图基准 (OGB)**：现代化大规模图数据集
- **SuiteSparse & SNAP**：科学计算和真实世界网络图实例

### 图着色
- **DIMACS & COLOR02/03/04**：图着色算法性能评估最权威标准
- **ROARS Benchmark Instances**：格式齐全的图着色基准
- **Network Repository**：真实世界和合成网络数据仓库

### 数值划分
- **Pedroso & Kubo 的 NPP 实例**：基于相变现象生成的实例
- **Mertens (2003)**：数值划分问题难度相变现象的理论分析
- **程序化生成器**：用户自定义参数生成整数集

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

## 📈 项目状态

- [x] 项目初始化和文档编写
- [x] 目录结构创建
- [x] 数据处理脚本开发
- [x] 数据集下载和收集
- [x] 数据格式标准化
- [x] 数据集压缩和优化
- [x] 统一数据加载器开发
- [x] 文档整理和优化
- [x] 大文件分块处理（GitHub 文件大小限制合规）
- [x] 项目清理工作（添加.claude到.gitignore，清理.DS_Store文件）
- [ ] 训练/验证/测试集划分
- [ ] 基线算法实现和测试
- [ ] 性能基准测试

## 🤝 贡献指南

欢迎提交问题报告、功能请求或数据集贡献。请确保：

1. 新数据集遵循现有的格式标准
2. 包含适当的元数据
3. 添加相应的测试用例
4. 更新文档

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