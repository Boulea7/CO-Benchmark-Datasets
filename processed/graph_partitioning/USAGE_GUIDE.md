# 图划分数据集使用指南

## 数据集分类

数据集已按规模分为以下类别：

### TINY (微型) - < 1,000 节点
- **用途**: 快速测试、算法调试、原型验证
- **推荐文件**: karate.txt, dolphins.txt, jazz.txt

### SMALL (小型) - 1,000-10,000 节点
- **用途**: 算法开发、小规模实验、教学演示
- **推荐文件**: PGPgiantcompo.txt, as-22july06.txt, cond-mat.txt

### MEDIUM (中型) - 10,000-100,000 节点
- **用途**: 标准训练、算法比较、性能评估
- **推荐文件**: preferentialAttachment.txt, bcsstk08.txt, bcsstk13.txt

### LARGE (大型) - 100,000-1,000,000 节点
- **用途**: 可扩展性测试、大规模算法验证
- **推荐文件**: cnr-2000.txt, eu-2005.txt, NACA0015.txt

### XLARGE (超大型) - > 1,000,000 节点
- **用途**: 最终压力测试、极限性能评估
- **推荐文件**: road_central.txt, audikw1.txt, ldoor.txt

## 使用方法

### 1. 加载数据
```python
from scripts.loader import load_graph_txt

# 加载图数据
graph = load_graph_txt('processed/graph_partitioning/tiny/karate.txt')
print(f'节点数: {graph.n}')
print(f'边数: {graph.m}')
```

### 2. 按规模选择数据集
- **开发阶段**: 使用TINY和SMALL数据集
- **测试阶段**: 使用MEDIUM数据集
- **验证阶段**: 使用LARGE和XLARGE数据集

### 3. 内存管理建议
- **大型数据集**: 建议分批加载，避免内存不足
- **超大型数据集**: 可能需要分布式处理或特殊内存管理技术

### 4. 算法评估建议
- **多规模测试**: 在不同规模数据集上测试算法性能
- **对比基线**: 与经典算法（如METIS）进行性能对比
- **指标记录**: 记录切割大小、平衡度、运行时间等指标

