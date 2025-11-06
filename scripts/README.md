# 脚本说明

本目录包含用于处理数据集的脚本。

## 核心脚本

### 统一数据加载器（推荐使用）

**unified_loader.py** - 统一数据加载器
- 支持所有三种问题类型的数据加载
- 自动处理索引转换、去重和去自环
- 支持压缩文件格式（.gz, .xz）
- 智能处理压缩文件中的tar头部信息

```python
from scripts.unified_loader import load_graph_txt, load_npp_txt, load_instance

# 加载图数据（自动处理索引转换、去重和去自环）
graph = load_graph_txt("processed/graph_partitioning/compressed/tiny/dolphins.txt.xz")

# 加载数值划分数据
npp = load_npp_txt("processed/number_partitioning/compressed/small/n025d12e00.txt.xz")

# 自动识别并加载（支持所有三种类型）
instance = load_instance("processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz")
```

### 其他主要脚本

- **example_usage.py** - 使用示例脚本
- **compress_datasets_parallel.py** - 并行压缩脚本
- **parse_gp.py** - 图划分数据解析器
- **parse_gc.py** - 图着色数据解析器
- **parse_npp.py** - 数值划分数据解析器
- **loader.py** - 传统数据加载器（仅支持未压缩文件）

## 工具脚本

### 数据处理工具
- **parser.py** - 通用数据解析器
- **compress_datasets.py** - 数据压缩脚本
- **decompress_datasets.py** - 数据解压脚本

### 数据检查工具
- **check_npp_completeness.py** - 检查NPP数据集完整性
- **check_gp_completeness.py** - 检查GP数据集完整性
- **run_all_checks.sh** - 一键执行所有检查

### 数据清理工具
- **clean_compressed_files.py** - 清理已压缩的原始文件
- **remove_duplicate_compressed.py** - 删除重复的压缩文件
- **clean_directory_structure.py** - 清理混乱的目录结构
- **organize_npp_by_size.py** - 按规模组织NPP数据集

### 数据生成工具
- **generate_npp_instances.py** - NPP数据集生成器
- **generate_missing_instances.py** - 生成缺失规模的NPP实例

## 数据格式

所有处理后的数据集采用统一格式，详细说明请参考：
- [`../processed/README.md`](../processed/README.md)：数据格式说明
- [`../processed/COMPRESSED_USAGE_GUIDE.md`](../processed/COMPRESSED_USAGE_GUIDE.md)：压缩数据集使用指南

## 依赖

- Python 3.8+
- numpy
- networkx (仅用于某些高级转换功能)

## 注意事项

1. 所有图数据都转换为无向图，使用1-based索引
2. 数值划分数据支持逐行或单行格式
3. 头部信息以`#`开头，加载器会自动跳过这些行
4. 边权重默认为1，除非原始数据指定了权重