#!/usr/bin/env python3
"""
数据集解压脚本
支持批量解压和选择性解压
"""

import os
import shutil
import gzip
import tarfile
import argparse
from pathlib import Path
from typing import List, Dict, Any


def decompress_gzip(input_path: str, output_path: str):
    """
    解压gzip文件
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
    """
    with gzip.open(input_path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def decompress_xz(input_path: str, output_dir: str):
    """
    解压xz文件
    
    Args:
        input_path: 输入文件路径
        output_dir: 输出目录
    """
    with tarfile.open(input_path, 'r:xz') as tar:
        tar.extractall(path=output_dir)


def decompress_file(input_path: str, output_dir: str, delete_original: bool = False):
    """
    解压单个文件
    
    Args:
        input_path: 输入文件路径
        output_dir: 输出目录
        delete_original: 是否删除原始压缩文件
    """
    file_name = os.path.basename(input_path)
    
    if input_path.endswith('.gz'):
        # 去掉.gz扩展名
        output_path = os.path.join(output_dir, file_name[:-3])
        decompress_gzip(input_path, output_path)
        print(f"✓ 解压gzip文件: {file_name} -> {os.path.basename(output_path)}")
    elif input_path.endswith('.xz'):
        # xz文件解压到目录
        decompress_xz(input_path, output_dir)
        print(f"✓ 解压xz文件: {file_name}")
    else:
        print(f"⚠️  跳过非压缩文件: {file_name}")
        return
    
    # 删除原始压缩文件
    if delete_original and os.path.exists(input_path):
        os.remove(input_path)
        print(f"  已删除原始压缩文件: {file_name}")


def decompress_directory(input_dir: str, output_dir: str, pattern: str = "*", delete_original: bool = False):
    """
    解压目录中的所有压缩文件
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        pattern: 文件模式（如"*.gz"或"*.xz"）
        delete_original: 是否删除原始压缩文件
    """
    import glob
    
    # 获取所有匹配的文件
    files = glob.glob(os.path.join(input_dir, pattern))
    
    if not files:
        print(f"没有找到匹配 '{pattern}' 的文件")
        return
    
    print(f"开始解压 {len(files)} 个文件...")
    
    for file_path in files:
        decompress_file(file_path, output_dir, delete_original)
    
    print(f"解压完成！共处理 {len(files)} 个文件")


def main():
    parser = argparse.ArgumentParser(description='Decompress datasets')
    parser.add_argument('--input', required=True, help='Input directory with compressed datasets')
    parser.add_argument('--output', required=True, help='Output directory for decompressed datasets')
    parser.add_argument('--pattern', default='*', help='File pattern to decompress (default: *)')
    parser.add_argument('--delete', action='store_true', help='Delete original compressed files after decompression')
    parser.add_argument('--recursive', action='store_true', help='Recursively decompress all subdirectories')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    pattern = args.pattern
    delete_original = args.delete
    recursive = args.recursive
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print(f"文件模式: {pattern}")
    print(f"删除原始文件: {delete_original}")
    print(f"递归处理: {recursive}")
    print("")
    
    if recursive:
        # 递归处理所有子目录
        for root, dirs, files in os.walk(input_dir):
            # 检查是否有匹配的文件
            import glob
            matched_files = glob.glob(os.path.join(root, pattern))
            
            if matched_files:
                # 创建对应的输出目录结构
                rel_path = os.path.relpath(root, input_dir)
                if rel_path == '.':
                    current_output_dir = output_dir
                else:
                    current_output_dir = os.path.join(output_dir, rel_path)
                
                os.makedirs(current_output_dir, exist_ok=True)
                
                # 解压当前目录的文件
                decompress_directory(root, current_output_dir, pattern, delete_original)
    else:
        # 只处理输入目录
        decompress_directory(input_dir, output_dir, pattern, delete_original)
    
    print("")
    print("解压完成！")


if __name__ == "__main__":
    main()