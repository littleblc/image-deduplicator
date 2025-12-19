"""Tests for CLI module."""

import os
import tempfile
from io import StringIO
from unittest.mock import patch
from src.image_deduplicator.cli import CLI
from src.image_deduplicator.deleter import DeletionStrategy


def test_display_welcome():
    """测试欢迎信息显示"""
    cli = CLI()
    
    # 捕获输出
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.display_welcome()
        output = fake_out.getvalue()
    
    # 验证输出包含关键信息
    assert "图片去重工具" in output
    assert "Image Deduplicator" in output
    assert ".jpg" in output
    assert ".png" in output


def test_prompt_folder_path_valid():
    """测试有效文件夹路径输入"""
    cli = CLI()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 模拟用户输入有效路径
        with patch('builtins.input', return_value=tmpdir):
            result = cli.prompt_folder_path()
        
        # 验证返回的是绝对路径
        assert os.path.isabs(result)
        assert os.path.exists(result)


def test_prompt_folder_path_invalid_then_valid():
    """测试无效路径后输入有效路径"""
    cli = CLI()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 模拟用户先输入无效路径，再输入有效路径
        with patch('builtins.input', side_effect=['/nonexistent/path', tmpdir]):
            with patch('sys.stdout', new=StringIO()):
                result = cli.prompt_folder_path()
        
        assert os.path.exists(result)


def test_display_progress():
    """测试进度显示"""
    cli = CLI()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.display_progress(50, 100, "扫描中")
        output = fake_out.getvalue()
    
    # 验证输出包含进度信息
    assert "扫描中" in output
    assert "50.0%" in output or "50%" in output


def test_display_duplicate_groups_empty():
    """测试显示空重复组"""
    cli = CLI()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.display_duplicate_groups([])
        output = fake_out.getvalue()
    
    assert "未找到重复文件" in output


def test_display_duplicate_groups_with_files():
    """测试显示包含文件的重复组"""
    cli = CLI()
    
    # 创建临时文件
    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "test1.jpg")
        file2 = os.path.join(tmpdir, "test2.jpg")
        
        # 创建文件
        with open(file1, 'w') as f:
            f.write("test content")
        with open(file2, 'w') as f:
            f.write("test content")
        
        duplicate_groups = [[file1, file2]]
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.display_duplicate_groups(duplicate_groups)
            output = fake_out.getvalue()
        
        # 验证输出包含文件信息
        assert "重复组 #1" in output
        assert "2 个文件" in output
        assert file1 in output
        assert file2 in output


def test_prompt_deletion_strategy_keep_first():
    """测试选择保留第一个文件策略"""
    cli = CLI()
    
    with patch('builtins.input', return_value='1'):
        with patch('sys.stdout', new=StringIO()):
            result = cli.prompt_deletion_strategy()
    
    assert result == DeletionStrategy.KEEP_FIRST


def test_prompt_deletion_strategy_keep_last():
    """测试选择保留最后一个文件策略"""
    cli = CLI()
    
    with patch('builtins.input', return_value='2'):
        with patch('sys.stdout', new=StringIO()):
            result = cli.prompt_deletion_strategy()
    
    assert result == DeletionStrategy.KEEP_LAST


def test_prompt_deletion_strategy_cancel():
    """测试取消删除操作"""
    cli = CLI()
    
    with patch('builtins.input', return_value='3'):
        with patch('sys.stdout', new=StringIO()):
            result = cli.prompt_deletion_strategy()
    
    assert result is None


def test_prompt_deletion_strategy_invalid_then_valid():
    """测试无效输入后输入有效选项"""
    cli = CLI()
    
    with patch('builtins.input', side_effect=['invalid', '99', '1']):
        with patch('sys.stdout', new=StringIO()):
            result = cli.prompt_deletion_strategy()
    
    assert result == DeletionStrategy.KEEP_FIRST


def test_confirm_deletion_yes():
    """测试确认删除"""
    cli = CLI()
    
    files = ['/path/to/file1.jpg', '/path/to/file2.jpg']
    
    with patch('builtins.input', return_value='yes'):
        with patch('sys.stdout', new=StringIO()):
            result = cli.confirm_deletion(files)
    
    assert result is True


def test_confirm_deletion_no():
    """测试取消删除"""
    cli = CLI()
    
    files = ['/path/to/file1.jpg', '/path/to/file2.jpg']
    
    with patch('builtins.input', return_value='no'):
        with patch('sys.stdout', new=StringIO()):
            result = cli.confirm_deletion(files)
    
    assert result is False


def test_display_results_success():
    """测试显示成功删除结果"""
    cli = CLI()
    
    deleted = ['/path/to/file1.jpg', '/path/to/file2.jpg']
    failed = []
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.display_results(deleted, failed)
        output = fake_out.getvalue()
    
    assert "成功删除 2 个文件" in output
    assert "操作完成" in output


def test_display_results_with_failures():
    """测试显示包含失败的删除结果"""
    cli = CLI()
    
    deleted = ['/path/to/file1.jpg']
    failed = [('/path/to/file2.jpg', '权限不足')]
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.display_results(deleted, failed)
        output = fake_out.getvalue()
    
    assert "成功删除 1 个文件" in output
    assert "删除失败 1 个文件" in output
    assert "权限不足" in output
