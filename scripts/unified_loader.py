"""
统一数据加载器
用于加载标准化格式的组合优化数据集
支持图划分、图着色和数值划分问题
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterator, Dict, Any, Union
import io
import os
import gzip
import lzma
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def _open_file(path: str) -> io.TextIOBase:
    """
    智能打开文件，支持普通文件、gzip和xz压缩格式
    
    Args:
        path: 文件路径
        
    Returns:
        文件对象
    """
    if path.endswith('.gz'):
        return gzip.open(path, 'rt', encoding='utf-8')
    elif path.endswith('.xz'):
        # 对于xz文件，需要特殊处理以跳过tar头部
        import subprocess
        try:
            # 尝试使用tar命令提取内容
            result = subprocess.run(
                ['bash', '-c', f'xz -dc "{path}" | tar -xOf - 2>/dev/null'],
                capture_output=True,
                text=True,
                check=True
            )
            return io.StringIO(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 如果tar命令失败，回退到常规方法
            return lzma.open(path, 'rt', encoding='utf-8')
    else:
        return open(path, 'r', encoding='utf-8')


@dataclass
class GraphInstance:
    """图实例数据结构"""
    name: str
    n: int
    m: int
    edges: List[Tuple[int, int, int]]  # 0-based, (u, v, w)
    meta: Header
    
    def __post_init__(self):
        """验证数据完整性"""
        if self.n <= 0:
            raise ValueError(f"节点数必须为正数，得到: {self.n}")
        if self.m < 0:
            raise ValueError(f"边数不能为负数，得到: {self.m}")
        if len(self.edges) != self.m:
            logger.warning(f"边数不匹配: 头部声明 {self.m}, 实际 {len(self.edges)}")


@dataclass
class NPPInstance:
    """数值划分实例数据结构"""
    name: str
    n: int
    values: List[int]
    meta: Header
    
    def __post_init__(self):
        """验证数据完整性"""
        if self.n <= 0:
            raise ValueError(f"数字个数必须为正数，得到: {self.n}")
        if len(self.values) != self.n:
            logger.warning(f"数字个数不匹配: 头部声明 {self.n}, 实际 {len(self.values)}")
        if any(v <= 0 for v in self.values):
            logger.warning("数值划分问题中存在非正整数")


def load_graph_txt(path: str) -> GraphInstance:
    """
    加载图数据文件
    
    关键功能：
    1. 正确处理 1-based 到 0-based 的索引转换
    2. 执行去重和去自环
    3. 规范化无向边顺序
    
    Args:
        path: 图数据文件路径
        
    Returns:
        GraphInstance: 图实例对象
    """
    logger.info(f"加载图数据: {path}")
    
    with _open_file(path) as f:
        raw = f.read()
    
    meta = parse_header(raw)
    f = io.StringIO(raw)
    lines = list(_iter_lines(f))
    
    if not lines:
        raise ValueError(f"文件 {path} 没有有效数据行")
    
    # 第一行非注释行: "n m"
    try:
        n, m = map(int, lines[0].split()[:2])
    except ValueError as e:
        raise ValueError(f"无法解析图规模信息: {lines[0]}") from e
    
    edges = []
    duplicate_count = 0
    self_loop_count = 0
    
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) < 2:
            continue  # 跳过无效行
            
        u, v, *rest = parts
        try:
            u = int(u) - 1  # 1-based -> 0-based
            v = int(v) - 1  # 1-based -> 0-based
            w = int(rest[0]) if rest else 1
        except ValueError as e:
            logger.warning(f"跳过无效边数据: {ln}")
            continue
        
        # 去除自环
        if u == v:
            self_loop_count += 1
            continue
            
        # 规范化无向边顺序 (确保 u <= v)
        if u > v:
            u, v = v, u
            
        edges.append((u, v, w))
    
    # 去重 - 使用字典去重，保留最后一个权重
    edge_dict = {}
    for u, v, w in edges:
        if (u, v) in edge_dict:
            duplicate_count += 1
        edge_dict[(u, v)] = (u, v, w)
    
    edges = list(edge_dict.values())
    
    if duplicate_count > 0:
        logger.info(f"去除了 {duplicate_count} 条重复边")
    if self_loop_count > 0:
        logger.info(f"去除了 {self_loop_count} 条自环")
    
    # 验证节点索引范围
    max_node = max(max(u, v) for u, v, _ in edges) if edges else -1
    if max_node >= n:
        logger.warning(f"节点索引超出范围: 最大索引 {max_node}, 节点数 {n}")
    
    return GraphInstance(
        name=meta.get("name", os.path.basename(path)),
        n=n,
        m=len(edges),
        edges=edges,
        meta=meta
    )


def load_npp_txt(path: str) -> NPPInstance:
    """
    加载数值划分数据文件
    
    Args:
        path: 数值划分数据文件路径
        
    Returns:
        NPPInstance: 数值划分实例对象
    """
    logger.info(f"加载数值划分数据: {path}")
    
    with _open_file(path) as f:
        raw = f.read()
    
    meta = parse_header(raw)
    f = io.StringIO(raw)
    it = _iter_lines(f)
    
    try:
        # 第一行: 数字个数
        n = int(next(it))
    except StopIteration:
        raise ValueError(f"文件 {path} 没有数字个数信息")
    except ValueError as e:
        raise ValueError(f"无法解析数字个数: {e}") from e
    
    # 兼容逐行或单行格式
    vals: List[int] = []
    for ln in it:
        parts = ln.split()
        try:
            vals.extend(map(int, parts))
        except ValueError as e:
            logger.warning(f"跳过无效数字: {ln}")
            continue
            
        if len(vals) >= n:
            break
    
    vals = vals[:n]
    
    if len(vals) < n:
        logger.warning(f"数字数量不足: 期望 {n}, 实际 {len(vals)}")
    
    return NPPInstance(
        name=meta.get("name", os.path.basename(path)),
        n=len(vals),  # 使用实际读取的数字个数
        values=vals,
        meta=meta
    )


def load_instance(path: str) -> Union[GraphInstance, NPPInstance]:
    """
    主要的调度函数，根据文件类型自动选择加载器
    
    Args:
        path: 数据文件路径
        
    Returns:
        GraphInstance 或 NPPInstance 对象
    """
    logger.info(f"自动识别并加载数据: {path}")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")
    
    # 首先尝试读取头部信息确定问题类型
    try:
        with _open_file(path) as f:
            raw = f.read()
        meta = parse_header(raw)
        problem_type = meta.get("problem", "").lower()
        
        if "graph" in problem_type:
            return load_graph_txt(path)
        elif "number" in problem_type:
            return load_npp_txt(path)
    except Exception as e:
        logger.warning(f"无法通过头部信息确定文件类型: {e}")
    
    # 如果头部信息不足，尝试通过内容判断
    try:
        with _open_file(path) as f:
            # 跳过注释行，找到第一个有效行
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                    
                parts = line.split()
                # 如果有两个或更多数字，可能是图数据 (n m)
                if len(parts) >= 2 and all(p.isdigit() for p in parts[:2]):
                    try:
                        # 尝试作为图数据加载
                        return load_graph_txt(path)
                    except:
                        # 如果失败，尝试作为数值划分数据加载
                        return load_npp_txt(path)
                else:
                    # 可能是数值划分数据
                    try:
                        return load_npp_txt(path)
                    except:
                        return load_graph_txt(path)
                        
    except Exception as e:
        logger.error(f"无法加载文件 {path}: {e}")
        raise


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


def batch_load_instances(file_paths: List[str]) -> List[Union[GraphInstance, NPPInstance]]:
    """
    批量加载数据实例
    
    Args:
        file_paths: 数据文件路径列表
        
    Returns:
        List[Union[GraphInstance, NPPInstance]]: 数据实例列表
    """
    instances = []
    failed_files = []
    
    for path in file_paths:
        try:
            instance = load_instance(path)
            instances.append(instance)
        except Exception as e:
            logger.error(f"加载文件失败 {path}: {e}")
            failed_files.append((path, str(e)))
    
    if failed_files:
        logger.warning(f"共有 {len(failed_files)} 个文件加载失败")
    
    return instances


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="统一数据加载器")
    parser.add_argument("file_path", help="数据文件路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        instance = load_instance(args.file_path)
        
        if isinstance(instance, GraphInstance):
            print(f"图: {instance.name}")
            print(f"节点数: {instance.n}, 边数: {instance.m}")
            print(f"前5条边: {instance.edges[:5]}")
        elif isinstance(instance, NPPInstance):
            print(f"数值划分: {instance.name}")
            print(f"数字个数: {instance.n}")
            print(f"前10个数字: {instance.values[:10]}")
            
    except Exception as e:
        logger.error(f"加载失败: {e}")
        sys.exit(1)