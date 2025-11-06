# NPP数据集生成器

## 概述

本目录包含一个数值划分问题（Number Partitioning Problem, NPP）的数据集生成器，可以生成三种类型的基准测试实例：

1. **Easy实例**：使用n/2位随机数，有大量完美分割
2. **Hard实例**：使用n位随机数，有少量完美分割
3. **Decimal实例**：使用十进制随机数

## 使用方法

### 基本用法

```bash
# 生成所有类型的实例
python3 generate_npp_instances.py --type all --output-dir ./generated_instances

# 只生成easy实例
python3 generate_npp_instances.py --type easy --output-dir ./easy_instances

# 只生成hard实例
python3 generate_npp_instances.py --type hard --output-dir ./hard_instances

# 只生成decimal实例
python3 generate_npp_instances.py --type decimal --output-dir ./decimal_instances
```

### 参数说明

- `--type`: 要生成的实例类型，可选值：`easy`, `hard`, `decimal`, `all`（默认：`all`）
- `--output-dir`: 输出目录（默认：`generated_instances`）
- `--seed`: 随机种子（默认：`1`）

## 实例规模

### Easy/Hard实例

生成以下规模的实例：
- 小规模：10, 20, 30, 40, 50, 60, 70, 80, 90, 100
- 中规模：200, 300, 400, 500, 600, 700, 800, 900
- 大规模：1000

### Decimal实例

生成以下参数组合的实例：
- 位数：10, 12, 14
- 元素数量：15, 25, 35, 45, 55, 65, 75, 85, 95, 105
- 实验编号：0-9（每个组合10个实例）

## 文件格式

生成的文件遵循NPP标准格式：

```
# problem: number_partitioning
# name: easy0010.txt
# n: 10
# k: 2
# generator: npp_mk_inst

10
0
0
5
6
6
6
13
14
19
27
```

其中：
- 第一行`# problem: number_partitioning`标识问题类型
- 第二行`# name: easy0010.txt`是实例名称
- 第三行`# n: 10`是数字个数
- 第四行`# k: 2`是划分数
- 第五行`# generator: npp_mk_inst`是生成器标识
- 第六行是空行
- 第七行是数字个数
- 后续每行是一个数字

## 理论背景

根据S.Mertens的"The easiest hard problem"研究，随机生成整数的关键位数决定了问题的难度。详细理论说明请参考[`README.md`](README.md)。

## 注意事项

1. 生成的实例已经排序，便于处理
2. 使用相同的随机种子可以生成相同的实例集
3. 生成的文件可以直接使用`scripts/loader.py`加载
4. 建议生成后使用压缩脚本进行压缩以节省存储空间

## 示例

```bash
# 生成小规模的easy实例用于快速测试
python3 generate_npp_instances.py --type easy --output-dir ./test_easy --seed 42

# 生成所有类型的实例用于完整测试
python3 generate_npp_instances.py --type all --output-dir ./full_test --seed 123

# 压缩生成的实例
cd ./full_test
python3 ../../scripts/compress_datasets.py --input . --output ./compressed