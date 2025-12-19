"""Duplicate detector module for finding duplicate files."""

from typing import Dict, List


class DuplicateDetector:
    """重复文件检测器"""
    
    def find_duplicates(self, file_hashes: Dict[str, str]) -> List[List[str]]:
        """
        根据哈希值查找重复文件
        
        参数:
            file_hashes: 文件路径到哈希值的映射
            
        返回:
            重复组列表，每组包含具有相同哈希的文件路径列表
        """
        # 按哈希值分组文件
        hash_groups = self.group_by_hash(file_hashes)
        
        # 只保留有重复的组（至少2个文件）
        duplicate_groups = []
        for hash_value, file_paths in hash_groups.items():
            if len(file_paths) >= 2:
                # 按路径排序
                sorted_paths = sorted(file_paths)
                duplicate_groups.append(sorted_paths)
        
        return duplicate_groups
    
    def group_by_hash(self, file_hashes: Dict[str, str]) -> Dict[str, List[str]]:
        """将文件按哈希值分组"""
        hash_groups: Dict[str, List[str]] = {}
        
        for file_path, hash_value in file_hashes.items():
            if hash_value not in hash_groups:
                hash_groups[hash_value] = []
            hash_groups[hash_value].append(file_path)
        
        return hash_groups
