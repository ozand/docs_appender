from fastapi.testclient import TestClient
from backend.src.backend.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "File Combiner API" in response.text

def test_combine_files_endpoint():
    """Test the combine files endpoint with a simple file."""
    files = [
        ("files", ("test1.txt", "Content of test file 1.", "text/plain")),
        ("files", ("test2.txt", "Content of test file 2.", "text/plain"))
    ]
    
    response = client.post(
        "/combine/",
        files=files,
        data={
            "sort_mode": "name",
            "output_format": "markdown"
        }
    )
    
    assert response.status_code == 200
    assert "Combined Files" in response.text
    assert "test1.txt" in response.text
    assert "test2.txt" in response.text
    assert "Content of test file 1." in response.text
    assert "Content of test file 2." in response.text

def test_combine_files_endpoint_json():
    """Test the combine files endpoint with JSON output."""
    files = [
        ("files", ("test1.txt", "Line 1\\nLine 2", "text/plain"))
    ]
    
    response = client.post(
        "/combine/",
        files=files,
        data={
            "sort_mode": "name",
            "output_format": "json"
        }
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    
    import json
    result = json.loads(response.text)
    assert result["metadata"]["title"] == "Combined Files"
    assert len(result["files"]) == 1
    assert result["files"][0]["name"] == "test1.txt"
    assert result["files"][0]["content"] == "Line 1\\nLine 2"

def test_combine_files_endpoint_yaml():
    """Test the combine files endpoint with YAML output."""
    files = [
        ("files", ("test1.txt", "Line A\\nLine B", "text/plain"))
    ]
    
    response = client.post(
        "/combine/",
        files=files,
        data={
            "sort_mode": "name",
            "output_format": "yaml"
        }
    )
    
    assert response.status_code == 200
    assert "application/yaml" in response.headers["content-type"]
    
    import yaml
    result = yaml.safe_load(response.text)
    assert result["metadata"]["title"] == "Combined Files"
    assert len(result["files"]) == 1
    assert result["files"][0]["name"] == "test1.txt"
    assert result["files"][0]["content"] == "Line A\\nLine B"

def test_combine_files_endpoint_no_files():
    """Test the combine files endpoint with no files."""
    response = client.post("/combine/")
    assert response.status_code == 422  # Validation error for missing files

def test_combine_folder_endpoint():
    """Test the combine folder endpoint."""
    import tempfile
    import os
    
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        with open(os.path.join(temp_dir, "file1.txt"), "w") as f:
            f.write("Content of file 1.")
        with open(os.path.join(temp_dir, "file2.txt"), "w") as f:
            f.write("Content of file 2.")
        
        response = client.post(
            "/combine-folder/",
            data={
                "folder_path": temp_dir,
                "sort_mode": "name",
                "output_format": "markdown"
            }
        )
        
        assert response.status_code == 200
        assert "Combined Files" in response.text
        assert "file1.txt" in response.text
        assert "file2.txt" in response.text
        assert "Content of file 1." in response.text
        assert "Content of file 2." in response.text

def test_combine_folder_endpoint_invalid_path():
    """Test the combine folder endpoint with invalid path."""
    response = client.post(
        "/combine-folder/",
        data={
            "folder_path": "/invalid/path",
            "sort_mode": "name"
        }
    )
    
    assert response.status_code == 400
    assert "does not exist or is not a directory" in response.text