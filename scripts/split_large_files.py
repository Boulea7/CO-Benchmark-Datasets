#!/usr/bin/env python3
"""
分割大型文件的脚本
用于将超过GitHub大小限制的文件分割成较小的部分
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def split_file(file_path, chunk_size_mb=50, compression_level=6):
    """
    将大文件分割成压缩的小块
    
    Args:
        file_path: 要分割的文件路径
        chunk_size_mb: 每块的大小（MB）
        compression_level: xz压缩级别（0-9）
    """
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"错误: 文件 {file_path} 不存在")
        return False
    
    # 创建输出目录
    output_dir = file_path.parent / f"{file_path.name}.parts"
    output_dir.mkdir(exist_ok=True)
    
    # 计算块大小（字节）
    chunk_size = chunk_size_mb * 1024 * 1024
    
    print(f"正在分割文件: {file_path}")
    print(f"文件大小: {file_path.stat().st_size / (1024*1024):.1f} MB")
    print(f"块大小: {chunk_size_mb} MB")
    print(f"输出目录: {output_dir}")
    
    # 使用split命令分割文件
    base_name = file_path.name
    try:
        # 首先解压文件（如果是压缩文件）
        if file_path.suffix in ['.gz', '.gzip', '.bz2', '.xz']:
            print("检测到压缩文件，先解压...")
            temp_file = file_path.parent / f"{file_path.stem}.temp"
            
            if file_path.suffix in ['.gz', '.gzip']:
                cmd = ['gunzip', '-c', str(file_path)]
            elif file_path.suffix == '.bz2':
                cmd = ['bunzip2', '-c', str(file_path)]
            elif file_path.suffix == '.xz':
                cmd = ['xz', '-d', '-c', str(file_path)]
            
            with open(temp_file, 'wb') as f:
                subprocess.run(cmd, stdout=f, check=True)
            
            file_to_split = temp_file
        else:
            file_to_split = file_path
        
        # 分割文件
        split_cmd = [
            'split', '-b', str(chunk_size),
            str(file_to_split),
            str(output_dir / f"{base_name}.part")
        ]
        subprocess.run(split_cmd, check=True)
        
        # 清理临时文件
        if 'temp_file' in locals():
            temp_file.unlink()
        
        # 压缩每个部分
        part_files = sorted(output_dir.glob(f"{base_name}.part*"))
        for i, part_file in enumerate(part_files, 1):
            print(f"正在压缩部分 {i}/{len(part_files)}: {part_file.name}")
            
            # 使用xz压缩
            compressed_file = f"{part_file}.xz"
            compress_cmd = ['xz', f'-{compression_level}', str(part_file)]
            subprocess.run(compress_cmd, check=True)
        
        print(f"分割完成! 共 {len(part_files)} 个部分")
        
        # 创建重建脚本
        create_reconstruct_script(output_dir, base_name, part_files)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"错误: 分割文件失败 - {e}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def create_reconstruct_script(output_dir, base_name, part_files):
    """创建重建脚本"""
    script_path = output_dir / f"reconstruct_{base_name.replace('.', '_')}.sh"
    
    with open(script_path, 'w') as f:
        f.write(f"""#!/bin/bash
# 重建 {base_name} 的脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
OUTPUT_FILE="${{SCRIPT_DIR}}/../{base_name}"

echo "正在重建 {base_name}..."
echo "输出文件: $OUTPUT_FILE"

# 连接并解压所有部分
cat {" ".join([f'"{p.name}.xz"' for p in part_files])} | xz -d > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "重建成功: $OUTPUT_FILE"
    ls -lh "$OUTPUT_FILE"
else
    echo "重建失败"
    exit 1
fi
""")
    
    # 使脚本可执行
    os.chmod(script_path, 0o755)
    print(f"创建重建脚本: {script_path}")

def main():
    parser = argparse.ArgumentParser(description='分割大文件以符合GitHub大小限制')
    parser.add_argument('files', nargs='+', help='要分割的文件路径')
    parser.add_argument('--chunk-size', type=int, default=50, 
                       help='每个块的大小（MB，默认50）')
    parser.add_argument('--compression-level', type=int, default=6,
                       help='xz压缩级别（0-9，默认6）')
    
    args = parser.parse_args()
    
    for file_path in args.files:
        success = split_file(file_path, args.chunk_size, args.compression_level)
        if not success:
            sys.exit(1)
    
    print("\n所有文件分割完成!")
    print("注意: 分割后的原始大文件应该从git中移除，只保留分割后的部分")

if __name__ == '__main__':
    main()