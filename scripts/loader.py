"""
数据加载器
用于加载统一格式的数据集
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterator, Dict, Any
import io
import os


Header = Dict[str, str]


def _iter_lines(fp: io.TextIOBase) -> Iterator[str]:
    """迭代文件行，跳过注释和空行"""
    for line in fp:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        yield line


def parse_header(raw: str) -> Header:
    """解析文件头部信息"""
    h: Header = {}
    for ln in raw.splitlines():
        if ln.startswith("#"):
            kv = ln[1:].strip().split(":", 1)
            if len(kv) == 2:
                h[kv[0].strip().lower()] = kv[1].strip()
    return h


@dataclass
class GraphInstance:
    """图实例数据结构"""
    name: str
    n: int
    m: int
    edges: List[Tuple[int, int, int]]  # 0-based, (u, v, w)
    meta: Header


def load_graph_txt(path: str) -> GraphInstance:
    """
    加载图数据文件
    
    Args:
        path: 图数据文件路径
        
    Returns:
        GraphInstance: 图实例对象
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    
    meta = parse_header(raw)
    f = io.StringIO(raw)
    lines = list(_iter_lines(f))
    
    # 第一行非注释行: "n m"
    n, m = map(int, lines[0].split()[:2])
    edges = []
    
    for ln in lines[1:]:
        u, v, *rest = ln.split()
        w = int(rest[0]) if rest else 1
        # 转换为0-based索引
        u = int(u) - 1
        v = int(v) - 1
        
        # 去除自环
        if u == v:
            continue
            
        # 规范化无向边顺序
        if u > v:
            u, v = v, u
            
        edges.append((u, v, w))
    
    # 去重
    edges = list({(u, v): (u, v, w) for (u, v, w) in edges}.values())
    
    return GraphInstance(
        name=meta.get("name", os.path.basename(path)),
        n=n,
        m=len(edges),
        edges=edges,
        meta=meta
    )


@dataclass
class NPPInstance:
    """数值划分实例数据结构"""
    name: str
    n: int
    values: List[int]
    meta: Header


def load_npp_txt(path: str) -> NPPInstance:
    """
    加载数值划分数据文件
    
    Args:
        path: 数值划分数据文件路径
        
    Returns:
        NPPInstance: 数值划分实例对象
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    
    meta = parse_header(raw)
    f = io.StringIO(raw)
    it = _iter_lines(f)
    
    # 第一行: 数字个数
    n = int(next(it))
    
    # 兼容逐行或单行格式
    vals: List[int] = []
    for ln in it:
        parts = ln.split()
        vals.extend(map(int, parts))
        if len(vals) >= n:
            break
    
    vals = vals[:n]
    
    return NPPInstance(
        name=meta.get("name", os.path.basename(path)),
        n=n,
        values=vals,
        meta=meta
    )


def load_instance(path: str) -> Any:
    """
    根据文件类型自动选择加载器
    
    Args:
        path: 数据文件路径
        
    Returns:
        GraphInstance 或 NPPInstance 对象
    """
    with open(path, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    
    if first_line.startswith("#"):
        # 读取头部信息确定问题类型
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        meta = parse_header(raw)
        problem_type = meta.get("problem", "").lower()
        
        if "graph" in problem_type:
            return load_graph_txt(path)
        elif "number" in problem_type:
            return load_npp_txt(path)
    
    # 根据内容判断
    parts = first_line.split()
    if len(parts) >= 2 and all(p.isdigit() for p in parts[:2]):
        # 可能是图数据 (n m)
        try:
            return load_graph_txt(path)
        except:
            return load_npp_txt(path)
    else:
        # 可能是数值划分数据
        try:
            return load_npp_txt(path)
        except:
            return load_graph_txt(path)


def load_dataset_split(split_file: str) -> List[str]:
    """
    加载数据集划分文件
    
    Args:
        split_file: 划分文件路径，每行包含一个数据文件路径
        
    Returns:
        List[str]: 数据文件路径列表
    """
    with open(split_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def create_dataset_split(data_files: List[str], output_file: str, 
                        base_path: str = "processed/"):
    """
    创建数据集划分文件
    
    Args:
        data_files: 数据文件路径列表
        output_file: 输出划分文件路径
        base_path: 基础路径
    """
    with open(output_file, 'w') as f:
        for file_path in data_files:
            # 确保路径是相对路径
            if file_path.startswith(base_path):
                rel_path = file_path[len(base_path):]
            else:
                rel_path = file_path
            f.write(f"{rel_path}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python loader.py <data_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    instance = load_instance(file_path)
    
    if isinstance(instance, GraphInstance):
        print(f"Graph: {instance.name}, n={instance.n}, m={instance.m}")
        print(f"First 5 edges: {instance.edges[:5]}")
    elif isinstance(instance, NPPInstance):
        print(f"NPP: {instance.name}, n={instance.n}")
        print(f"First 10 values: {instance.values[:10]}")