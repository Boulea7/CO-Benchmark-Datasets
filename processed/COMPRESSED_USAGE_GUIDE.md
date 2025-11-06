# 压缩数据集使用指南

本目录包含压缩后的数据集，按规模分类。

## 目录结构

```
processed/
├── graph_partitioning/compressed/
│   ├── tiny/      # xz压缩，高压缩比
│   ├── small/      # xz压缩，高压缩比
│   ├── medium/     # xz压缩，平衡压缩比和解压速度
│   ├── large/      # xz压缩，平衡压缩比和解压速度
│   └── xlarge/     # gzip/xz混合压缩，平衡速度和空间
├── graph_coloring/compressed/
│   ├── tiny/       # xz压缩，高压缩比
│   └── small/      # xz压缩，高压缩比
└── number_partitioning/compressed/
    ├── tiny/       # gzip压缩，快速解压
    ├── small/      # gzip压缩，快速解压
    ├── medium/     # gzip压缩，平衡压缩比和解压速度
    └── large/      # xz压缩，高压缩比
```

## 解压方法

### gzip文件
```bash
# 解压单个文件
gunzip file.txt.gz

# 解压整个目录
gunzip *.gz
```

### xz文件
```bash
# 解压单个文件
unxz file.txt.xz

# 解压整个目录
unxz *.xz
```

## Python中使用

```python
import gzip
import tarfile

# 解压gzip文件
with gzip.open('file.txt.gz', 'rt') as f:
    content = f.read()

# 解压xz文件
with tarfile.open('file.txt.xz', 'r:xz') as tar:
    with tar.extractfile(tar.getmember('file.txt')) as f:
        content = f.read().decode('utf-8')
```

## 压缩策略

我们使用混合压缩策略，平衡压缩比和解压速度：

- **图着色数据集**: 全部使用xz压缩，提供高压缩比
- **图划分数据集**:
  - tiny/small规模: 主要使用xz压缩
  - medium规模: 混合使用gzip和xz压缩
  - large/xlarge规模: 主要使用gzip压缩，提高解压速度
- **数值划分数据集**:
  - tiny/small规模: 使用gzip压缩，便于频繁访问
  - medium/large规模: 使用xz压缩，节省存储空间

## 注意事项

1. 所有原始文件已删除，请使用压缩版本
2. xz压缩文件需要更多时间解压，但压缩比更高
3. gzip压缩文件解压速度快，适合大文件和频繁访问
4. 建议根据使用频率选择合适的数据集规模
5. 如果压缩被中断，可以重新运行脚本，它会自动从断点继续

## 推荐使用方法

建议使用统一数据加载器 `scripts/unified_loader.py` 直接加载压缩文件，无需手动解压：

```python
from scripts.unified_loader import load_graph_txt, load_npp_txt, load_instance

# 直接加载压缩文件
graph = load_graph_txt('processed/graph_partitioning/compressed/tiny/dolphins.txt.xz')
npp = load_npp_txt('processed/number_partitioning/compressed/small/n025d12e00.txt.xz')
instance = load_instance('processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz')