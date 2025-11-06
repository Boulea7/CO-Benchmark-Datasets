#!/usr/bin/env python3
"""
统一加载器使用示例
演示如何使用 unified_loader.py 加载不同类型的数据集
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unified_loader import load_graph_txt, load_npp_txt, load_instance, batch_load_instances


def example_graph_partitioning():
    """示例：加载图划分数据"""
    print("=== 图划分数据示例 ===")
    
    # 加载图数据
    graph = load_graph_txt("processed/graph_partitioning/compressed/tiny/dolphins.txt.xz")
    
    print(f"图名称: {graph.name}")
    print(f"节点数: {graph.n}")
    print(f"边数: {graph.m}")
    print(f"前5条边: {graph.edges[:5]}")
    print(f"元数据: {graph.meta}")
    print()


def example_number_partitioning():
    """示例：加载数值划分数据"""
    print("=== 数值划分数据示例 ===")
    
    # 加载数值划分数据
    npp = load_npp_txt("processed/number_partitioning/compressed/small/n025d12e00.txt.xz")
    
    print(f"实例名称: {npp.name}")
    print(f"数字个数: {npp.n}")
    print(f"前10个数字: {npp.values[:10]}")
    print(f"数字总和: {sum(npp.values)}")
    print(f"元数据: {npp.meta}")
    print()


def example_graph_coloring():
    """示例：加载图着色数据"""
    print("=== 图着色数据示例 ===")
    
    # 使用自动识别加载图着色数据
    graph = load_instance("processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz")
    
    print(f"图名称: {graph.name}")
    print(f"节点数: {graph.n}")
    print(f"边数: {graph.m}")
    print(f"前5条边: {graph.edges[:5]}")
    print(f"元数据: {graph.meta}")
    print()


def example_batch_loading():
    """示例：批量加载数据"""
    print("=== 批量加载示例 ===")
    
    # 定义要加载的文件列表
    files = [
        "processed/graph_partitioning/compressed/tiny/dolphins.txt.xz",
        "processed/number_partitioning/compressed/small/n025d12e00.txt.xz",
        "processed/graph_coloring/compressed/tiny/DSJC125.1.col.txt.xz"
    ]
    
    # 批量加载
    instances = batch_load_instances(files)
    
    for i, instance in enumerate(instances):
        if hasattr(instance, 'edges'):  # 图数据
            print(f"{i+1}. 图: {instance.name}, 节点数={instance.n}, 边数={instance.m}")
        else:  # 数值划分数据
            print(f"{i+1}. NPP: {instance.name}, 数字个数={instance.n}")
    print()


def example_metadata_extraction():
    """示例：提取和使用元数据"""
    print("=== 元数据提取示例 ===")
    
    # 加载图数据
    graph = load_graph_txt("processed/graph_partitioning/compressed/tiny/dolphins.txt.xz")
    
    # 提取元数据
    problem_type = graph.meta.get('problem', 'unknown')
    name = graph.meta.get('name', 'unknown')
    k = int(graph.meta.get('k', 0))
    weighted = bool(int(graph.meta.get('weighted', 0)))
    directed = bool(int(graph.meta.get('directed', 0)))
    
    print(f"问题类型: {problem_type}")
    print(f"实例名称: {name}")
    print(f"划分数/颜色数: {k}")
    print(f"是否加权: {weighted}")
    print(f"是否有向: {directed}")
    print()


def main():
    """主函数"""
    print("统一加载器使用示例")
    print("=" * 50)
    print()
    
    try:
        example_graph_partitioning()
        example_number_partitioning()
        example_graph_coloring()
        example_batch_loading()
        example_metadata_extraction()
        
        print("所有示例运行完成！")
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        print("请确保数据文件存在且路径正确。")


if __name__ == "__main__":
    main()