"""Tests for the FileScanner module."""

import os
import tempfile
import pytest
from pathlib import Path
from src.image_deduplicator.scanner import FileScanner


class TestFileScanner:
    """Test cases for FileScanner class."""
    
    def test_is_image_file_with_supported_extensions(self):
        """Test that supported image extensions are recognized."""
        scanner = FileScanner()
        
        # Test all supported extensions (lowercase)
        assert scanner.is_image_file("test.jpg")
        assert scanner.is_image_file("test.jpeg")
        assert scanner.is_image_file("test.png")
        assert scanner.is_image_file("test.gif")
        assert scanner.is_image_file("test.bmp")
        assert scanner.is_image_file("test.webp")
        assert scanner.is_image_file("test.tiff")
        
        # Test uppercase extensions
        assert scanner.is_image_file("test.JPG")
        assert scanner.is_image_file("test.PNG")
    
    def test_is_image_file_with_unsupported_extensions(self):
        """Test that unsupported extensions are not recognized."""
        scanner = FileScanner()
        
        assert not scanner.is_image_file("test.txt")
        assert not scanner.is_image_file("test.pdf")
        assert not scanner.is_image_file("test.doc")
        assert not scanner.is_image_file("test.mp4")
        assert not scanner.is_image_file("noextension")
    
    def test_scan_invalid_path(self):
        """Test that scan raises ValueError for non-existent path."""
        scanner = FileScanner()
        
        with pytest.raises(ValueError, match="路径不存在"):
            scanner.scan("/nonexistent/path/that/does/not/exist")
    
    def test_scan_file_instead_of_directory(self):
        """Test that scan raises ValueError when given a file path."""
        scanner = FileScanner()
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            with pytest.raises(ValueError, match="路径不是文件夹"):
                scanner.scan(tmp_path)
        finally:
            os.unlink(tmp_path)
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        scanner = FileScanner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = scanner.scan(tmpdir)
            assert result == []
    
    def test_scan_directory_with_images(self):
        """Test scanning a directory with image files."""
        scanner = FileScanner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test image files
            img1 = Path(tmpdir) / "image1.jpg"
            img2 = Path(tmpdir) / "image2.png"
            txt_file = Path(tmpdir) / "readme.txt"
            
            img1.touch()
            img2.touch()
            txt_file.touch()
            
            result = scanner.scan(tmpdir)
            
            # Should find 2 image files, not the txt file
            assert len(result) == 2
            assert any("image1.jpg" in path for path in result)
            assert any("image2.png" in path for path in result)
            assert not any("readme.txt" in path for path in result)
    
    def test_scan_recursive(self):
        """Test that scan recursively traverses subdirectories."""
        scanner = FileScanner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory structure
            subdir1 = Path(tmpdir) / "subdir1"
            subdir2 = Path(tmpdir) / "subdir1" / "subdir2"
            subdir1.mkdir()
            subdir2.mkdir()
            
            # Create image files at different levels
            img1 = Path(tmpdir) / "root.jpg"
            img2 = subdir1 / "sub1.png"
            img3 = subdir2 / "sub2.gif"
            
            img1.touch()
            img2.touch()
            img3.touch()
            
            result = scanner.scan(tmpdir)
            
            # Should find all 3 images
            assert len(result) == 3
            assert any("root.jpg" in path for path in result)
            assert any("sub1.png" in path for path in result)
            assert any("sub2.gif" in path for path in result)
    
    def test_scan_with_progress_callback(self):
        """Test that progress callback is called during scan."""
        scanner = FileScanner()
        callback_calls = []
        
        def progress_callback(count, message):
            callback_calls.append((count, message))
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test image files
            for i in range(3):
                img = Path(tmpdir) / f"image{i}.jpg"
                img.touch()
            
            scanner.scan(tmpdir, progress_callback=progress_callback)
            
            # Callback should have been called 3 times
            assert len(callback_calls) == 3
            assert callback_calls[0][0] == 1
            assert callback_calls[1][0] == 2
            assert callback_calls[2][0] == 3
    
    def test_scan_returns_absolute_paths(self):
        """Test that scan returns absolute paths."""
        scanner = FileScanner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            img = Path(tmpdir) / "test.jpg"
            img.touch()
            
            result = scanner.scan(tmpdir)
            
            assert len(result) == 1
            assert os.path.isabs(result[0])
