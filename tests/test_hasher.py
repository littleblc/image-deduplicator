"""Tests for the FileHasher class."""

import os
import tempfile
import pytest
from src.image_deduplicator.hasher import FileHasher


class TestFileHasher:
    """Test cases for FileHasher"""
    
    def test_compute_hash_basic(self):
        """Test basic hash computation"""
        hasher = FileHasher()
        
        # Create a temporary file with known content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            # Compute hash
            hash1 = hasher.compute_hash(temp_path)
            
            # Verify it's a valid SHA-256 hash (64 hex characters)
            assert len(hash1) == 64
            assert all(c in '0123456789abcdef' for c in hash1)
            
            # Compute again - should get same result
            hash2 = hasher.compute_hash(temp_path)
            assert hash1 == hash2
        finally:
            os.unlink(temp_path)
    
    def test_compute_hash_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent files"""
        hasher = FileHasher()
        
        with pytest.raises(FileNotFoundError):
            hasher.compute_hash("/nonexistent/file.txt")
    
    def test_compute_hash_directory(self):
        """Test that IOError is raised for directories"""
        hasher = FileHasher()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(IOError):
                hasher.compute_hash(temp_dir)
    
    def test_hash_cache(self):
        """Test that hash caching works"""
        hasher = FileHasher()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("cached content")
            temp_path = f.name
        
        try:
            # First computation
            assert hasher.get_cache_size() == 0
            hash1 = hasher.compute_hash(temp_path)
            assert hasher.get_cache_size() == 1
            
            # Second computation should use cache
            hash2 = hasher.compute_hash(temp_path)
            assert hash1 == hash2
            assert hasher.get_cache_size() == 1
            
            # Clear cache
            hasher.clear_cache()
            assert hasher.get_cache_size() == 0
        finally:
            os.unlink(temp_path)
    
    def test_same_content_same_hash(self):
        """Test that files with same content have same hash"""
        hasher = FileHasher()
        
        # Create two files with identical content
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1:
            f1.write("identical content")
            path1 = f1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
            f2.write("identical content")
            path2 = f2.name
        
        try:
            hash1 = hasher.compute_hash(path1)
            hash2 = hasher.compute_hash(path2)
            
            assert hash1 == hash2
        finally:
            os.unlink(path1)
            os.unlink(path2)
    
    def test_compute_hashes_batch(self):
        """Test batch hash computation"""
        hasher = FileHasher()
        
        # Create multiple temporary files
        temp_files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(f"content {i}")
                temp_files.append(f.name)
        
        try:
            # Compute hashes in batch
            results = hasher.compute_hashes(temp_files)
            
            # Verify all files were processed
            assert len(results) == 3
            for path in temp_files:
                assert path in results
                assert len(results[path]) == 64
        finally:
            for path in temp_files:
                os.unlink(path)
    
    def test_compute_hashes_with_progress(self):
        """Test batch computation with progress callback"""
        hasher = FileHasher()
        
        # Create temporary files
        temp_files = []
        for i in range(2):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(f"content {i}")
                temp_files.append(f.name)
        
        try:
            # Track progress calls
            progress_calls = []
            
            def progress_callback(current, total, file_path):
                progress_calls.append((current, total, file_path))
            
            # Compute with progress
            results = hasher.compute_hashes(temp_files, progress_callback)
            
            # Verify progress was reported
            assert len(progress_calls) == 2
            assert progress_calls[0][0] == 1
            assert progress_calls[0][1] == 2
            assert progress_calls[1][0] == 2
            assert progress_calls[1][1] == 2
        finally:
            for path in temp_files:
                os.unlink(path)
    
    def test_compute_hashes_handles_errors(self):
        """Test that batch computation continues on errors"""
        hasher = FileHasher()
        
        # Create one valid file and one invalid path
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("valid content")
            valid_path = f.name
        
        invalid_path = "/nonexistent/file.txt"
        
        try:
            # Compute hashes - should skip invalid file
            results = hasher.compute_hashes([valid_path, invalid_path])
            
            # Only valid file should be in results
            assert len(results) == 1
            assert valid_path in results
            assert invalid_path not in results
        finally:
            os.unlink(valid_path)
    
    def test_large_file_streaming(self):
        """Test that large files are handled with streaming"""
        hasher = FileHasher()
        
        # Create a file larger than CHUNK_SIZE
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            # Write 20KB of data (larger than 8KB chunk size)
            data = b'x' * (20 * 1024)
            f.write(data)
            temp_path = f.name
        
        try:
            # Should successfully compute hash
            hash_value = hasher.compute_hash(temp_path)
            assert len(hash_value) == 64
        finally:
            os.unlink(temp_path)
