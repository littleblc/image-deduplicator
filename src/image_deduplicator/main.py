"""Main entry point for the image deduplicator application."""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any

from .scanner import FileScanner
from .hasher import FileHasher
from .detector import DuplicateDetector
from .deleter import FileDeleter, DeletionStrategy
from .cli import CLI


# 默认配置
DEFAULT_CONFIG = {
    "supported_extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"],
    "chunk_size": 8192,
    "default_strategy": "keep_first",
    "enable_cache": True,
    "log_level": "INFO"
}


def setup_logging(log_level: str = "INFO") -> None:
    """
    设置日志记录
    
    参数:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # 创建日志目录
    log_dir = Path.home() / ".image-deduplicator"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "error.log"
    
    # 配置日志格式
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 配置日志处理器
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stderr)
        ]
    )


def create_default_config() -> None:
    """创建默认配置文件"""
    config_dir = Path.home() / ".image-deduplicator"
    config_dir.mkdir(exist_ok=True)
    
    config_path = config_dir / "config.json"
    
    if not config_path.exists():
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
            logging.info(f"已创建默认配置文件: {config_path}")
        except Exception as e:
            logging.error(f"创建配置文件失败: {e}")


def load_config() -> Dict[str, Any]:
    """
    加载配置文件
    
    返回:
        配置字典
    """
    config_path = Path.home() / ".image-deduplicator" / "config.json"
    
    # 如果配置文件不存在，创建默认配置文件
    if not config_path.exists():
        logging.info("配置文件不存在，创建默认配置")
        create_default_config()
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = json.load(f)
        
        # 合并用户配置和默认配置
        config = DEFAULT_CONFIG.copy()
        config.update(user_config)
        
        logging.info(f"已加载配置文件: {config_path}")
        return config
    
    except json.JSONDecodeError as e:
        logging.error(f"配置文件格式错误: {e}")
        logging.info("使用默认配置")
        return DEFAULT_CONFIG.copy()
    
    except Exception as e:
        logging.error(f"加载配置文件失败: {e}")
        logging.info("使用默认配置")
        return DEFAULT_CONFIG.copy()


def parse_arguments() -> argparse.Namespace:
    """
    解析命令行参数
    
    返回:
        解析后的参数
    """
    parser = argparse.ArgumentParser(
        description="图片去重工具 - 扫描并删除重复的图片文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 交互式模式
  %(prog)s --folder /path/to/images # 指定文件夹
  %(prog)s --dry-run                # 预览模式（不实际删除）
  %(prog)s --auto keep-first        # 自动删除（保留第一个）
  %(prog)s --no-color               # 禁用彩色输出
  %(prog)s --no-progress            # 禁用进度条

配置文件:
  配置文件位于: ~/.image-deduplicator/config.json
  可配置项包括: supported_extensions, chunk_size, default_strategy, 
               enable_cache, log_level
        """
    )
    
    parser.add_argument(
        '--folder',
        type=str,
        help='要扫描的文件夹路径'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式：显示将要删除的文件但不实际删除'
    )
    
    parser.add_argument(
        '--auto',
        type=str,
        choices=['keep-first', 'keep-last'],
        help='自动删除模式：keep-first（保留第一个）或 keep-last（保留最后一个）'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='日志级别（默认: INFO）'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )
    
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='禁用 tqdm 进度条'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    return parser.parse_args()


def run_workflow(
    folder_path: str,
    dry_run: bool = False,
    auto_strategy: Optional[str] = None,
    use_colors: bool = True,
    use_progress_bar: bool = True
) -> int:
    """
    运行主工作流
    
    参数:
        folder_path: 要扫描的文件夹路径
        dry_run: 是否为预览模式
        auto_strategy: 自动删除策略（None 表示交互模式）
        use_colors: 是否使用彩色输出
        use_progress_bar: 是否使用进度条
    
    返回:
        退出码（0 表示成功）
    """
    cli = CLI(use_colors=use_colors, use_progress_bar=use_progress_bar)
    
    try:
        # 1. 扫描文件
        logging.info(f"开始扫描文件夹: {folder_path}")
        print("\n正在扫描文件夹...")
        
        scanner = FileScanner()
        file_count = [0]  # 使用列表以便在闭包中修改
        
        def scan_progress(count: int, message: str):
            file_count[0] = count
            cli.display_progress(count, 0, f"扫描中")
        
        start_time = time.time()
        image_files = scanner.scan(folder_path, progress_callback=scan_progress)
        scan_time = time.time() - start_time
        
        cli.close_progress()  # 关闭进度条
        print()  # 换行
        print(f"✓ 扫描完成，找到 {len(image_files)} 个图片文件（耗时 {scan_time:.2f} 秒）")
        logging.info(f"扫描完成: {len(image_files)} 个文件，耗时 {scan_time:.2f} 秒")
        
        if len(image_files) == 0:
            print("未找到任何图片文件。")
            return 0
        
        # 2. 计算哈希值
        print("\n正在计算文件哈希值...")
        
        hasher = FileHasher()
        
        def hash_progress(current: int, total: int, file_path: str):
            cli.display_progress(current, total, "计算哈希")
        
        file_hashes = hasher.compute_hashes(image_files, progress_callback=hash_progress)
        
        cli.close_progress()  # 关闭进度条
        print()  # 换行
        print(f"✓ 哈希计算完成，成功处理 {len(file_hashes)} 个文件")
        logging.info(f"哈希计算完成: {len(file_hashes)} 个文件")
        
        # 3. 检测重复文件
        print("\n正在检测重复文件...")
        
        detector = DuplicateDetector()
        duplicate_groups = detector.find_duplicates(file_hashes)
        
        print(f"✓ 检测完成，找到 {len(duplicate_groups)} 个重复组")
        logging.info(f"检测完成: {len(duplicate_groups)} 个重复组")
        
        if len(duplicate_groups) == 0:
            print("\n未找到重复文件。")
            return 0
        
        # 4. 显示重复组
        cli.display_duplicate_groups(duplicate_groups)
        
        # 5. 选择删除策略
        strategy = None
        
        # 在 dry-run 模式下，如果没有指定策略，使用默认策略
        if dry_run and not auto_strategy:
            strategy = DeletionStrategy.KEEP_FIRST
            print(f"\n[预览模式] 使用默认策略: 保留每组第一个文件")
        elif auto_strategy:
            # 自动模式
            if auto_strategy == 'keep-first':
                strategy = DeletionStrategy.KEEP_FIRST
                print(f"\n使用自动删除策略: 保留每组第一个文件")
            elif auto_strategy == 'keep-last':
                strategy = DeletionStrategy.KEEP_LAST
                print(f"\n使用自动删除策略: 保留每组最后一个文件")
        else:
            # 交互模式
            strategy = cli.prompt_deletion_strategy()
        
        if strategy is None:
            print("\n操作已取消。")
            logging.info("用户取消操作")
            return 0
        
        # 6. 删除文件
        deleter = FileDeleter()
        
        # 选择要删除的文件
        files_to_delete = deleter.select_files_to_delete(duplicate_groups, strategy)
        
        if len(files_to_delete) == 0:
            print("\n没有文件需要删除。")
            return 0
        
        # 确认删除（除非是 dry-run 模式）
        if dry_run:
            print(f"\n[预览模式] 以下 {len(files_to_delete)} 个文件将被删除:")
            for idx, file_path in enumerate(files_to_delete[:20], 1):
                print(f"  {idx}. {file_path}")
            if len(files_to_delete) > 20:
                print(f"  ... 还有 {len(files_to_delete) - 20} 个文件")
            print("\n提示: 移除 --dry-run 参数以实际删除文件")
            return 0
        
        # 交互模式需要确认
        if not auto_strategy:
            confirmed = cli.confirm_deletion(files_to_delete)
            if not confirmed:
                logging.info("用户取消删除操作")
                return 0
        
        # 执行删除
        print("\n正在删除文件...")
        logging.info(f"开始删除 {len(files_to_delete)} 个文件")
        
        deleted, failed = deleter.delete_duplicates(duplicate_groups, strategy, dry_run=False)
        
        # 记录删除结果
        for file_path in deleted:
            logging.info(f"已删除: {file_path}")
        
        for file_path, error_msg in failed:
            logging.error(f"删除失败: {file_path} - {error_msg}")
        
        # 显示结果
        cli.display_results(deleted, failed)
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n操作被用户中断。")
        logging.info("操作被用户中断")
        return 1
    
    except Exception as e:
        print(f"\n错误: {str(e)}")
        logging.exception(f"发生未预期的错误: {e}")
        return 1


def main():
    """主程序入口"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 加载配置
    config = load_config()
    
    # 设置日志
    log_level = args.log_level or config.get('log_level', 'INFO')
    setup_logging(log_level)
    
    logging.info("=" * 60)
    logging.info("图片去重工具启动")
    logging.info("=" * 60)
    
    # 创建 CLI 实例
    use_colors = not args.no_color
    use_progress_bar = not args.no_progress
    cli = CLI(use_colors=use_colors, use_progress_bar=use_progress_bar)
    
    # 显示欢迎信息
    cli.display_welcome()
    
    # 获取文件夹路径
    folder_path = args.folder
    
    if not folder_path:
        # 交互模式：提示用户输入
        folder_path = cli.prompt_folder_path()
    else:
        # 验证命令行提供的路径
        if not os.path.exists(folder_path):
            print(f"错误: 路径不存在: {folder_path}")
            logging.error(f"路径不存在: {folder_path}")
            return 1
        
        if not os.path.isdir(folder_path):
            print(f"错误: 该路径不是文件夹: {folder_path}")
            logging.error(f"路径不是文件夹: {folder_path}")
            return 1
        
        folder_path = os.path.abspath(folder_path)
    
    # 运行主工作流
    exit_code = run_workflow(
        folder_path=folder_path,
        dry_run=args.dry_run,
        auto_strategy=args.auto,
        use_colors=use_colors,
        use_progress_bar=use_progress_bar
    )
    
    logging.info("程序退出")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
