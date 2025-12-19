"""File scanner module for finding image files."""

import os
from pathlib import Path
from typing import List, Optional, Callable


class FileScanner:
    """文件扫描器，负责递归扫描文件夹并识别图片文件"""
    
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff'}
    
    def scan(self, folder_path: str, progress_callback: Optional[Callable] = None) -> List[str]:
        """
        扫描指定文件夹，返回所有图片文件路径
        
        参数:
            folder_path: 目标文件夹路径
            progress_callback: 可选的进度回调函数，接收 (current_count, message) 参数
            
        返回:
            图片文件路径列表
            
        异常:
            ValueError: 如果文件夹路径无效
            PermissionError: 如果没有访问权限
        """
        # 验证路径
        path = Path(folder_path)
        
        if not path.exists():
            raise ValueError(f"路径不存在: {folder_path}")
        
        if not path.is_dir():
            raise ValueError(f"路径不是文件夹: {folder_path}")
        
        # 检查访问权限
        if not os.access(folder_path, os.R_OK):
            raise PermissionError(f"没有读取权限: {folder_path}")
        
        image_files = []
        file_count = 0
        
        # 递归遍历文件夹
        try:
            for root, dirs, files in os.walk(folder_path):
                # 处理权限错误：尝试访问每个子目录
                dirs_to_remove = []
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if not os.access(dir_path, os.R_OK):
                        dirs_to_remove.append(dir_name)
                        # 静默跳过无权限的目录
                
                # 从遍历列表中移除无权限的目录
                for dir_name in dirs_to_remove:
                    dirs.remove(dir_name)
                
                # 检查每个文件
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    
                    # 检查是否为图片文件
                    if self.is_image_file(file_path):
                        # 获取绝对路径
                        abs_path = os.path.abspath(file_path)
                        image_files.append(abs_path)
                        file_count += 1
                        
                        # 调用进度回调
                        if progress_callback:
                            progress_callback(file_count, f"扫描: {file_name}")
        
        except PermissionError as e:
            # 如果根目录本身无权限访问，抛出异常
            raise PermissionError(f"扫描过程中权限错误: {e}")
        
        return image_files
    
    def is_image_file(self, file_path: str) -> bool:
        """判断文件是否为支持的图片格式"""
        # 获取文件扩展名（转换为小写）
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.SUPPORTED_EXTENSIONS
