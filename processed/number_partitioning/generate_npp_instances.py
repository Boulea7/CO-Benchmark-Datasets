#!/usr/bin/env python3
"""
NPP数据集生成器

该脚本用于生成数值划分问题的基准测试实例，支持三种类型的实例：
1. easy实例：使用n/2位随机数，有大量完美分割
2. hard实例：使用n位随机数，有少量完美分割
3. decimal实例：使用十进制随机数

使用方法:
    python generate_npp_instances.py --type easy --output-dir ./easy_instances
    python generate_npp_instances.py --type hard --output-dir ./hard_instances
    python generate_npp_instances.py --type decimal --output-dir ./decimal_instances
"""

import os
import random
import argparse
from pathlib import Path

def mk_data_trivial(n, min_value, max_value):
    """生成随机数据：简单情况"""
    return [min_value + int(random.random() * (max_value-min_value+1)) for i in range(n)]

def mk_data(n, nbits):
    """生成随机数据：使用'nbits'位整数"""
    data = []
    for i in range(n):
        value = 0
        for b in range(nbits):
            if random.random() >= 0.5:
                value += 2**b
        data.append(value)
    return data

def mk_data_decimal(n, nbits):
    """生成随机数据：使用'nbits'位十进制整数"""
    data = []
    for i in range(n):
        value = 0
        for b in range(nbits):
            value = 10*value + int(random.random()*10)
        data.append(value)
    return data

def write_data(filename, data):
    """将数据写入文件，符合NPP标准格式"""
    print(f"生成文件: {filename}")
    with open(filename, 'w') as f:
        # 写入头部信息
        f.write(f"# problem: number_partitioning\n")
        f.write(f"# name: {os.path.basename(filename)}\n")
        f.write(f"# n: {len(data)}\n")
        f.write(f"# k: 2\n")
        f.write(f"# generator: npp_mk_inst\n")
        f.write(f"\n")
        
        # 写入数据
        f.write(f"{len(data)}\n")
        for i in data:
            f.write(f"{i}\n")

def generate_easy_instances(output_dir, sizes):
    """生成easy实例"""
    print(f"生成 {len(sizes)} 个easy实例...")
    
    for n in sizes:
        # easy实例：使用n/2位随机数
        data = mk_data(n, n//2)
        data.sort()
        filename = f"easy{n:04d}.txt"
        filepath = os.path.join(output_dir, filename)
        write_data(filepath, data)

def generate_hard_instances(output_dir, sizes):
    """生成hard实例"""
    print(f"生成 {len(sizes)} 个hard实例...")
    
    for n in sizes:
        # hard实例：使用n位随机数
        data = mk_data(n, n)
        data.sort()
        filename = f"hard{n:04d}.txt"
        filepath = os.path.join(output_dir, filename)
        write_data(filepath, data)

def generate_decimal_instances(output_dir, bit_sizes, element_sizes, experiments):
    """生成decimal实例"""
    print(f"生成 {len(bit_sizes) * len(element_sizes) * len(experiments)} 个decimal实例...")
    
    for b in bit_sizes:
        for n in element_sizes:
            for e in experiments:
                # decimal实例：使用十进制随机数
                data = mk_data_decimal(n, b)
                data.sort()
                filename = f"n{n:03d}d{b:02d}e{e:02d}.txt"
                filepath = os.path.join(output_dir, filename)
                write_data(filepath, data)

def main():
    parser = argparse.ArgumentParser(description="生成NPP数据集实例")
    parser.add_argument("--type", choices=["easy", "hard", "decimal", "all"], 
                       default="all", help="要生成的实例类型")
    parser.add_argument("--output-dir", default="generated_instances",
                       help="输出目录 (默认: generated_instances)")
    parser.add_argument("--seed", type=int, default=1,
                       help="随机种子 (默认: 1)")
    
    args = parser.parse_args()
    
    # 设置随机种子
    random.seed(args.seed)
    
    # 确保输出目录存在
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"NPP数据集生成器")
    print("=" * 50)
    print(f"实例类型: {args.type}")
    print(f"输出目录: {output_dir}")
    print(f"随机种子: {args.seed}")
    print()
    
    # 定义实例大小
    easy_hard_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    decimal_bit_sizes = [10, 12, 14]
    decimal_element_sizes = [15, 25, 35, 45, 55, 65, 75, 85, 95, 105]
    decimal_experiments = list(range(10))
    
    # 生成实例
    if args.type in ["easy", "all"]:
        easy_dir = output_dir / "easy"
        easy_dir.mkdir(exist_ok=True)
        generate_easy_instances(str(easy_dir), easy_hard_sizes)
        print()
    
    if args.type in ["hard", "all"]:
        hard_dir = output_dir / "hard"
        hard_dir.mkdir(exist_ok=True)
        generate_hard_instances(str(hard_dir), easy_hard_sizes)
        print()
    
    if args.type in ["decimal", "all"]:
        decimal_dir = output_dir / "decimal"
        decimal_dir.mkdir(exist_ok=True)
        generate_decimal_instances(str(decimal_dir), decimal_bit_sizes, decimal_element_sizes, decimal_experiments)
        print()
    
    print("✅ 实例生成完成!")

if __name__ == "__main__":
    main()