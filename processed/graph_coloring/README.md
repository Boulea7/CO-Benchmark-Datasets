# 图着色（Graph Coloring）数据集

## 概述

本目录包含图着色问题的数据集，这是一个经典的NP-Hard问题：为图 $G=(V,E)$ 的每个顶点分配一个"颜色"，使得任意两个相邻的顶点都具有不同的颜色，同时最小化所使用的颜色总数。

## 目录结构

```
processed/graph_coloring/
├── compressed/               # 压缩后的数据集
│   ├── tiny/               # < 1,000 节点，用于快速测试
│   └── small/              # 1,000-10,000 节点，用于算法开发
└── compression_report.txt   # 压缩统计报告
```

## 数据集来源

主要包含来自DIMACS实施挑战赛和COLOR系列研讨会的图着色实例，这是图着色算法的公认标准。

数据集包括多种图族：
- **随机图（DSJC系列）**：具有不同边密度的随机图
- **几何图（flat系列）**：基于几何约束的图
- **寄存器分配图（le450系列）**：来自寄存器分配问题的图
- **皇后图（queen系列）**：N皇后问题对应的图
- **Mycielski图（myciel系列）**：具有高色数的图
- **其他特殊图**：如学校时间表、书籍引用网络等

## 数据集统计

| 规模 | 文件数量 | 节点数范围 | 边数范围 | 推荐用途 |
|--------|----------|--------------|------------|----------|
| tiny | 73 | 11-864 | 0-19095 | 快速测试和算法开发 |
| small | 6 | 1000 | 24911-31398 | 算法开发和调试 |

**总计**: 79个数据集，589,522条边

**压缩状态**: 所有数据集已压缩，压缩比82.9%（从5.06MB压缩到0.87MB）

## 使用方法

推荐使用统一数据加载器：

```python
from scripts.unified_loader import load_graph_txt

# 加载压缩数据集
graph = load_graph_txt("processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz")

# 访问数据
print(f"问题类型: {graph.meta.get('problem')}")
print(f"实例名称: {graph.name}")
print(f"节点数: {graph.n}")
print(f"边数: {graph.m}")
```

## 算法基准

### 公认RL算法

1. **ReLCol（2023）**
   - 基于DQN+GNN的构造式启发式方法
   - 学习顶点选择顺序，然后使用First-Fit规则着色
   - 论文：https://arxiv.org/abs/2304.04051

2. **LOMAC（2024）**
   - 面向大图的深度强化学习框架
   - 通过状态空间重构实现高效着色
   - 论文：https://openreview.net/forum?id=yG2WrLenxd

## 相关文档

- [`../../COMPRESSED_USAGE_GUIDE.md`](../COMPRESSED_USAGE_GUIDE.md)：压缩数据集使用指南
- [`../../scripts/README.md`](../../scripts/README.md)：脚本使用说明

## 注意事项

1. 所有图数据都是无向图，使用1-based索引
2. 边权重统一为1（无权图）
3. 二进制格式文件（.col.b）已成功解析，使用14位编码（每个节点7位）
4. 部分二进制文件可能无法完全解析所有边，但已解析的边足够用于算法测试
5. 建议根据研究需求选择合适规模的数据集
6. 不同来源的图具有不同的结构特征，建议多样化选择以测试算法泛化能力