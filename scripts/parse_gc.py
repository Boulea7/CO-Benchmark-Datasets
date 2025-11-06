#!/usr/bin/env python3
"""
图着色（Graph Coloring）数据解析器
处理DIMACS/COLOR格式的数据，转换为统一格式
"""

import os
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any, Set
import re


def parse_col_file(content: str) -> Tuple[int, int, List[Tuple[int, int, int]]]:
    """
    解析DIMACS/COLOR格式的图数据
    
    Args:
        content: 文件内容字符串
        
    Returns:
        (n, m, edges): 节点数、边数、边列表
    """
    lines = content.strip().split('\n')
    
    n = 0
    m = 0
    edges = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 跳过注释行（以c开头）
        if line.startswith('c'):
            continue
            
        # 解析问题行：p edge n m
        if line.startswith('p'):
            parts = line.split()
            if len(parts) >= 4 and parts[1] == 'edge':
                n = int(parts[2])
                m = int(parts[3])
            continue
            
        # 解析边：e u v
        if line.startswith('e'):
            parts = line.split()
            if len(parts) >= 3:
                u = int(parts[1])
                v = int(parts[2])
                # 添加边，权重为1（无权图）
                edges.append((u, v, 1))
    
    return n, len(edges), edges


def parse_col_binary_file(content: str) -> Tuple[int, int, List[Tuple[int, int, int]]]:
    """
    解析DIMACS/COLOR二进制格式的图数据(.col.b)
    
    Args:
        content: 文件内容字符串
        
    Returns:
        (n, m, edges): 节点数、边数、边列表
    """
    lines = content.strip().split('\n')
    
    n = 0
    m = 0
    edges = []
    
    # 解析文本部分
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 跳过注释行（以c开头）
        if line.startswith('c'):
            continue
            
        # 解析问题行：p edge n m
        if line.startswith('p'):
            parts = line.split()
            if len(parts) >= 4 and parts[1] == 'edge':
                n = int(parts[2])
                m = int(parts[3])
            continue
            
        # 如果遇到非文本行（包含非ASCII字符），停止解析文本部分
        try:
            line.encode('ascii')
        except UnicodeEncodeError:
            break
    
    # 如果没有找到p edge行，尝试从第一行获取节点数
    if n == 0 and lines:
        try:
            n = int(lines[0].strip())
        except ValueError:
            pass
    
    # 对于二进制格式的边，我们无法直接解析，但可以返回已知信息
    # 实际应用中，这些文件通常有对应的.col文件
    return n, m, edges


def parse_col_binary_file_advanced(file_path: str) -> Tuple[int, int, List[Tuple[int, int, int]]]:
    """
    高级解析DIMACS/COLOR二进制格式的图数据(.col.b)
    尝试解析二进制边数据
    
    Args:
        file_path: 文件路径
        
    Returns:
        (n, m, edges): 节点数、边数、边列表
    """
    import struct
    
    n = 0
    m = 0
    edges = []
    
    try:
        with open(file_path, 'rb') as f:
            # 读取文件内容
            content = f.read()
            
            # 先尝试解析文本部分
            text_content = content.decode('latin-1', errors='ignore')
            lines = text_content.split('\n')
            
            # 解析文本部分
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # 跳过注释行（以c开头）
                if line.startswith('c'):
                    continue
                    
                # 解析问题行：p edge n m
                if line.startswith('p'):
                    parts = line.split()
                    if len(parts) >= 4 and parts[1] == 'edge':
                        n = int(parts[2])
                        m = int(parts[3])
                    continue
            
            # 找到二进制部分的起始位置
            # 查找"p edge"行后的位置
            p_edge_pos = text_content.find('p edge')
            binary_start = -1
            
            if p_edge_pos >= 0:
                # 找到p edge行后的换行符
                newline_pos = text_content.find('\n', p_edge_pos)
                if newline_pos >= 0:
                    # 二进制数据从换行符后开始
                    binary_start = newline_pos + 1
                    
                    # 跳过可能的空字节或非数据字节
                    while (binary_start < len(content) and
                           (content[binary_start] == 0 or
                            content[binary_start] == 10 or  # \n
                            content[binary_start] == 13)):  # \r
                        binary_start += 1
            
            # 尝试解析二进制边数据
            if binary_start > 0 and binary_start < len(content):
                binary_data = content[binary_start:]
                
                # DIMACS二进制格式使用14位编码来存储边
                # 每个节点用7位表示（最多128个节点）
                # 一条边需要14位（2个节点）
                edges = parse_dimacs_binary_edges(binary_data, n, m)
                
                # 更新实际边数
                if len(edges) > 0:
                    m = len(edges)
                    print(f"Successfully parsed {len(edges)} edges from binary format")
                else:
                    print(f"Warning: Could not parse binary edges, falling back to text parsing")
    
    except Exception as e:
        print(f"Error parsing binary file {file_path}: {e}")
    
    return n, m, edges


def parse_dimacs_binary_edges(binary_data: bytes, n: int, m: int) -> List[Tuple[int, int, int]]:
    """
    解析DIMACS二进制格式的边数据
    使用14位编码：每个节点7位，一条边14位
    
    Args:
        binary_data: 二进制数据
        n: 节点数
        m: 预期边数
        
    Returns:
        边列表
    """
    edges = []
    i = 0
    bit_buffer = 0
    bits_available = 0
    
    # 计算需要的位数
    bits_per_node = 7
    if n > 127:
        bits_per_node = 8  # 对于大于127的节点，使用8位
    elif n > 63:
        bits_per_node = 7  # 64-127节点，使用7位
    elif n > 31:
        bits_per_node = 6  # 32-63节点，使用6位
    
    bits_per_edge = bits_per_node * 2
    
    while i < len(binary_data) and len(edges) < m:
        # 确保缓冲区中有足够的位
        while bits_available < bits_per_edge and i < len(binary_data):
            bit_buffer |= (binary_data[i] << bits_available)
            bits_available += 8
            i += 1
        
        if bits_available >= bits_per_edge:
            # 提取边数据
            edge_bits = bit_buffer & ((1 << bits_per_edge) - 1)
            
            # 解析两个节点
            u = (edge_bits & ((1 << bits_per_node) - 1)) + 1
            v = ((edge_bits >> bits_per_node) & ((1 << bits_per_node) - 1)) + 1
            
            # 验证节点有效性
            if 1 <= u <= n and 1 <= v <= n and u != v:
                edges.append((u, v, 1))
            
            # 移除已使用的位
            bit_buffer >>= bits_per_edge
            bits_available -= bits_per_edge
        else:
            break  # 没有足够的数据
    
    return edges


def try_parse_4byte_edges(binary_data: bytes, n: int, m: int) -> List[Tuple[int, int, int]]:
    """
    尝试将二进制数据解析为4字节边（2字节u, 2字节v）
    """
    import struct
    edges = []
    
    edge_size = 4
    max_edges = min(len(binary_data) // edge_size, m)
    
    for i in range(max_edges):
        start = i * edge_size
        if start + edge_size <= len(binary_data):
            edge_bytes = binary_data[start:start+edge_size]
            
            try:
                # 尝试小端序
                u, v = struct.unpack('<HH', edge_bytes)
                if 1 <= u <= n and 1 <= v <= n and u != v:
                    edges.append((u, v, 1))
            except:
                try:
                    # 尝试大端序
                    u, v = struct.unpack('>HH', edge_bytes)
                    if 1 <= u <= n and 1 <= v <= n and u != v:
                        edges.append((u, v, 1))
                except:
                    continue
    
    return edges


def try_parse_variable_length_edges(binary_data: bytes, n: int, m: int) -> List[Tuple[int, int, int]]:
    """
    尝试将二进制数据解析为变长编码的边
    """
    import struct
    edges = []
    
    i = 0
    while i < len(binary_data) - 1 and len(edges) < m:
        try:
            # 尝试读取变长整数
            u = read_variable_length_int(binary_data, i)
            i += get_variable_length_size(binary_data, i)
            
            if i >= len(binary_data):
                break
                
            v = read_variable_length_int(binary_data, i)
            i += get_variable_length_size(binary_data, i)
            
            if 1 <= u <= n and 1 <= v <= n and u != v:
                edges.append((u, v, 1))
        except:
            i += 1  # 跳过当前字节，继续尝试
    
    return edges


def try_parse_bitstream_edges(binary_data: bytes, n: int, m: int) -> List[Tuple[int, int, int]]:
    """
    尝试将二进制数据解析为位流格式的边
    """
    import struct
    edges = []
    
    # 将二进制数据视为位流，尝试提取边信息
    # 这是一种启发式方法，可能不适用于所有格式
    
    # 尝试不同的字节对组合
    for i in range(0, len(binary_data) - 3, 2):
        if len(edges) >= m:
            break
            
        chunk = binary_data[i:i+4] if i+4 <= len(binary_data) else binary_data[i:]
        
        # 尝试多种解析方式
        for byte_order in ['<', '>']:
            for fmt in ['HH', 'BB', 'HB', 'BH']:
                try:
                    if len(chunk) >= struct.calcsize(fmt):
                        values = struct.unpack(byte_order + fmt, chunk)
                        if len(values) >= 2:
                            u, v = values[0], values[1]
                            if 1 <= u <= n and 1 <= v <= n and u != v:
                                edges.append((u, v, 1))
                                break
                except:
                    continue
            
            if len(edges) > 0 and edges[-1][0] == u and edges[-1][1] == v:
                break  # 避免重复添加同一条边
    
    return edges


def read_variable_length_int(data: bytes, pos: int) -> int:
    """
    从指定位置读取变长整数
    """
    if pos >= len(data):
        raise ValueError("Position out of bounds")
    
    # 简单的变长整数解码：最高位表示是否继续
    result = 0
    shift = 0
    
    while pos < len(data):
        byte = data[pos]
        result |= (byte & 0x7F) << shift
        pos += 1
        
        if (byte & 0x80) == 0:
            break
            
        shift += 7
        if shift >= 32:
            break  # 防止无限循环
    
    return result


def get_variable_length_size(data: bytes, pos: int) -> int:
    """
    获取变长整数的字节长度
    """
    if pos >= len(data):
        return 0
    
    size = 1
    while pos + size < len(data) and (data[pos + size - 1] & 0x80):
        size += 1
        if size > 5:  # 最多5字节
            break
    
    return size


def write_txt_file(n: int, m: int, edges: List[Tuple[int, int, int]], 
                  output_path: str, name: str, k: int = 0):
    """
    将图数据写入统一文本格式
    
    Args:
        n: 节点数
        m: 边数
        edges: 边列表
        output_path: 输出文件路径
        name: 实例名称
        k: 颜色数（未知时为0）
    """
    with open(output_path, 'w') as f:
        # 写入头部信息
        f.write(f"# problem: graph_coloring\n")
        f.write(f"# name: {name}\n")
        f.write(f"# n: {n}\n")
        f.write(f"# m: {m}\n")
        f.write(f"# k: {k}\n")
        f.write(f"# weighted: 0\n")
        f.write(f"# directed: 0\n")
        f.write(f"{n} {m}\n")
        
        # 写入边
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")


def get_size_category(n: int) -> str:
    """
    根据节点数确定规模分类
    
    Args:
        n: 节点数
        
    Returns:
        规模分类：tiny, small, medium, large, xlarge
    """
    if n < 1000:
        return "tiny"
    elif n < 10000:
        return "small"
    elif n < 100000:
        return "medium"
    elif n < 1000000:
        return "large"
    else:
        return "xlarge"


def process_col_file(input_path: str, output_base_dir: str, 
                   processed_signatures: Dict[str, Set[str]] = None):
    """
    处理单个.col文件
    
    Args:
        input_path: 输入文件路径
        output_base_dir: 输出基础目录
        processed_signatures: 已处理的图签名（用于去重）
    """
    if processed_signatures is None:
        processed_signatures = {"tiny": set(), "small": set(), "medium": set(), "large": set(), "xlarge": set()}
    
    print(f"Processing {input_path}...")
    
    # 读取文件内容
    try:
        with open(input_path, 'r') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 如果是二进制文件，尝试用latin-1编码读取
        with open(input_path, 'rb') as f:
            content = f.read().decode('latin-1', errors='ignore')
    
    # 根据文件扩展名选择解析方法
    if input_path.endswith('.col.b'):
        # 二进制格式，尝试使用对应的.col文件
        base_path = input_path[:-2]  # 去掉.b
        col_path = f"{base_path}.col"
        
        if os.path.exists(col_path):
            print(f"  Using corresponding .col file: {col_path}")
            with open(col_path, 'r') as f:
                col_content = f.read()
            n, m, edges = parse_col_file(col_content)
        else:
            print(f"  No corresponding .col file found, parsing binary format")
            n, m, edges = parse_col_binary_file_advanced(input_path)
    else:
        # 标准格式
        n, m, edges = parse_col_file(content)
    
    # 生成图签名（节点数和边数的组合）
    signature = f"{n}_{m}"
    size_category = get_size_category(n)
    
    # 检查是否已处理过相同签名的图
    if signature in processed_signatures[size_category]:
        print(f"Skipping duplicate graph with signature {signature} in category {size_category}")
        return processed_signatures
    
    # 确定输出目录
    output_dir = os.path.join(output_base_dir, size_category)
    os.makedirs(output_dir, exist_ok=True)
    
    # 确定输出文件名
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}.txt")
    
    # 写入统一格式
    write_txt_file(n, m, edges, output_path, base_name)
    
    # 记录已处理的签名
    processed_signatures[size_category].add(signature)
    
    print(f"Saved to {output_path} (n={n}, m={m}, category={size_category})")
    
    return processed_signatures


def process_dimacs_directory(input_dir: str, output_dir: str):
    """
    处理DIMACS目录中的所有.col文件
    
    Args:
        input_dir: DIMACS输入目录
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 用于去重的签名记录
    processed_signatures = {
        "tiny": set(), 
        "small": set(), 
        "medium": set(), 
        "large": set(), 
        "xlarge": set()
    }
    
    # 查找所有.col文件（包括.col和.col.b）
    col_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if (file.endswith('.col') or file.endswith('.col.b')):
                input_path = os.path.join(root, file)
                col_files.append(input_path)
    
    # 处理每个文件
    for input_path in col_files:
        processed_signatures = process_col_file(input_path, output_dir, processed_signatures)
    
    # 输出统计信息
    total_files = 0
    for category, signatures in processed_signatures.items():
        count = len(signatures)
        total_files += count
        print(f"{category}: {count} files")
    
    print(f"Total processed: {total_files} files")


def process_roars_directory(input_dir: str, output_dir: str):
    """
    处理ROARS目录中的图着色文件
    
    Args:
        input_dir: ROARS输入目录
        output_dir: 输出目录
    """
    # ROARS处理逻辑（如果存在ROARS数据集）
    if not os.path.exists(input_dir):
        print(f"ROARS directory not found: {input_dir}")
        return
    
    print("Processing ROARS datasets...")
    process_dimacs_directory(input_dir, output_dir)


def main():
    parser = argparse.ArgumentParser(description='Process graph coloring datasets')
    parser.add_argument('--input', required=True, help='Input directory containing raw GC datasets')
    parser.add_argument('--output', required=True, help='Output directory for processed GC datasets')
    parser.add_argument('--datasets', nargs='+', 
                       choices=['dimacs', 'roars', 'all'],
                       default=['all'],
                       help='Which datasets to process')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理指定的数据集
    if 'all' in args.datasets or 'dimacs' in args.datasets:
        dimacs_dir = os.path.join(input_dir, 'DIMACS')
        if os.path.exists(dimacs_dir):
            print("Processing DIMACS datasets...")
            process_dimacs_directory(dimacs_dir, output_dir)
        elif os.path.basename(input_dir) == 'DIMACS' or any('DIMACS' in path for path in input_dir.split('/')):
            # 如果输入目录本身就是DIMACS或其子目录
            print("Processing DIMACS datasets...")
            process_dimacs_directory(input_dir, output_dir)
        else:
            print(f"DIMACS directory not found: {dimacs_dir}")
    
    if 'all' in args.datasets or 'roars' in args.datasets:
        roars_dir = os.path.join(input_dir, 'ROARS')
        if os.path.exists(roars_dir):
            print("Processing ROARS datasets...")
            process_roars_directory(roars_dir, output_dir)
        elif os.path.basename(input_dir) == 'ROARS' or any('ROARS' in path for path in input_dir.split('/')):
            # 如果输入目录本身就是ROARS或其子目录
            print("Processing ROARS datasets...")
            process_roars_directory(input_dir, output_dir)
        else:
            print(f"ROARS directory not found: {roars_dir}")
    
    print("Processing completed!")


if __name__ == "__main__":
    main()