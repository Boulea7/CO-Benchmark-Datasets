#!/usr/bin/env python3
"""
图划分数据解析器
处理DIMACS10 (.graph) 和 SuiteSparse (.mtx) 格式的数据，转换为统一格式
"""

import os
import bz2
import gzip
import tarfile
import zipfile
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any
import re


def parse_dimacs_graph(content: str) -> Tuple[int, int, List[Tuple[int, int, int]]]:
    """
    解析DIMACS10格式的图数据
    
    Args:
        content: 文件内容字符串
        
    Returns:
        (n, m, edges): 节点数、边数、边列表
    """
    lines = content.strip().split('\n')
    
    # 跳过注释行（以%开头）
    i = 0
    while i < len(lines) and lines[i].startswith('%'):
        i += 1
    
    # 第一行: n m 0 (最后的0可能表示无向图)
    first_line = lines[i].strip().split()
    n = int(first_line[0])
    m = int(first_line[1])
    
    edges = []
    
    # 解析邻接列表格式
    for j, line in enumerate(lines[i+1:], i+1):
        if not line.strip():
            continue
            
        neighbors = list(map(int, line.strip().split()))
        
        # 每行格式: 节点j的邻居列表
        for neighbor in neighbors:
            if neighbor > j:  # 避免重复边，只保留j < neighbor的边
                edges.append((j, neighbor, 1))
    
    return n, len(edges), edges


def parse_mtx_matrix(content: str) -> Tuple[int, int, List[Tuple[int, int, int]]]:
    """
    解析Matrix Market格式的矩阵数据
    
    Args:
        content: 文件内容字符串
        
    Returns:
        (n, m, edges): 节点数、边数、边列表
    """
    lines = content.strip().split('\n')
    
    # 跳过注释行
    i = 0
    while i < len(lines) and lines[i].startswith('%'):
        i += 1
    
    # 读取矩阵头信息
    header = lines[i].strip().split()
    
    # 检查矩阵类型
    if len(header) >= 4 and header[1] == 'array':
        # array格式，不是coordinate格式，跳过
        print("Skipping array format matrix (not coordinate format)")
        return 0, 0, []
    
    # 读取矩阵维度和非零元素数
    if len(header) >= 3:
        try:
            n_rows, n_cols, n_nonzeros = map(int, header[:3])
        except ValueError:
            # 可能只有两个值（对于某些特殊格式）
            n_rows, n_cols = map(int, header[:2])
            n_nonzeros = 0
    else:
        print(f"Invalid matrix header: {header}")
        return 0, 0, []
    
    # 对于对称矩阵，我们保留所有边，然后去重
    edges = []
    
    for j in range(i + 1, len(lines)):
        if not lines[j].strip() or lines[j].startswith('%'):
            continue
            
        parts = lines[j].strip().split()
        if len(parts) >= 2:
            try:
                row, col = int(parts[0]), int(parts[1])
                
                # 跳过对角线元素（自环）
                if row != col:
                    weight = abs(float(parts[2])) if len(parts) > 2 else 1
                    edges.append((row, col, int(weight)))
            except ValueError:
                continue
    
    # 去重并规范化边顺序（确保u <= v）
    unique_edges = {}
    for u, v, w in edges:
        if u > v:
            u, v = v, u
        unique_edges[(u, v)] = (u, v, w)
    
    edges = list(unique_edges.values())
    
    return max(n_rows, n_cols), len(edges), edges


def process_graph_file(input_path: str, output_path: str, name: str = None, k: int = 2):
    """
    处理单个图文件
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        name: 实例名称
        k: 划分数
    """
    print(f"Processing {input_path}...")
    
    # 确定文件类型
    if input_path.endswith('.graph') or input_path.endswith('.graph.bz2'):
        # DIMACS10格式
        if input_path.endswith('.bz2'):
            with bz2.open(input_path, 'rt') as f:
                content = f.read()
        else:
            with open(input_path, 'r') as f:
                content = f.read()
        
        n, m, edges = parse_dimacs_graph(content)
        
    elif input_path.endswith('.mtx'):
        # SuiteSparse Matrix Market格式
        with open(input_path, 'r') as f:
            content = f.read()
        
        n, m, edges = parse_mtx_matrix(content)
        
    else:
        print(f"Unsupported file format: {input_path}")
        return
    
    # 写入统一格式
    with open(output_path, 'w') as f:
        f.write(f"# problem: graph_partitioning\n")
        f.write(f"# name: {name or os.path.basename(input_path)}\n")
        f.write(f"# n: {n}\n")
        f.write(f"# m: {m}\n")
        f.write(f"# k: {k}\n")
        f.write(f"# weighted: 0\n")
        f.write(f"# directed: 0\n")
        f.write(f"{n} {m}\n")
        
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")
    
    print(f"Saved to {output_path} (n={n}, m={m})")


def extract_and_process_archive(archive_path: str, output_dir: str, k: int = 2):
    """
    解压并处理归档文件
    
    Args:
        archive_path: 归档文件路径
        output_dir: 输出目录
        k: 划分数
    """
    base_name = os.path.basename(archive_path)
    name_without_ext = os.path.splitext(base_name)[0]
    
    # 创建临时目录
    temp_dir = f"/tmp/{name_without_ext}"
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        if archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(temp_dir)
        elif archive_path.endswith('.tar.bz2') or archive_path.endswith('.tbz2'):
            with tarfile.open(archive_path, 'r:bz2') as tar:
                tar.extractall(temp_dir)
        elif archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        else:
            print(f"Unsupported archive format: {archive_path}")
            return
        
        # 查找.mtx文件
        processed_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.mtx') and not file.endswith('_coord.mtx'):
                    input_path = os.path.join(root, file)
                    
                    # 使用原始文件名作为输出名，但去掉.mtx扩展名
                    mtx_name = os.path.splitext(file)[0]
                    output_name = f"{name_without_ext}_{mtx_name}.txt"
                    output_path = os.path.join(output_dir, output_name)
                    
                    # 处理文件
                    n, m, edges = parse_mtx_matrix(open(input_path, 'r').read())
                    
                    # 只有当有边时才保存
                    if n > 0 and m > 0:
                        # 写入统一格式
                        with open(output_path, 'w') as f:
                            f.write(f"# problem: graph_partitioning\n")
                            f.write(f"# name: {name_without_ext}_{mtx_name}\n")
                            f.write(f"# n: {n}\n")
                            f.write(f"# m: {m}\n")
                            f.write(f"# k: {k}\n")
                            f.write(f"# weighted: 0\n")
                            f.write(f"# directed: 0\n")
                            f.write(f"{n} {m}\n")
                            
                            for u, v, w in edges:
                                f.write(f"{u} {v} {w}\n")
                        
                        print(f"Saved to {output_path} (n={n}, m={m})")
                        processed_files.append(output_path)
        
        if not processed_files:
            print(f"No valid coordinate matrix files found in {archive_path}")
    
    finally:
        # 清理临时目录
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


def process_dimacs10_directory(input_dir: str, output_dir: str, k: int = 2):
    """
    处理DIMACS10目录中的所有.graph文件
    
    Args:
        input_dir: DIMACS10输入目录
        output_dir: 输出目录
        k: 划分数
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 如果输入目录直接包含.graph文件，处理当前目录
    # 如果输入目录是DIMACS10的父目录，查找所有子目录中的.graph文件
    graph_files = []
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.graph.bz2'):
                input_path = os.path.join(root, file)
                graph_files.append(input_path)
    
    for input_path in graph_files:
        file = os.path.basename(input_path)
        output_name = file.replace('.graph.bz2', '.txt')
        output_path = os.path.join(output_dir, output_name)
        
        # 解压并处理
        print(f"Extracting {input_path}...")
        with bz2.open(input_path, 'rt') as f:
            content = f.read()
        
        n, m, edges = parse_dimacs_graph(content)
        
        # 写入统一格式
        with open(output_path, 'w') as f:
            f.write(f"# problem: graph_partitioning\n")
            f.write(f"# name: {file.replace('.graph.bz2', '')}\n")
            f.write(f"# n: {n}\n")
            f.write(f"# m: {m}\n")
            f.write(f"# k: {k}\n")
            f.write(f"# weighted: 0\n")
            f.write(f"# directed: 0\n")
            f.write(f"{n} {m}\n")
            
            for u, v, w in edges:
                f.write(f"{u} {v} {w}\n")
        
        print(f"Saved to {output_path} (n={n}, m={m})")


def process_suitesparse_directory(input_dir: str, output_dir: str, k: int = 2):
    """
    处理SuiteSparse目录中的所有归档文件
    
    Args:
        input_dir: SuiteSparse输入目录
        output_dir: 输出目录
        k: 划分数
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.tar.gz') or file.endswith('.tgz'):
                input_path = os.path.join(root, file)
                extract_and_process_archive(input_path, output_dir, k)


def main():
    parser = argparse.ArgumentParser(description='Process graph partitioning datasets')
    parser.add_argument('--input', required=True, help='Input directory containing raw datasets')
    parser.add_argument('--output', required=True, help='Output directory for processed datasets')
    parser.add_argument('--k', type=int, default=2, help='Number of partitions')
    parser.add_argument('--datasets', nargs='+', 
                       choices=['dimacs10', 'suitesparse', 'all'],
                       default=['all'],
                       help='Which datasets to process')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    k = args.k
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理指定的数据集
    if 'all' in args.datasets or 'dimacs10' in args.datasets:
        dimacs10_dir = os.path.join(input_dir, 'DIMACS10')
        if os.path.exists(dimacs10_dir):
            print("Processing DIMACS10 datasets...")
            process_dimacs10_directory(dimacs10_dir, output_dir, k)
        elif os.path.basename(input_dir) == 'DIMACS10' or any('DIMACS10' in path for path in input_dir.split('/')):
            # 如果输入目录本身就是DIMACS10或其子目录
            print("Processing DIMACS10 datasets...")
            process_dimacs10_directory(input_dir, output_dir, k)
        else:
            print(f"DIMACS10 directory not found: {dimacs10_dir}")
    
    if 'all' in args.datasets or 'suitesparse' in args.datasets:
        suitesparse_dir = os.path.join(input_dir, 'SuiteSparse')
        if os.path.exists(suitesparse_dir):
            print("Processing SuiteSparse datasets...")
            process_suitesparse_directory(suitesparse_dir, output_dir, k)
        elif os.path.basename(input_dir) == 'SuiteSparse' or any('SuiteSparse' in path for path in input_dir.split('/')):
            # 如果输入目录本身就是SuiteSparse或其子目录
            print("Processing SuiteSparse datasets...")
            process_suitesparse_directory(input_dir, output_dir, k)
        else:
            print(f"SuiteSparse directory not found: {suitesparse_dir}")
    
    print("Processing completed!")


if __name__ == "__main__":
    main()