#!/bin/bash

# 重建大型分割文件的脚本
# 此脚本帮助重建因GitHub文件大小限制而被分割的原始大型图文件

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ERDOS_DIR="$PROJECT_ROOT/raw/graph_partitioning/DIMACS10/Erdös-Rényi Graphs"

# 输出颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # 无颜色

# 打印彩色消息的函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 从部分文件重建文件的函数
reconstruct_file() {
    local base_name="$1"
    local output_dir="$2"
    
    print_info "正在重建 $base_name..."
    
    # 检查部分文件是否存在
    local parts=("$ERDOS_DIR/${base_name}.part"*.xz)
    if [ ! -e "${parts[0]}" ]; then
        print_error "未找到 $base_name 的部分文件"
        return 1
    fi
    
    local part_count=$(ls -1 "$ERDOS_DIR/${base_name}.part"*.xz 2>/dev/null | wc -l)
    print_info "找到 $part_count 个部分文件"
    
    # 重建文件
    local output_file="$output_dir/${base_name}"
    print_info "正在解压并连接部分文件..."
    cat "$ERDOS_DIR/${base_name}.part"*.xz | xz -d > "$output_file"
    
    if [ $? -eq 0 ]; then
        print_info "成功重建: $output_file"
        local size=$(du -h "$output_file" | cut -f1)
        print_info "文件大小: $size"
        return 0
    else
        print_error "重建 $base_name 失败"
        return 1
    fi
}

# 主脚本
main() {
    print_info "大型文件重建工具"
    print_info "================================"
    echo
    
    # 检查xz是否可用
    if ! command -v xz &> /dev/null; then
        print_error "未找到xz命令。请安装xz-utils。"
        exit 1
    fi
    
    # 询问用户要执行的操作
    echo "可重建的文件:"
    echo "  1) er-fact1.5-scale25.graph"
    echo "  2) er-fact1.5-scale26.graph"
    echo "  3) 两个文件"
    echo "  4) 退出"
    echo
    read -p "选择一个选项 (1-4): " choice
    
    # 创建输出目录
    OUTPUT_DIR="${OUTPUT_DIR:-$PROJECT_ROOT/reconstructed}"
    mkdir -p "$OUTPUT_DIR"
    print_info "输出目录: $OUTPUT_DIR"
    echo
    
    case $choice in
        1)
            reconstruct_file "er-fact1.5-scale25.graph" "$OUTPUT_DIR"
            ;;
        2)
            reconstruct_file "er-fact1.5-scale26.graph" "$OUTPUT_DIR"
            ;;
        3)
            reconstruct_file "er-fact1.5-scale25.graph" "$OUTPUT_DIR"
            reconstruct_file "er-fact1.5-scale26.graph" "$OUTPUT_DIR"
            ;;
        4)
            print_info "正在退出..."
            exit 0
            ;;
        *)
            print_error "无效选项"
            exit 1
            ;;
    esac
    
    echo
    print_info "完成!"
    print_info "重建的文件位于: $OUTPUT_DIR"
}

# 运行主函数
main
