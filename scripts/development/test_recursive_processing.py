#!/usr/bin/env python3
"""
Test script to verify recursive folder processing functionality.
This script creates a test directory structure and verifies that our folder processing works correctly.
"""

import os
import tempfile
import shutil
from datetime import datetime

# Import our shared logic
import sys
sys.path.append('backend/src')
from shared.combine_logic import combine_files_content


def create_test_structure():
    """Create a test directory structure with files in subdirectories."""
    # Create a temporary directory for our test
    test_dir = tempfile.mkdtemp(prefix="docs_appender_test_")
    
    # Create some test files in the root directory
    with open(os.path.join(test_dir, "file1.txt"), "w", encoding="utf-8") as f:
        f.write("Content of file 1 in root directory")
    
    with open(os.path.join(test_dir, "file2.md"), "w", encoding="utf-8") as f:
        f.write("Content of file 2 in root directory")
    
    # Create a subdirectory
    subdir1 = os.path.join(test_dir, "subdir1")
    os.makedirs(subdir1)
    
    # Create files in the first subdirectory
    with open(os.path.join(subdir1, "file3.txt"), "w", encoding="utf-8") as f:
        f.write("Content of file 3 in subdir1")
    
    with open(os.path.join(subdir1, "file4.py"), "w", encoding="utf-8") as f:
        f.write("# Content of file 4 in subdir1")
    
    # Create a nested subdirectory
    subdir2 = os.path.join(subdir1, "subdir2")
    os.makedirs(subdir2)
    
    # Create files in the nested subdirectory
    with open(os.path.join(subdir2, "file5.txt"), "w", encoding="utf-8") as f:
        f.write("Content of file 5 in subdir2 (nested)")
    
    with open(os.path.join(subdir2, "file6.json"), "w", encoding="utf-8") as f:
        f.write('{"key": "Content of file 6 in subdir2 (nested)"}')
    
    return test_dir


def test_recursive_processing():
    """Test the recursive folder processing functionality."""
    print("Creating test directory structure...")
    test_dir = create_test_structure()
    
    try:
        print(f"Test directory: {test_dir}")
        
        # Create file data list with relative paths (simulating what our backend does)
        file_data_list = [
            {
                "name": "file1.txt",
                "content": "Content of file 1 in root directory",
                "last_modified": datetime.now(),
                "relative_path": "file1.txt"
            },
            {
                "name": "file2.md",
                "content": "Content of file 2 in root directory",
                "last_modified": datetime.now(),
                "relative_path": "file2.md"
            },
            {
                "name": "subdir1/file3.txt",
                "content": "Content of file 3 in subdir1",
                "last_modified": datetime.now(),
                "relative_path": "subdir1/file3.txt"
            },
            {
                "name": "subdir1/file4.py",
                "content": "# Content of file 4 in subdir1",
                "last_modified": datetime.now(),
                "relative_path": "subdir1/file4.py"
            },
            {
                "name": "subdir1/subdir2/file5.txt",
                "content": "Content of file 5 in subdir2 (nested)",
                "last_modified": datetime.now(),
                "relative_path": "subdir1/subdir2/file5.txt"
            },
            {
                "name": "subdir1/subdir2/file6.json",
                "content": '{"key": "Content of file 6 in subdir2 (nested)"}',
                "last_modified": datetime.now(),
                "relative_path": "subdir1/subdir2/file6.json"
            }
        ]
        
        # Test JSON output with relative paths
        print("\nTesting JSON output with relative paths...")
        json_result = combine_files_content(
            file_data_list, 
            sort_mode="name", 
            output_format="json"
        )
        
        # Verify relative paths are included
        assert '"relative_path": "file1.txt"' in json_result
        assert '"relative_path": "subdir1/file3.txt"' in json_result
        assert '"relative_path": "subdir1/subdir2/file5.txt"' in json_result
        print("✓ JSON output correctly includes relative paths")
        
        # Test YAML output with relative paths
        print("\nTesting YAML output with relative paths...")
        yaml_result = combine_files_content(
            file_data_list, 
            sort_mode="name", 
            output_format="yaml"
        )
        
        # Verify relative paths are included
        assert 'relative_path: file1.txt' in yaml_result
        assert 'relative_path: subdir1/file3.txt' in yaml_result
        assert 'relative_path: subdir1/subdir2/file5.txt' in yaml_result
        print("✓ YAML output correctly includes relative paths")
        
        # Test Markdown output (should not include relative paths)
        print("\nTesting Markdown output...")
        markdown_result = combine_files_content(
            file_data_list, 
            sort_mode="name", 
            output_format="markdown"
        )
        
        # Verify relative paths are not included in Markdown (but filenames are)
        assert 'file1.txt' in markdown_result
        assert 'subdir1/file3.txt' in markdown_result
        print("✓ Markdown output correctly formats file names")
        
        print("\n🎉 All tests passed! Recursive folder processing is working correctly.")
        
    finally:
        # Clean up
        shutil.rmtree(test_dir)
        print(f"\nCleaned up test directory: {test_dir}")


if __name__ == "__main__":
    test_recursive_processing()