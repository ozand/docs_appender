from datetime import datetime

from backend.src.shared.combine_logic import combine_files_content


def test_combine_files_content_with_relative_paths():
    """Test that combine_files_content correctly handles files with relative paths for JSON output."""
    # Create test data with relative paths
    file_data_list = [
        {
            "name": "file1.txt",
            "content": "Content of file 1",
            "last_modified": datetime(2023, 1, 1, 12, 0, 0),
            "relative_path": "file1.txt"
        },
        {
            "name": "subdir/file2.txt",
            "content": "Content of file 2",
            "last_modified": datetime(2023, 1, 2, 12, 0, 0),
            "relative_path": "subdir/file2.txt"
        }
    ]
    
    # Test JSON output with relative paths
    result = combine_files_content(
        file_data_list, 
        sort_mode="name", 
        output_format="json"
    )
    
    # Parse the JSON result
    import json
    result_data = json.loads(result)
    
    # Check that relative paths are included in the output
    assert "files" in result_data
    assert len(result_data["files"]) == 2
    
    # Check first file
    file1 = result_data["files"][0]
    assert file1["name"] == "file1.txt"
    assert file1["relative_path"] == "file1.txt"
    
    # Check second file
    file2 = result_data["files"][1]
    assert file2["name"] == "subdir/file2.txt"
    assert file2["relative_path"] == "subdir/file2.txt"


def test_combine_files_content_without_relative_paths():
    """Test that combine_files_content works correctly without relative paths."""
    # Create test data without relative paths
    file_data_list = [
        {
            "name": "file1.txt",
            "content": "Content of file 1",
            "last_modified": datetime(2023, 1, 1, 12, 0, 0)
        },
        {
            "name": "file2.txt",
            "content": "Content of file 2",
            "last_modified": datetime(2023, 1, 2, 12, 0, 0)
        }
    ]
    
    # Test JSON output without relative paths
    result = combine_files_content(
        file_data_list, 
        sort_mode="name", 
        output_format="json"
    )
    
    # Parse the JSON result
    import json
    result_data = json.loads(result)
    
    # Check that relative paths are not included in the output
    assert "files" in result_data
    assert len(result_data["files"]) == 2
    
    # Check first file (should not have relative_path)
    file1 = result_data["files"][0]
    assert file1["name"] == "file1.txt"
    assert "relative_path" not in file1
    
    # Check second file (should not have relative_path)
    file2 = result_data["files"][1]
    assert file2["name"] == "file2.txt"
    assert "relative_path" not in file2