"""File deletion module for removing duplicate images."""

import os
from enum import Enum
from typing import List, Tuple


class DeletionStrategy(Enum):
    """删除策略枚举"""
    KEEP_FIRST = "keep_first"      # 保留每组第一个
    KEEP_LAST = "keep_last"        # 保留每组最后一个
    MANUAL = "manual"              # 手动选择


class FileDeleter:
    """文件删除器，实现各种删除策略"""
    
    def __init__(self):
        """初始化文件删除器"""
        pass
    
    def select_files_to_delete(
        self, 
        duplicate_groups: List[List[str]], 
        strategy: DeletionStrategy
    ) -> List[str]:
        """
        根据策略选择要删除的文件
        
        参数:
            duplicate_groups: 重复组列表，每组包含文件路径列表
            strategy: 删除策略
            
        返回:
            要删除的文件路径列表
        """
        files_to_delete = []
        
        for group in duplicate_groups:
            if len(group) < 2:
                # 确保每组至少有2个文件
                continue
            
            if strategy == DeletionStrategy.KEEP_FIRST:
                # 保留第一个，删除其余
                files_to_delete.extend(group[1:])
            elif strategy == DeletionStrategy.KEEP_LAST:
                # 保留最后一个，删除其余
                files_to_delete.extend(group[:-1])
            elif strategy == DeletionStrategy.MANUAL:
                # 手动模式暂不实现，由调用者处理
                pass
        
        return files_to_delete
    
    def safe_delete(self, file_path: str) -> Tuple[bool, str]:
        """
        安全删除单个文件
        
        参数:
            file_path: 要删除的文件路径
            
        返回:
            (是否成功, 错误消息或空字符串)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"文件不存在: {file_path}"
            
            os.remove(file_path)
            return True, ""
        except PermissionError as e:
            return False, f"权限不足: {str(e)}"
        except OSError as e:
            # 处理文件被占用等错误
            return False, f"删除失败: {str(e)}"
        except Exception as e:
            return False, f"未知错误: {str(e)}"
    
    def delete_duplicates(
        self, 
        duplicate_groups: List[List[str]], 
        strategy: DeletionStrategy,
        dry_run: bool = False
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        删除重复文件
        
        参数:
            duplicate_groups: 重复组列表，每组包含文件路径列表
            strategy: 删除策略
            dry_run: 如果为 True，只返回将要删除的文件，不实际删除
            
        返回:
            (成功删除的文件列表, 失败的文件及原因列表)
        """
        # 选择要删除的文件
        files_to_delete = self.select_files_to_delete(duplicate_groups, strategy)
        
        if dry_run:
            # Dry-run 模式：不实际删除，只返回将要删除的文件
            return files_to_delete, []
        
        # 实际删除文件
        deleted_files = []
        failed_files = []
        
        for file_path in files_to_delete:
            success, error_msg = self.safe_delete(file_path)
            if success:
                deleted_files.append(file_path)
            else:
                failed_files.append((file_path, error_msg))
        
        return deleted_files, failed_files

