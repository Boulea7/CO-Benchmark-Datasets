#!/usr/bin/env python3
"""
数据集并行压缩脚本
使用多进程、混合压缩策略、进度显示和断点续传
"""

import os
import shutil
import gzip
import tarfile
import argparse
import multiprocessing as mp
from pathlib import Path
from typing import List, Tuple, Dict, Any
import time
import pickle
import signal
import sys


# 全局变量，用于断点续传
compression_state = {
    'completed_files': [],
    'failed_files': [],
    'total_files': 0,
    'current_file': '',
    'start_time': 0
}

# 状态文件路径
STATE_FILE = 'compression_state.pkl'


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)


def get_compression_type(file_path: str) -> str:
    """
    根据文件大小确定压缩类型
    
    Args:
        file_path: 文件路径
        
    Returns:
        压缩类型: gzip, xz
    """
    file_size = get_file_size(file_path)
    
    # 超大文件（>2GB）：使用gzip（速度快）
    if file_size > 2 * 1024 * 1024 * 1024:  # 2GB
        return 'gzip'
    # 大文件（500MB-2GB）：使用xz（平衡压缩比和速度）
    elif file_size > 500 * 1024 * 1024:  # 500MB
        return 'xz'
    # 中小文件（<500MB）：使用xz（高压缩比）
    else:
        return 'xz'


def compress_gzip(input_path: str, output_path: str) -> Tuple[int, float]:
    """
    使用gzip压缩文件
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        
    Returns:
        (compressed_size, ratio): 压缩后大小、压缩比
    """
    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    original_size = get_file_size(input_path)
    compressed_size = get_file_size(output_path)
    ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    
    return compressed_size, ratio


def compress_xz(input_path: str, output_path: str) -> Tuple[int, float]:
    """
    使用xz压缩文件
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        
    Returns:
        (compressed_size, ratio): 压缩后大小、压缩比
    """
    # 使用tar.xz格式压缩
    with tarfile.open(output_path, 'w:xz') as tar:
        tar.add(input_path, arcname=os.path.basename(input_path))
    
    original_size = get_file_size(input_path)
    compressed_size = get_file_size(output_path)
    ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    
    return compressed_size, ratio


def compress_file_worker(args: Tuple[str, str, str]) -> Tuple[str, int, float, bool]:
    """
    压缩文件的工作函数（用于多进程）
    
    Args:
        args: (input_path, output_path, compression_type)
        
    Returns:
        (file_path, compressed_size, ratio, success): 文件路径、压缩后大小、压缩比、是否成功
    """
    input_path, output_path, compression_type = args
    file_name = os.path.basename(input_path)
    
    try:
        start_time = time.time()
        
        if compression_type == 'gzip':
            compressed_size, ratio = compress_gzip(input_path, output_path)
        elif compression_type == 'xz':
            compressed_size, ratio = compress_xz(input_path, output_path)
        else:
            return file_name, 0, 0, False
        
        elapsed_time = time.time() - start_time
        
        # 更新全局状态
        with mp.Lock():
            compression_state['completed_files'].append(file_name)
            compression_state['current_file'] = file_name
        
        # 保存状态到文件
        save_state()
        
        return file_name, compressed_size, ratio, True
    
    except Exception as e:
        print(f"Error compressing {file_name}: {str(e)}")
        
        # 更新全局状态
        with mp.Lock():
            compression_state['failed_files'].append(file_name)
        
        # 保存状态到文件
        save_state()
        
        return file_name, 0, 0, False


def save_state():
    """保存压缩状态到文件"""
    with open(STATE_FILE, 'wb') as f:
        pickle.dump(compression_state, f)


def load_state():
    """从文件加载压缩状态"""
    global compression_state
    
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'rb') as f:
                compression_state = pickle.load(f)
            return True
        except Exception as e:
            print(f"Error loading state: {str(e)}")
    
    return False


def print_progress():
    """打印压缩进度"""
    completed = len(compression_state['completed_files'])
    failed = len(compression_state['failed_files'])
    total = compression_state['total_files']
    
    if total > 0:
        progress = (completed + failed) / total * 100
        print(f"\r进度: {progress:.1f}% ({completed} 完成, {failed} 失败, {total} 总计)", end='', flush=True)
        
        if compression_state['current_file']:
            print(f" 当前文件: {compression_state['current_file']}", end='', flush=True)


def signal_handler(signum, frame):
    """信号处理器，用于保存状态"""
    print("\n收到中断信号，保存状态...")
    save_state()
    sys.exit(0)


def compress_datasets_parallel(input_dir: str, output_dir: str, problem_type: str, workers: int = 4):
    """
    并行压缩数据集，按规模分类
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录
        problem_type: 问题类型
        workers: 工作进程数
    """
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 加载之前的状态
    state_loaded = load_state()
    if state_loaded:
        print(f"发现之前的压缩状态，已完成 {len(compression_state['completed_files'])} 个文件")
    
    # 创建压缩目录
    compressed_dir = os.path.join(output_dir, 'compressed')
    os.makedirs(compressed_dir, exist_ok=True)
    
    # 创建规模分类目录
    size_dirs = ['tiny', 'small', 'medium', 'large', 'xlarge']
    for size_dir in size_dirs:
        os.makedirs(os.path.join(compressed_dir, size_dir), exist_ok=True)
    
    # 获取所有数据文件
    data_files = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                data_files.append(os.path.join(root, file))
    
    # 过滤已完成的文件
    if state_loaded:
        completed_files = set(compression_state['completed_files'])
        data_files = [f for f in data_files if os.path.basename(f) not in completed_files]
    
    # 更新总文件数
    compression_state['total_files'] = len(data_files)
    compression_state['start_time'] = time.time()
    
    if not data_files:
        print("所有文件已压缩完成！")
        return
    
    print(f"开始压缩 {len(data_files)} 个文件，使用 {workers} 个进程...")
    
    # 准备工作参数
    work_args = []
    for file_path in data_files:
        file_name = os.path.basename(file_path)
        size_category = os.path.basename(os.path.dirname(file_path))
        compression_type = get_compression_type(file_path)
        
        output_path = os.path.join(compressed_dir, size_category, f"{file_name}.{compression_type}")
        
        work_args.append((file_path, output_path, compression_type))
    
    # 创建进程池
    with mp.Pool(workers) as pool:
        # 使用imap_unordered获取结果
        results = pool.imap_unordered(compress_file_worker, work_args)
        
        # 处理结果
        for result in results:
            file_name, compressed_size, ratio, success = result
            
            if success:
                # 删除原始文件（除了tiny和small）
                size_category = None
                for arg in work_args:
                    if file_name in arg[0]:
                        size_category = os.path.basename(os.path.dirname(arg[1]))
                        break
                
                if size_category and size_category not in ['tiny', 'small']:
                    input_path = None
                    for arg in work_args:
                        if file_name in arg[0]:
                            input_path = arg[0]
                            break
                    
                    if input_path and os.path.exists(input_path):
                        os.remove(input_path)
                        print(f"已删除原始文件: {file_name}")
            
            # 打印进度
            print_progress()
    
    # 完成压缩
    print("\n压缩完成！")
    
    # 生成压缩报告
    generate_compression_report(compressed_dir, problem_type, input_dir)
    
    # 创建使用指南
    create_usage_guide(compressed_dir, problem_type)
    
    # 清理状态文件
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    
    # 计算总时间
    total_time = time.time() - compression_state['start_time']
    print(f"总耗时: {total_time/60:.1f} 分钟")


def generate_compression_report(compressed_dir: str, problem_type: str, input_dir: str):
    """生成压缩报告"""
    report_path = os.path.join(compressed_dir, 'compression_report.txt')
    
    # 统计各规模分类的文件
    size_stats = {'tiny': [], 'small': [], 'medium': [], 'large': [], 'xlarge': []}
    
    for size_dir in size_stats.keys():
        dir_path = os.path.join(compressed_dir, size_dir)
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith('.gz') or file.endswith('.xz'):
                    file_path = os.path.join(dir_path, file)
                    compressed_size = get_file_size(file_path)
                    size_stats[size_dir].append((file, compressed_size))
    
    # 写入报告
    with open(report_path, 'w') as f:
        f.write(f"# {problem_type.replace('_', ' ').title()} 数据集压缩报告\n\n")
        
        # 计算总原始大小（从原始文件计算）
        total_original = 0
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    total_original += get_file_size(file_path)
        
        total_compressed = sum(size for files in size_stats.values() for _, size in files)
        total_ratio = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
        total_saved = total_original - total_compressed
        
        f.write(f"总原始大小: {total_original/1024/1024:.2f} MB\n")
        f.write(f"总压缩大小: {total_compressed/1024/1024:.2f} MB\n")
        f.write(f"总节省空间: {total_saved/1024/1024:.2f} MB ({total_ratio:.1f}%)\n\n")
        
        f.write("## 按规模分类统计\n\n")
        f.write("| 规模 | 文件数量 | 压缩大小 | 压缩格式 |\n")
        f.write("|------|--------|----------|----------|\n")
        
        for size_dir, files in size_stats.items():
            if not files:
                continue
                
            total_size = sum(size for _, size in files)
            compression_format = 'gzip' if files and files[0][0].endswith('.gz') else 'xz'
            
            f.write(f"| {size_dir} | {len(files)} | {total_size/1024/1024:.2f}MB | {compression_format} |\n")


def create_usage_guide(compressed_dir: str, problem_type: str):
    """创建使用指南"""
    guide_path = os.path.join(compressed_dir, 'USAGE.md')
    
    with open(guide_path, 'w') as f:
        f.write(f"# {problem_type.replace('_', ' ').title()} 压缩数据集使用指南\n\n")
        f.write("本目录包含压缩后的数据集，按规模分类。\n\n")
        
        f.write("## 目录结构\n\n")
        f.write("```\n")
        f.write(f"{compressed_dir}/\n")
        f.write("├── tiny/      # xz压缩，高压缩比\n")
        f.write("├── small/      # xz压缩，高压缩比\n")
        f.write("├── medium/     # xz压缩，平衡压缩比和解压速度\n")
        f.write("├── large/      # xz压缩，平衡压缩比和解压速度\n")
        f.write("└── xlarge/     # gzip/xz混合压缩，平衡速度和空间\n")
        f.write("├── compression_report.txt  # 压缩统计报告\n")
        f.write("└── USAGE.md              # 本文件\n")
        f.write("```\n\n")
        
        f.write("## 解压方法\n\n")
        f.write("### gzip文件\n")
        f.write("```bash\n")
        f.write("# 解压单个文件\n")
        f.write("gunzip file.txt.gz\n\n")
        f.write("# 解压整个目录\n")
        f.write("gunzip *.gz\n")
        f.write("```\n\n")
        
        f.write("### xz文件\n")
        f.write("```bash\n")
        f.write("# 解压单个文件\n")
        f.write("unxz file.txt.xz\n\n")
        f.write("# 解压整个目录\n")
        f.write("unxz *.xz\n")
        f.write("```\n\n")
        
        f.write("## Python中使用\n\n")
        f.write("```python\n")
        f.write("import gzip\n")
        f.write("import tarfile\n\n")
        f.write("# 解压gzip文件\n")
        f.write("with gzip.open('file.txt.gz', 'rt') as f:\n")
        f.write("    content = f.read()\n\n")
        f.write("# 解压xz文件\n")
        f.write("with tarfile.open('file.txt.xz', 'r:xz') as tar:\n")
        f.write("    with tar.extractfile(tar.getmember('file.txt')) as f:\n")
        f.write("        content = f.read().decode('utf-8')\n")
        f.write("```\n\n")
        
        f.write("## 注意事项\n\n")
        f.write("1. 所有原始文件已删除，请使用压缩版本\n")
        f.write("2. xz压缩文件需要更多时间解压，但压缩比更高\n")
        f.write("3. gzip压缩文件解压速度快，适合大文件\n")
        f.write("4. 建议根据使用频率选择合适的数据集规模\n")
        f.write("5. 如果压缩被中断，可以重新运行脚本，它会自动从断点继续\n")


def main():
    parser = argparse.ArgumentParser(description='Compress datasets in parallel with mixed compression strategy')
    parser.add_argument('--input', required=True, help='Input directory with organized datasets')
    parser.add_argument('--output', required=True, help='Output directory for compressed datasets')
    parser.add_argument('--problem', required=True, 
                       choices=['graph_partitioning', 'graph_coloring', 'number_partitioning'],
                       help='Problem type')
    parser.add_argument('--workers', type=int, default=mp.cpu_count(),
                       help='Number of worker processes (default: number of CPUs)')
    
    args = parser.parse_args()
    
    input_dir = args.input
    output_dir = args.output
    problem_type = args.problem
    workers = args.workers
    
    print(f"开始并行压缩 {problem_type} 数据集，使用 {workers} 个进程...")
    compress_datasets_parallel(input_dir, output_dir, problem_type, workers)
    print(f"压缩完成! 压缩数据集保存在 {output_dir}")


if __name__ == "__main__":
    main()