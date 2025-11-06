"""
数据解析器
用于将原始数据集转换为统一格式的.txt文件
"""

import os
import shutil
from typing import Dict, List, Tuple, Any
import networkx as nx
import numpy as np


class GraphParser:
    """图数据解析器基类"""
    
    def __init__(self, problem_type: str):
        self.problem_type = problem_type
    
    def parse_dimacs_graph(self, input_path: str, output_path: str, name: str = None, k: int = 0):
        """
        解析DIMACS格式的图数据（.col文件）
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            name: 实例名称
            k: 划分数/颜色数
        """
        edges = []
        n = 0
        m = 0
        
        with open(input_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('p edge'):
                    parts = line.split()
                    n = int(parts[2])
                    m = int(parts[3])
                elif line.startswith('e '):
                    parts = line.split()
                    u, v = int(parts[1]), int(parts[2])
                    edges.append((u, v, 1))  # 无权图，权重为1
        
        # 写入统一格式
        with open(output_path, 'w') as f:
            f.write(f"# problem: {self.problem_type}\n")
            f.write(f"# name: {name or os.path.basename(input_path)}\n")
            f.write(f"# n: {n}\n")
            f.write(f"# m: {len(edges)}\n")
            f.write(f"# k: {k}\n")
            f.write(f"# weighted: 0\n")
            f.write(f"# directed: 0\n")
            f.write(f"{n} {len(edges)}\n")
            
            for u, v, w in edges:
                f.write(f"{u} {v} {w}\n")
    
    def parse_metis_graph(self, input_path: str, output_path: str, name: str = None, k: int = 2):
        """
        解析METIS格式的图数据
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            name: 实例名称
            k: 划分数
        """
        edges = []
        n = 0
        
        with open(input_path, 'r') as f:
            lines = f.readlines()
            
        # 第一行包含节点数和边数
        first_line = lines[0].strip()
        n, m = map(int, first_line.split()[:2])
        
        # 解析边
        for i, line in enumerate(lines[1:n+1], 1):
            parts = line.strip().split()
            for part in parts:
                v = int(part)
                if v > i:  # 避免重复边
                    edges.append((i, v, 1))
        
        # 写入统一格式
        with open(output_path, 'w') as f:
            f.write(f"# problem: {self.problem_type}\n")
            f.write(f"# name: {name or os.path.basename(input_path)}\n")
            f.write(f"# n: {n}\n")
            f.write(f"# m: {len(edges)}\n")
            f.write(f"# k: {k}\n")
            f.write(f"# weighted: 0\n")
            f.write(f"# directed: 0\n")
            f.write(f"{n} {len(edges)}\n")
            
            for u, v, w in edges:
                f.write(f"{u} {v} {w}\n")


class NumberPartitioningParser:
    """数值划分数据解析器"""
    
    def parse_pedroso_kubo(self, input_path: str, output_path: str, name: str = None, k: int = 2):
        """
        解析Pedroso & Kubo格式的数值划分数据
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            name: 实例名称
            k: 划分数
        """
        values = []
        
        with open(input_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('%'):
                    values.extend(map(int, line.split()))
        
        n = len(values)
        
        # 写入统一格式
        with open(output_path, 'w') as f:
            f.write(f"# problem: number_partitioning\n")
            f.write(f"# name: {name or os.path.basename(input_path)}\n")
            f.write(f"# n: {n}\n")
            f.write(f"# k: {k}\n")
            f.write(f"{n}\n")
            
            for value in values:
                f.write(f"{value}\n")
    
    def generate_synthetic(self, output_path: str, n: int, value_range: Tuple[int, int], 
                          name: str = None, k: int = 2, distribution: str = "uniform"):
        """
        生成合成数值划分实例
        
        Args:
            output_path: 输出文件路径
            n: 数字个数
            value_range: 数值范围 (min, max)
            name: 实例名称
            k: 划分数
            distribution: 分布类型 ("uniform", "normal")
        """
        if distribution == "uniform":
            values = np.random.randint(value_range[0], value_range[1] + 1, n).tolist()
        elif distribution == "normal":
            mean = (value_range[0] + value_range[1]) / 2
            std = (value_range[1] - value_range[0]) / 6
            values = np.clip(np.random.normal(mean, std, n), value_range[0], value_range[1]).astype(int).tolist()
        else:
            raise ValueError(f"Unsupported distribution: {distribution}")
        
        # 写入统一格式
        with open(output_path, 'w') as f:
            f.write(f"# problem: number_partitioning\n")
            f.write(f"# name: {name or os.path.basename(output_path)}\n")
            f.write(f"# n: {n}\n")
            f.write(f"# k: {k}\n")
            f.write(f"# distribution: {distribution}\n")
            f.write(f"# range: {value_range[0]}-{value_range[1]}\n")
            f.write(f"{n}\n")
            
            for value in values:
                f.write(f"{value}\n")


def batch_convert_graphs(input_dir: str, output_dir: str, problem_type: str, 
                        file_pattern: str = "*.txt", k: int = 0):
    """
    批量转换图数据
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        problem_type: 问题类型
        file_pattern: 文件模式
        k: 划分数/颜色数
    """
    parser = GraphParser(problem_type)
    
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.col'):
            input_path = os.path.join(input_dir, filename)
            output_filename = filename.replace('.col', '.txt')
            output_path = os.path.join(output_dir, output_filename)
            
            parser.parse_dimacs_graph(input_path, output_path, filename[:-4], k)
            print(f"Converted {filename} to {output_filename}")
        
        elif filename.endswith('.graph') or filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            parser.parse_metis_graph(input_path, output_path, filename, k)
            print(f"Converted {filename}")


def batch_convert_npp(input_dir: str, output_dir: str, k: int = 2):
    """
    批量转换数值划分数据
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        k: 划分数
    """
    parser = NumberPartitioningParser()
    
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.dat') or filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.dat', '.txt'))
            
            parser.parse_pedroso_kubo(input_path, output_path, filename, k)
            print(f"Converted {filename} to {output_path.replace('.dat', '.txt')}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert datasets to unified format')
    parser.add_argument('--type', choices=['graph_partitioning', 'graph_coloring', 'number_partitioning'], 
                       required=True, help='Problem type')
    parser.add_argument('--input', required=True, help='Input directory')
    parser.add_argument('--output', required=True, help='Output directory')
    parser.add_argument('--k', type=int, default=0, help='Number of partitions/colors')
    
    args = parser.parse_args()
    
    if args.type in ['graph_partitioning', 'graph_coloring']:
        batch_convert_graphs(args.input, args.output, args.type, k=args.k)
    elif args.type == 'number_partitioning':
        batch_convert_npp(args.input, args.output, k=args.k)