#!/bin/bash
# 简单解压脚本
# 使用方法：./scripts/simple_decompress.sh

echo "=========================================="
echo "CO-Benchmark-Datasets 简单解压脚本"
echo "=========================================="
echo ""

# 设置参数
COMPRESSED_DIR="processed/graph_partitioning/compressed"
OUTPUT_DIR="processed/graph_partitioning/decompressed"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "压缩目录: $COMPRESSED_DIR"
echo "输出目录: $OUTPUT_DIR"
echo ""

# 检查压缩目录是否存在
if [ ! -d "$COMPRESSED_DIR" ]; then
    echo "错误: 压缩目录不存在: $COMPRESSED_DIR"
    exit 1
fi

# 解压所有文件
echo "开始解压所有压缩文件..."
echo ""

# 解压gzip文件
echo "解压gzip文件..."
find "$COMPRESSED_DIR" -name "*.gz" -exec sh -c '
    file="$1"
    filename=$(basename "$file" .gz)
    output_dir="'$OUTPUT_DIR'/$(dirname "$file" | sed "s|'$COMPRESSED_DIR'/||")"
    mkdir -p "$output_dir"
    gunzip -c "$file" > "$output_dir/$filename"
    echo "✓ 解压: $filename"
' sh {} \;

# 解压xz文件
echo ""
echo "解压xz文件..."
find "$COMPRESSED_DIR" -name "*.xz" -exec sh -c '
    file="$1"
    filename=$(basename "$file" .xz)
    output_dir="'$OUTPUT_DIR'/$(dirname "$file" | sed "s|'$COMPRESSED_DIR'/||")"
    mkdir -p "$output_dir"
    unxz -c "$file" > "$output_dir/$filename"
    echo "✓ 解压: $filename"
' sh {} \;

echo ""
echo "=========================================="
echo "解压完成！"
echo "=========================================="
echo ""
echo "解压文件保存在: $OUTPUT_DIR"
echo ""
echo "按规模分类的文件数量:"
for dir in tiny small medium large xlarge; do
    if [ -d "$OUTPUT_DIR/$dir" ]; then
        count=$(find "$OUTPUT_DIR/$dir" -name "*.txt" | wc -l)
        echo "$dir: $count 个文件"
    fi
done