"""File hasher module for computing SHA-256 hashes."""

import hashlib
import os
from typing import Dict, List, Optional, Callable


class FileHasher:
    """文件哈希计算器，使用 SHA-256 算法"""
    
    CHUNK_SIZE = 8192  # 8KB 块大小，用于流式读取
    
    def __init__(self):
        self._hash_cache: Dict[str, str] = {}
    
    def compute_hash(self, file_path: str) -> str:
        """
        计算文件的 SHA-256 哈希值
        
        参数:
            file_path: 文件路径
            
        返回:
            十六进制格式的哈希字符串
            
        异常:
            FileNotFoundError: 如果文件不存在
            IOError: 如果读取文件失败
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 检查是否为文件（而非目录）
        if not os.path.isfile(file_path):
            raise IOError(f"路径不是文件: {file_path}")
        
        # 检查缓存
        if file_path in self._hash_cache:
            return self._hash_cache[file_path]
        
        # 计算哈希值
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                # 流式读取文件
                while True:
                    chunk = f.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    sha256_hash.update(chunk)
        except PermissionError as e:
            raise IOError(f"没有读取权限: {file_path}") from e
        except OSError as e:
            raise IOError(f"读取文件失败: {file_path}") from e
        
        # 获取十六进制哈希值
        hash_value = sha256_hash.hexdigest()
        
        # 缓存结果
        self._hash_cache[file_path] = hash_value
        
        return hash_value
    
    def compute_hashes(
        self, 
        file_paths: List[str], 
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, str]:
        """
        批量计算文件哈希值
        
        参数:
            file_paths: 文件路径列表
            progress_callback: 可选的进度回调函数，接收 (current, total, file_path) 参数
        
        返回:
            文件路径到哈希值的映射字典
        """
        result = {}
        total = len(file_paths)
        
        for index, file_path in enumerate(file_paths, 1):
            try:
                hash_value = self.compute_hash(file_path)
                result[file_path] = hash_value
                
                # 调用进度回调
                if progress_callback:
                    progress_callback(index, total, file_path)
            
            except (FileNotFoundError, IOError) as e:
                # 跳过无法处理的文件，继续处理其他文件
                # 可以选择记录错误，但不中断整个批量处理
                if progress_callback:
                    progress_callback(index, total, f"错误: {file_path}")
                continue
        
        return result
    
    def clear_cache(self):
        """清空哈希缓存"""
        self._hash_cache.clear()
    
    def get_cache_size(self) -> int:
        """返回缓存中的条目数量"""
        return len(self._hash_cache)
