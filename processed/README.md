# 处理后数据集

本目录用于存放经过 `scripts/parser.py` 处理后的、统一格式的.txt文件。

## 目录结构

```
processed/
├── graph_coloring/          # 处理后的图着色数据
├── graph_partitioning/       # 处理后的图划分数据
└── number_partitioning/      # 处理后的数值划分数据
```

## 数据加载

推荐使用统一数据加载器 `scripts/unified_loader.py` 加载处理后的数据：

```python
from scripts.unified_loader import load_graph_txt, load_npp_txt, load_instance

# 加载图数据（自动处理索引转换、去重和去自环）
graph = load_graph_txt("processed/graph_partitioning/compressed/tiny/dolphins.txt.xz")

# 加载数值划分数据
npp = load_npp_txt("processed/number_partitioning/compressed/small/n025d12e00.txt.xz")

# 自动识别并加载任何类型的数据集
instance = load_instance("processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz")

# 批量加载
from scripts.unified_loader import batch_load_instances
instances = batch_load_instances([
    "processed/graph_partitioning/compressed/tiny/dolphins.txt.xz",
    "processed/number_partitioning/compressed/small/n025d12e00.txt.xz"
])
```

## 数据特点

1. **统一格式**: 所有数据都采用相同的.txt格式，便于统一处理
2. **完整元信息**: 头部包含问题类型、规模、参数等关键信息
3. **标准化索引**: 图数据使用1-based索引，便于算法处理
4. **去重处理**: 已去除重复边和自环
5. **兼容性**: 兼容RLSolver等现有框架

## 相关文档

- [`COMPRESSED_USAGE_GUIDE.md`](COMPRESSED_USAGE_GUIDE.md)：压缩数据集使用指南
- [`graph_partitioning/README.md`](graph_partitioning/README.md)：图划分数据集详细说明
- [`graph_coloring/README.md`](graph_coloring/README.md)：图着色数据集详细说明
- [`number_partitioning/README.md`](number_partitioning/README.md)：数值划分数据集详细说明

## 数据集划分

处理后的数据将用于创建训练/验证/测试集划分，确保：
- 按规模分层抽样
- 覆盖不同来源的数据
- 保持数据分布的多样性