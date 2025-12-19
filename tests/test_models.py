"""Tests for core data models."""

import pytest
import tempfile
import os
from image_deduplicator.models import ImageFile, DuplicateGroup, ScanResult


class TestImageFile:
    """Tests for ImageFile model"""
    
    def test_image_file_creation_with_existing_file(self):
        """Test creating ImageFile with an existing file"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name
        
        try:
            img = ImageFile(path=tmp_path, size=100, hash="abc123")
            assert img.path == tmp_path
            assert img.size == 100
            assert img.hash == "abc123"
        finally:
            os.unlink(tmp_path)
    
    def test_image_file_raises_error_for_nonexistent_file(self):
        """Test that ImageFile raises FileNotFoundError for non-existent files"""
        with pytest.raises(FileNotFoundError):
            ImageFile(path="/nonexistent/path.jpg", size=100, hash="abc123")


class TestDuplicateGroup:
    """Tests for DuplicateGroup model"""
    
    def test_duplicate_group_creation(self):
        """Test creating a valid DuplicateGroup"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp1, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp2:
            tmp1.write(b"test")
            tmp2.write(b"test")
            path1, path2 = tmp1.name, tmp2.name
        
        try:
            file1 = ImageFile(path=path1, size=100, hash="abc123")
            file2 = ImageFile(path=path2, size=100, hash="abc123")
            
            group = DuplicateGroup(hash="abc123", files=[file1, file2])
            assert group.hash == "abc123"
            assert group.count == 2
            assert group.total_size == 200
            assert group.wasted_space == 100
        finally:
            os.unlink(path1)
            os.unlink(path2)
    
    def test_duplicate_group_raises_error_with_single_file(self):
        """Test that DuplicateGroup raises ValueError with less than 2 files"""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test")
            tmp_path = tmp.name
        
        try:
            file1 = ImageFile(path=tmp_path, size=100, hash="abc123")
            with pytest.raises(ValueError, match="重复组必须包含至少 2 个文件"):
                DuplicateGroup(hash="abc123", files=[file1])
        finally:
            os.unlink(tmp_path)
    
    def test_duplicate_group_sorts_files_by_path(self):
        """Test that DuplicateGroup sorts files by path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path1 = os.path.join(tmpdir, "z_file.jpg")
            path2 = os.path.join(tmpdir, "a_file.jpg")
            
            with open(path1, 'w') as f1, open(path2, 'w') as f2:
                f1.write("test")
                f2.write("test")
            
            file1 = ImageFile(path=path1, size=100, hash="abc123")
            file2 = ImageFile(path=path2, size=100, hash="abc123")
            
            group = DuplicateGroup(hash="abc123", files=[file1, file2])
            # Should be sorted alphabetically
            assert group.files[0].path == path2  # a_file.jpg
            assert group.files[1].path == path1  # z_file.jpg


class TestScanResult:
    """Tests for ScanResult model"""
    
    def test_scan_result_properties(self):
        """Test ScanResult computed properties"""
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = [os.path.join(tmpdir, f"file{i}.jpg") for i in range(4)]
            for path in paths:
                with open(path, 'w') as f:
                    f.write("test")
            
            # Create 2 duplicate groups with 2 files each
            files1 = [ImageFile(path=paths[0], size=100, hash="hash1"),
                     ImageFile(path=paths[1], size=100, hash="hash1")]
            files2 = [ImageFile(path=paths[2], size=200, hash="hash2"),
                     ImageFile(path=paths[3], size=200, hash="hash2")]
            
            group1 = DuplicateGroup(hash="hash1", files=files1)
            group2 = DuplicateGroup(hash="hash2", files=files2)
            
            result = ScanResult(
                total_files=4,
                duplicate_groups=[group1, group2],
                scan_time=1.5
            )
            
            assert result.duplicate_count == 4  # All 4 files are duplicates
            assert result.unique_count == 2  # 2 unique files (one per group)
            assert result.total_wasted_space == 300  # 100 + 200
