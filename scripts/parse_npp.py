#!/usr/bin/env python3
"""
数值划分（Number Partitioning）数据集解析脚本
将P&K的.dat格式转换为统一文本格式
"""

import os
import argparse
import zipfile
from pathlib import Path
from typing import List, Tuple, Dict, Any


def parse_dat_file(file_path: str) -> Tuple[List[int], int]:
    """
    解析P&K的.dat格式文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        (numbers, k): 数字列表、划分数
    """
    numbers = []
    k = 0
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
        # 第一行是数字个数和划分数
        if lines:
            first_line = lines[0].strip()
            parts = first_line.split()
            if len(parts) >= 2:
                n = int(parts[0])
                k = int(parts[1])
        
        # 后续行是数字
        for line in lines[1:]:
            line = line.strip()
            if line:
                try:
                    num = int(line)
                    numbers.append(num)
                except ValueError:
                    continue
    
    return numbers, k


def write_txt_file(numbers: List[int], k: int, output_path: str, name: str):
    """
    将数字列表写入统一文本格式
    
    Args:
        numbers: 数字列表
        k: 划分数
        output_path: 输出文件路径
        name: 实例名称
    """
    with open(output_path, 'w') as f:
        # 写入头部信息
        f.write(f"# problem: number_partitioning\n")
        f.write(f"# name: {name}\n")
        f.write(f"# n: {len(numbers)}\n")
        f.write(f"# k: {k}\n")
        f.write(f"\n")
        
        # 写入数字
        f.write(f"{len(numbers)}\n")
        for num in numbers:
            f.write(f"{num}\n")


def extract_zip(zip_path: str, extract_dir: str):
    """
    解压zip文件
    
    Args:
        zip_path: zip文件路径
        extract_dir: 解压目录
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)


def process_npp_database(input_dir: str, output_dir: str):
    """
    处理NPP数据库
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 按规模分类
    tiny_dir = os.path.join(output_dir, 'tiny')
    small_dir = os.path.join(output_dir, 'small')
    medium_dir = os.path.join(output_dir, 'medium')
    large_dir = os.path.join(output_dir, 'large')
    xlarge_dir = os.path.join(output_dir, 'xlarge')
    
    os.makedirs(tiny_dir, exist_ok=True)
    os.makedirs(small_dir, exist_ok=True)
    os.makedirs(medium_dir, exist_ok=True)
    os.makedirs(large_dir, exist_ok=True)
    os.makedirs(xlarge_dir, exist_ok=True)
    
    # 处理easy文件
    easy_zip = os.path.join(input_dir, 'easy.zip')
    if os.path.exists(easy_zip):
        print(f"解压easy.zip...")
        extract_zip(easy_zip, input_dir)
        
        # 处理easy文件
        easy_dir = os.path.join(input_dir, 'easy')
        if os.path.exists(easy_dir):
            for file in os.listdir(easy_dir):
                if file.endswith('.dat'):
                    file_path = os.path.join(easy_dir, file)
                    numbers, k = parse_dat_file(file_path)
                    
                    # 根据数字个数分类
                    n = len(numbers)
                    if n <= 100:
                        output_dir_size = tiny_dir
                    elif n <= 1000:
                        output_dir_size = small_dir
                    elif n <= 10000:
                        output_dir_size = medium_dir
                    else:
                        output_dir_size = large_dir
                    
                    # 写入文件
                    output_file = os.path.join(output_dir_size, file.replace('.dat', '.txt'))
                    write_txt_file(numbers, k, output_file, file.replace('.dat', ''))
                    print(f"处理: {file} -> {output_file}")
    
    # 处理hard文件
    hard_zip = os.path.join(input_dir, 'hard.zip')
    if os.path.exists(hard_zip):
        print(f"解压hard.zip...")
        extract_zip(hard_zip, input_dir)
        
        # 处理hard文件
        hard_dir = os.path.join(input_dir, 'hard')
        if os.path.exists(hard_dir):
            for file in os.listdir(hard_dir):
                if file.endswith('.dat'):
                    file_path = os.path.join(hard_dir, file)
                    numbers, k = parse_dat_file(file_path)
                    
                    # 根据数字个数分类
                    n = len(numbers)
                    if n <= 100:
                        output_dir_size = tiny_dir
                    elif n <= 1000:
                        output_dir_size = small_dir
                    elif n <= 10000:
                        output_dir_size = medium_dir
                    else:
                        output_dir_size = large_dir
                    
                    # 写入文件
                    output_file = os.path.join(output_dir_size, file.replace('.dat', '.txt'))
                    write_txt_file(numbers, k, output_file, file.replace('.dat', ''))
                    print(f"处理: {file} -> {output_file}")
    
    # 处理其他文件
    for file in os.listdir(input_dir):
        if file.endswith('.dat') and not file.startswith('easy') and not file.startswith('hard'):
            file_path = os.path.join(input_dir, file)
            numbers, k = parse_dat_file(file_path)
            
            # 根据数字个数分类
            n = len(numbers)
            if n <= 100:
                output_dir_size = tiny_dir
            elif n <= 1000:
                output_dir_size = small_dir
            elif n <= 10000:
                output_dir_size = medium_dir
            else:
                output_dir_size = large_dir
            
            # 写入文件
            output_file = os.path.join(output_dir_size, file.replace('.dat', '.txt'))
            write_txt_file(numbers, k, output_file, file.replace('.dat', ''))
            print(f"处理: {file} -> {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Parse Number Partitioning datasets')
    parser.add_argument('--input', required=True, help='Input directory with raw NPP datasets')
    parser.add_argument('--output', required=True, help='Output directory for processed NPP datasets')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    
    print(f"开始处理数值划分数据集...")
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print("")
    
    # 处理NPP数据库
    process_npp_database(input_dir, output_dir)
    
    print("")
    print("处理完成！")


if __name__ == "__main__":
    main()