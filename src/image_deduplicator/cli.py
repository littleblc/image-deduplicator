"""Command-line interface module."""

import os
import sys
from typing import List, Tuple, Optional
from .deleter import DeletionStrategy

# Optional dependencies
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)  # Initialize colorama
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback: define empty color codes
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""
    class Back:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""


class CLI:
    """命令行界面"""
    
    def __init__(self, use_colors: bool = True, use_progress_bar: bool = True):
        """
        初始化 CLI
        
        参数:
            use_colors: 是否使用彩色输出（需要 colorama）
            use_progress_bar: 是否使用进度条（需要 tqdm）
        """
        self.use_colors = use_colors and COLORAMA_AVAILABLE
        self.use_progress_bar = use_progress_bar and TQDM_AVAILABLE
        self._progress_bar = None
    
    def _colorize(self, text: str, color: str = "", style: str = "") -> str:
        """
        为文本添加颜色
        
        参数:
            text: 要着色的文本
            color: 颜色代码
            style: 样式代码
            
        返回:
            着色后的文本（如果启用颜色）
        """
        if not self.use_colors:
            return text
        return f"{style}{color}{text}{Style.RESET_ALL}"
    
    def display_welcome(self):
        """显示欢迎信息"""
        separator = "=" * 60
        title = "图片去重工具 - Image Deduplicator"
        
        if self.use_colors:
            print(self._colorize(separator, Fore.CYAN))
            print(self._colorize(title, Fore.CYAN, Style.BRIGHT))
            print(self._colorize(separator, Fore.CYAN))
        else:
            print(separator)
            print(title)
            print(separator)
        
        print()
        print("本工具可以帮助您扫描文件夹中的重复图片和视频并进行清理。")
        
        image_formats = ".jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff"
        video_formats = ".mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v, .mpg, .mpeg"
        
        if self.use_colors:
            print(f"支持的图片格式: {self._colorize(image_formats, Fore.GREEN)}")
            print(f"支持的视频格式: {self._colorize(video_formats, Fore.CYAN)}")
        else:
            print(f"支持的图片格式: {image_formats}")
            print(f"支持的视频格式: {video_formats}")
        
        print()
    
    def prompt_folder_path(self) -> str:
        """
        提示用户输入文件夹路径
        
        返回:
            有效的文件夹路径
        """
        while True:
            try:
                prompt = "请输入要扫描的文件夹路径: "
                if self.use_colors:
                    prompt = self._colorize(prompt, Fore.YELLOW)
                
                path = input(prompt).strip()
                
                # 处理空输入
                if not path:
                    error_msg = "错误: 路径不能为空，请重新输入。"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print()
                    continue
                
                # 验证路径是否存在
                if not os.path.exists(path):
                    error_msg = f"错误: 路径不存在: {path}"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print("请输入有效的文件夹路径。")
                    print()
                    continue
                
                # 验证是否为文件夹
                if not os.path.isdir(path):
                    error_msg = f"错误: 该路径不是文件夹: {path}"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print("请输入文件夹路径。")
                    print()
                    continue
                
                # 验证是否可访问
                if not os.access(path, os.R_OK):
                    error_msg = f"错误: 没有访问权限: {path}"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print("请检查文件夹权限。")
                    print()
                    continue
                
                return os.path.abspath(path)
                
            except KeyboardInterrupt:
                print("\n\n操作已取消。")
                sys.exit(0)
            except Exception as e:
                error_msg = f"错误: {str(e)}"
                if self.use_colors:
                    print(self._colorize(error_msg, Fore.RED))
                else:
                    print(error_msg)
                print("请重新输入。")
                print()
    
    def display_progress(self, current: int, total: int, message: str):
        """
        显示进度信息
        
        参数:
            current: 当前进度
            total: 总数
            message: 进度消息
        """
        if self.use_progress_bar and total > 0:
            # 使用 tqdm 进度条
            if self._progress_bar is None:
                self._progress_bar = tqdm(total=total, desc=message, unit="文件")
            
            # 更新进度条
            if current > self._progress_bar.n:
                self._progress_bar.update(current - self._progress_bar.n)
        else:
            # 使用简单的文本进度显示
            if total > 0:
                percentage = (current / total) * 100
                bar_length = 40
                filled_length = int(bar_length * current / total)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                print(f'\r{message}: [{bar}] {percentage:.1f}% ({current}/{total})', end='', flush=True)
            else:
                print(f'\r{message}: {current}', end='', flush=True)
    
    def close_progress(self):
        """关闭进度条"""
        if self._progress_bar is not None:
            self._progress_bar.close()
            self._progress_bar = None
    
    def display_duplicate_groups(self, duplicate_groups: List[List[str]]):
        """
        显示重复文件组
        
        参数:
            duplicate_groups: 重复组列表，每组包含文件路径列表
        """
        print("\n")
        separator = "=" * 60
        title = "扫描结果 - 发现的重复文件组"
        
        if self.use_colors:
            print(self._colorize(separator, Fore.CYAN))
            print(self._colorize(title, Fore.CYAN, Style.BRIGHT))
            print(self._colorize(separator, Fore.CYAN))
        else:
            print(separator)
            print(title)
            print(separator)
        
        print()
        
        if not duplicate_groups:
            msg = "未找到重复文件。"
            if self.use_colors:
                print(self._colorize(msg, Fore.GREEN))
            else:
                print(msg)
            print()
            return
        
        for idx, group in enumerate(duplicate_groups, 1):
            group_header = f"重复组 #{idx} - 共 {len(group)} 个文件:"
            if self.use_colors:
                print(self._colorize(group_header, Fore.YELLOW, Style.BRIGHT))
            else:
                print(group_header)
            
            print("-" * 60)
            
            for file_path in group:
                try:
                    file_size = os.path.getsize(file_path)
                    size_mb = file_size / (1024 * 1024)
                    
                    if self.use_colors:
                        print(f"  - {self._colorize(file_path, Fore.WHITE)}")
                        print(f"    大小: {self._colorize(f'{size_mb:.2f} MB', Fore.CYAN)} ({file_size:,} 字节)")
                    else:
                        print(f"  - {file_path}")
                        print(f"    大小: {size_mb:.2f} MB ({file_size:,} 字节)")
                except Exception as e:
                    if self.use_colors:
                        print(f"  - {self._colorize(file_path, Fore.WHITE)}")
                        print(f"    大小: {self._colorize(f'无法获取 ({str(e)})', Fore.RED)}")
                    else:
                        print(f"  - {file_path}")
                        print(f"    大小: 无法获取 ({str(e)})")
            
            print()
        
        # 显示统计信息
        total_duplicates = sum(len(group) for group in duplicate_groups)
        total_groups = len(duplicate_groups)
        summary = f"总计: {total_groups} 个重复组，{total_duplicates} 个重复文件"
        
        if self.use_colors:
            print(self._colorize(summary, Fore.MAGENTA, Style.BRIGHT))
        else:
            print(summary)
        
        print()
    
    def prompt_deletion_strategy(self) -> Optional[DeletionStrategy]:
        """
        提示用户选择删除策略
        
        返回:
            选择的删除策略，如果用户取消则返回 None
        """
        separator = "=" * 60
        title = "删除策略选择"
        
        if self.use_colors:
            print(self._colorize(separator, Fore.CYAN))
            print(self._colorize(title, Fore.CYAN, Style.BRIGHT))
            print(self._colorize(separator, Fore.CYAN))
        else:
            print(separator)
            print(title)
            print(separator)
        
        print()
        print("请选择删除策略:")
        print("  1. 保留每组第一个文件（按路径排序）")
        print("  2. 保留每组最后一个文件（按路径排序）")
        print("  3. 取消操作")
        print()
        
        while True:
            try:
                prompt = "请输入选项 (1-3): "
                if self.use_colors:
                    prompt = self._colorize(prompt, Fore.YELLOW)
                
                choice = input(prompt).strip()
                
                if not choice:
                    error_msg = "错误: 请输入有效的选项编号。"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print()
                    continue
                
                if choice == "1":
                    return DeletionStrategy.KEEP_FIRST
                elif choice == "2":
                    return DeletionStrategy.KEEP_LAST
                elif choice == "3":
                    return None
                else:
                    error_msg = f"错误: 无效的选项 '{choice}'"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print("请输入 1、2 或 3。")
                    print()
                    
            except KeyboardInterrupt:
                print("\n\n操作已取消。")
                return None
            except Exception as e:
                error_msg = f"错误: {str(e)}"
                if self.use_colors:
                    print(self._colorize(error_msg, Fore.RED))
                else:
                    print(error_msg)
                print("请重新输入。")
                print()
    
    def confirm_deletion(self, files_to_delete: List[str]) -> bool:
        """
        确认删除操作
        
        参数:
            files_to_delete: 将要删除的文件列表
            
        返回:
            True 如果用户确认删除，False 如果取消
        """
        print()
        separator = "=" * 60
        title = "删除确认"
        
        if self.use_colors:
            print(self._colorize(separator, Fore.CYAN))
            print(self._colorize(title, Fore.CYAN, Style.BRIGHT))
            print(self._colorize(separator, Fore.CYAN))
        else:
            print(separator)
            print(title)
            print(separator)
        
        print()
        
        count_msg = f"以下 {len(files_to_delete)} 个文件将被删除:"
        if self.use_colors:
            print(self._colorize(count_msg, Fore.YELLOW, Style.BRIGHT))
        else:
            print(count_msg)
        
        print()
        
        # 显示将要删除的文件（最多显示前20个）
        display_limit = 20
        for idx, file_path in enumerate(files_to_delete[:display_limit], 1):
            if self.use_colors:
                print(f"  {idx}. {self._colorize(file_path, Fore.WHITE)}")
            else:
                print(f"  {idx}. {file_path}")
        
        if len(files_to_delete) > display_limit:
            remaining = f"  ... 还有 {len(files_to_delete) - display_limit} 个文件"
            if self.use_colors:
                print(self._colorize(remaining, Fore.YELLOW))
            else:
                print(remaining)
        
        print()
        
        warning = "警告: 此操作不可撤销！"
        if self.use_colors:
            print(self._colorize(warning, Fore.RED, Style.BRIGHT))
        else:
            print(warning)
        
        print()
        
        while True:
            try:
                prompt = "确认删除这些文件吗？(yes/no): "
                if self.use_colors:
                    prompt = self._colorize(prompt, Fore.YELLOW)
                
                confirmation = input(prompt).strip().lower()
                
                if confirmation in ['yes', 'y', '是']:
                    return True
                elif confirmation in ['no', 'n', '否']:
                    cancel_msg = "操作已取消，所有文件已保留。"
                    if self.use_colors:
                        print(self._colorize(cancel_msg, Fore.GREEN))
                    else:
                        print(cancel_msg)
                    return False
                else:
                    error_msg = f"错误: 无效的输入 '{confirmation}'"
                    if self.use_colors:
                        print(self._colorize(error_msg, Fore.RED))
                    else:
                        print(error_msg)
                    print("请输入 'yes' 或 'no'。")
                    print()
                    
            except KeyboardInterrupt:
                cancel_msg = "\n\n操作已取消，所有文件已保留。"
                if self.use_colors:
                    print(self._colorize(cancel_msg, Fore.GREEN))
                else:
                    print(cancel_msg)
                return False
            except Exception as e:
                error_msg = f"错误: {str(e)}"
                if self.use_colors:
                    print(self._colorize(error_msg, Fore.RED))
                else:
                    print(error_msg)
                print("请重新输入。")
                print()
    
    def display_results(self, deleted: List[str], failed: List[Tuple[str, str]]):
        """
        显示删除结果
        
        参数:
            deleted: 成功删除的文件列表
            failed: 失败的文件及原因列表 [(文件路径, 错误消息), ...]
        """
        print()
        separator = "=" * 60
        title = "操作结果摘要"
        
        if self.use_colors:
            print(self._colorize(separator, Fore.CYAN))
            print(self._colorize(title, Fore.CYAN, Style.BRIGHT))
            print(self._colorize(separator, Fore.CYAN))
        else:
            print(separator)
            print(title)
            print(separator)
        
        print()
        
        # 显示成功删除的文件
        if deleted:
            success_msg = f"✓ 成功删除 {len(deleted)} 个文件"
            if self.use_colors:
                print(self._colorize(success_msg, Fore.GREEN, Style.BRIGHT))
            else:
                print(success_msg)
            
            if len(deleted) <= 10:
                for file_path in deleted:
                    if self.use_colors:
                        print(f"  - {self._colorize(file_path, Fore.WHITE)}")
                    else:
                        print(f"  - {file_path}")
            print()
        else:
            no_delete_msg = "没有文件被删除。"
            if self.use_colors:
                print(self._colorize(no_delete_msg, Fore.YELLOW))
            else:
                print(no_delete_msg)
            print()
        
        # 显示失败的文件
        if failed:
            failed_msg = f"✗ 删除失败 {len(failed)} 个文件:"
            if self.use_colors:
                print(self._colorize(failed_msg, Fore.RED, Style.BRIGHT))
            else:
                print(failed_msg)
            
            for file_path, error_msg in failed:
                if self.use_colors:
                    print(f"  - {self._colorize(file_path, Fore.WHITE)}")
                    print(f"    原因: {self._colorize(error_msg, Fore.RED)}")
                else:
                    print(f"  - {file_path}")
                    print(f"    原因: {error_msg}")
            print()
        
        # 显示总结
        total_attempted = len(deleted) + len(failed)
        if total_attempted > 0:
            success_rate = (len(deleted) / total_attempted) * 100
            
            summary_lines = [
                f"总计: 尝试删除 {total_attempted} 个文件",
                f"成功率: {success_rate:.1f}%"
            ]
            
            if self.use_colors:
                for line in summary_lines:
                    print(self._colorize(line, Fore.MAGENTA))
            else:
                for line in summary_lines:
                    print(line)
        
        print()
        
        complete_msg = "操作完成。"
        if self.use_colors:
            print(self._colorize(complete_msg, Fore.GREEN, Style.BRIGHT))
        else:
            print(complete_msg)
        
        print()
