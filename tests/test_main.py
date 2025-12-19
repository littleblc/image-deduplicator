"""Tests for the main module."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from image_deduplicator.main import (
    setup_logging,
    load_config,
    parse_arguments,
    run_workflow,
    DEFAULT_CONFIG
)


class TestSetupLogging:
    """测试日志设置"""
    
    def test_setup_logging_creates_log_directory(self):
        """测试日志设置创建日志目录"""
        setup_logging("INFO")
        
        log_dir = Path.home() / ".image-deduplicator"
        assert log_dir.exists()
        assert log_dir.is_dir()
    
    def test_setup_logging_creates_log_file(self):
        """测试日志设置创建日志文件"""
        setup_logging("INFO")
        
        log_file = Path.home() / ".image-deduplicator" / "error.log"
        assert log_file.exists()


class TestLoadConfig:
    """测试配置加载"""
    
    def test_load_config_returns_default_when_no_file(self):
        """测试当配置文件不存在时返回默认配置"""
        # 确保配置文件不存在
        config_path = Path.home() / ".image-deduplicator" / "config.json"
        if config_path.exists():
            config_path.unlink()
        
        config = load_config()
        
        assert config == DEFAULT_CONFIG
    
    def test_load_config_merges_user_config(self):
        """测试加载并合并用户配置"""
        import json
        
        # 创建临时配置文件
        config_dir = Path.home() / ".image-deduplicator"
        config_dir.mkdir(exist_ok=True)
        config_path = config_dir / "config.json"
        
        user_config = {
            "log_level": "DEBUG",
            "custom_setting": "test_value"
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(user_config, f)
        
        config = load_config()
        
        # 应该包含默认配置和用户配置
        assert config["log_level"] == "DEBUG"
        assert config["custom_setting"] == "test_value"
        assert "chunk_size" in config  # 默认配置项
        
        # 清理
        config_path.unlink()


class TestParseArguments:
    """测试命令行参数解析"""
    
    def test_parse_arguments_no_args(self):
        """测试无参数情况"""
        with patch('sys.argv', ['main.py']):
            args = parse_arguments()
            
            assert args.folder is None
            assert args.dry_run is False
            assert args.auto is None
            assert args.log_level == 'INFO'
    
    def test_parse_arguments_with_folder(self):
        """测试指定文件夹参数"""
        with patch('sys.argv', ['main.py', '--folder', '/test/path']):
            args = parse_arguments()
            
            assert args.folder == '/test/path'
    
    def test_parse_arguments_with_dry_run(self):
        """测试 dry-run 参数"""
        with patch('sys.argv', ['main.py', '--dry-run']):
            args = parse_arguments()
            
            assert args.dry_run is True
    
    def test_parse_arguments_with_auto_strategy(self):
        """测试自动删除策略参数"""
        with patch('sys.argv', ['main.py', '--auto', 'keep-first']):
            args = parse_arguments()
            
            assert args.auto == 'keep-first'
    
    def test_parse_arguments_with_log_level(self):
        """测试日志级别参数"""
        with patch('sys.argv', ['main.py', '--log-level', 'DEBUG']):
            args = parse_arguments()
            
            assert args.log_level == 'DEBUG'


class TestRunWorkflow:
    """测试主工作流"""
    
    def test_run_workflow_with_no_images(self, fs):
        """测试扫描空文件夹"""
        # 创建空文件夹
        test_dir = "/test/empty"
        fs.create_dir(test_dir)
        
        # 运行工作流
        exit_code = run_workflow(test_dir)
        
        assert exit_code == 0
    
    def test_run_workflow_with_no_duplicates(self, fs):
        """测试没有重复文件的情况"""
        # 创建测试文件夹和文件
        test_dir = "/test/images"
        fs.create_dir(test_dir)
        
        # 创建不同内容的图片文件
        fs.create_file(f"{test_dir}/image1.jpg", contents="content1")
        fs.create_file(f"{test_dir}/image2.jpg", contents="content2")
        
        # 运行工作流
        exit_code = run_workflow(test_dir)
        
        assert exit_code == 0
    
    def test_run_workflow_with_duplicates_dry_run(self, fs):
        """测试有重复文件的 dry-run 模式"""
        # 创建测试文件夹和重复文件
        test_dir = "/test/images"
        fs.create_dir(test_dir)
        
        # 创建相同内容的图片文件
        same_content = "duplicate content"
        fs.create_file(f"{test_dir}/image1.jpg", contents=same_content)
        fs.create_file(f"{test_dir}/image2.jpg", contents=same_content)
        
        # 运行 dry-run 模式
        exit_code = run_workflow(test_dir, dry_run=True)
        
        assert exit_code == 0
        
        # 验证文件未被删除
        assert os.path.exists(f"{test_dir}/image1.jpg")
        assert os.path.exists(f"{test_dir}/image2.jpg")
    
    def test_run_workflow_with_duplicates_auto_delete(self, fs):
        """测试自动删除重复文件"""
        # 创建测试文件夹和重复文件
        test_dir = "/test/images"
        fs.create_dir(test_dir)
        
        # 创建相同内容的图片文件
        same_content = "duplicate content"
        fs.create_file(f"{test_dir}/aaa.jpg", contents=same_content)
        fs.create_file(f"{test_dir}/bbb.jpg", contents=same_content)
        
        # 运行自动删除模式（保留第一个）
        exit_code = run_workflow(test_dir, auto_strategy='keep-first')
        
        assert exit_code == 0
        
        # 验证第一个文件保留，第二个被删除
        assert os.path.exists(f"{test_dir}/aaa.jpg")
        assert not os.path.exists(f"{test_dir}/bbb.jpg")
    
    def test_run_workflow_handles_keyboard_interrupt(self, fs):
        """测试处理键盘中断"""
        test_dir = "/test/images"
        fs.create_dir(test_dir)
        
        # 模拟键盘中断
        with patch('image_deduplicator.scanner.FileScanner.scan', side_effect=KeyboardInterrupt):
            exit_code = run_workflow(test_dir)
            
            assert exit_code == 1
    
    def test_run_workflow_handles_exceptions(self, fs):
        """测试处理异常"""
        test_dir = "/test/images"
        fs.create_dir(test_dir)
        
        # 模拟异常
        with patch('image_deduplicator.scanner.FileScanner.scan', side_effect=Exception("Test error")):
            exit_code = run_workflow(test_dir)
            
            assert exit_code == 1
