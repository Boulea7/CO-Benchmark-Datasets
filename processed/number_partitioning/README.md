# 数值划分问题（Number Partitioning Problem, NPP）数据集

## 概述

本目录包含数值划分问题的数据集，这是一个经典的NP-Hard问题：给定一组数字，将其划分为两个子集，使得两个子集的和尽可能接近。

## 目录结构

```
processed/number_partitioning/
├── compressed/                  # 压缩后的数据集
│   ├── tiny/                   # 小规模实例（< 5KB）
│   ├── small/                  # 小规模实例（5KB - 20KB）
│   ├── medium/                 # 中等规模实例（20KB - 100KB）
│   └── large/                  # 大规模实例（≥ 100KB）
├── generate_npp_instances.py   # 数据集生成器
└── GENERATOR_README.md         # 生成器使用说明
```

## 数据集来源

### 原始数据集

原始数据集来自Pedroso & Kubo格式，包含300个实例，按以下方式命名：
- `nXXXdYYeZZ.txt`：其中XXX表示数字个数，YY表示数字位数，ZZ表示实验编号

### 生成数据集

使用`generate_npp_instances.py`脚本可以生成三种类型的实例：
1. **Easy实例**：使用n/2位随机数，有大量完美分割
2. **Hard实例**：使用n位随机数，有少量完美分割
3. **Decimal实例**：使用十进制随机数

详细使用方法请参考[`GENERATOR_README.md`](GENERATOR_README.md)。

## 数据集规模

| 规模 | 文件数量 | 描述 |
|--------|----------|--------|
| tiny | 15 | 小规模实例（< 5KB） |
| small | 35 | 小规模实例（5KB - 20KB） |
| medium | 6 | 中等规模实例（20KB - 100KB） |
| large | 3 | 大规模实例（≥ 100KB） |

## 使用方法

推荐使用统一数据加载器：

```python
from scripts.unified_loader import load_npp_txt

# 加载压缩数据集
npp = load_npp_txt("processed/number_partitioning/compressed/small/n025d12e00.txt.xz")

# 访问数据
print(f"问题类型: {npp.problem}")
print(f"实例名称: {npp.name}")
print(f"数字个数: {npp.n}")
print(f"划分数: {npp.k}")
print(f"数字: {npp.values}")
```

## 理论背景

根据S.Mertens的"The easiest hard problem"研究，随机生成整数的关键位数决定了问题的难度：

对于N个元素的问题，临界位数为：
```
kc(N) = 1 - (log2(N) - log2(pi/6))/(1.7*N)
```

- Easy实例使用n/2位随机数，远低于临界位数，因此有大量完美分割
- Hard实例使用n位随机数，接近临界位数，因此有少量完美分割

## 相关文档

- [`GENERATOR_README.md`](GENERATOR_README.md)：数据集生成器详细说明
- [`../../COMPRESSED_USAGE_GUIDE.md`](../COMPRESSED_USAGE_GUIDE.md)：压缩数据集使用指南
- [`../../scripts/README.md`](../../scripts/README.md)：脚本使用说明

## 注意事项

1. 所有数据集已经过排序，便于处理
2. 压缩文件可以使用`scripts/decompress_datasets.py`解压
3. 生成的数据集可以直接使用`scripts/unified_loader.py`加载
4. 建议根据研究需求选择合适规模的数据集