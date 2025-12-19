"""Core data models for the image deduplicator."""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class ImageFile:
    """图片文件信息"""
    path: str           # 完整文件路径
    size: int           # 文件大小（字节）
    hash: str           # SHA-256 哈希值
    
    def __post_init__(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"文件不存在: {self.path}")


@dataclass
class DuplicateGroup:
    """重复文件组"""
    hash: str                    # 共同的哈希值
    files: List[ImageFile]       # 该组中的所有文件
    
    def __post_init__(self):
        if len(self.files) < 2:
            raise ValueError("重复组必须包含至少 2 个文件")
        # 按路径排序
        self.files.sort(key=lambda f: f.path)
    
    @property
    def count(self) -> int:
        """返回组中文件数量"""
        return len(self.files)
    
    @property
    def total_size(self) -> int:
        """返回组中所有文件的总大小"""
        return sum(f.size for f in self.files)
    
    @property
    def wasted_space(self) -> int:
        """返回重复文件浪费的空间（保留一个文件）"""
        return self.total_size - self.files[0].size


@dataclass
class ScanResult:
    """扫描结果"""
    total_files: int                      # 扫描到的总文件数
    duplicate_groups: List[DuplicateGroup] # 重复组列表
    scan_time: float                      # 扫描耗时（秒）
    
    @property
    def duplicate_count(self) -> int:
        """返回重复文件总数"""
        return sum(group.count for group in self.duplicate_groups)
    
    @property
    def unique_count(self) -> int:
        """返回唯一文件数"""
        return self.total_files - self.duplicate_count + len(self.duplicate_groups)
    
    @property
    def total_wasted_space(self) -> int:
        """返回所有重复文件浪费的总空间"""
        return sum(group.wasted_space for group in self.duplicate_groups)
