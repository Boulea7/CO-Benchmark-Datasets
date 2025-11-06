# Graph Partitioning 数据集

本目录包含按规模分类的数据集，便于根据需求选择合适的数据。

## 目录结构

```
processed/graph_partitioning/
├── compressed/               # 压缩后的数据集
│   ├── tiny/               # < 1,000 节点，用于快速测试
│   ├── small/              # 1,000-10,000 节点，用于算法开发
│   ├── medium/             # 10,000-100,000 节点，用于标准训练
│   ├── large/              # 100,000-1,000,000 节点，用于性能评估
│   └── xlarge/             # > 1,000,000 节点，用于压力测试
└── USAGE_GUIDE.md          # 使用指南
```

## 数据集统计

| 规模 | 文件数量 | 推荐用途 |
|------|--------|----------|
| tiny | 3 | 快速测试和算法调试 |
| small | 4 | 算法开发和小规模实验 |
| medium | 4 | 标准训练和算法比较 |
| large | 17 | 可扩展性测试和大规模验证 |
| xlarge | 21 | 最终压力测试和极限性能评估 |

## 使用方法

推荐使用统一数据加载器：

```python
from scripts.unified_loader import load_graph_txt

# 加载压缩数据集
graph = load_graph_txt('processed/graph_partitioning/compressed/tiny/dolphins.txt.xz')
print(f'节点数: {graph.n}')
print(f'边数: {graph.m}')
```

## 使用建议

1. **开发阶段**: 使用tiny和small数据集
2. **测试阶段**: 使用medium数据集
3. **验证阶段**: 使用large和xlarge数据集

## 相关文档

- [`USAGE_GUIDE.md`](USAGE_GUIDE.md)：详细使用指南
- [`../../COMPRESSED_USAGE_GUIDE.md`](../COMPRESSED_USAGE_GUIDE.md)：压缩数据集使用指南
- [`../../scripts/README.md`](../../scripts/README.md)：脚本使用说明

## 注意事项

1. 大型数据集可能需要较多内存，建议根据硬件条件选择合适规模
2. 超大型数据集主要用于算法可扩展性验证，不适合频繁训练
3. 不同来源的图具有不同的结构特征，建议多样化选择以测试算法泛化能力
4. 部分原始数据集可能包含多个连通分量，使用时需要注意
