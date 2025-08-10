# Testing Instructions for Folder Selection Feature

## Prerequisites
1. Ensure both backend and frontend servers are running
2. The test_folder directory should be present with test files

## Test Cases

### 1. Basic Folder Processing
- Open the frontend application
- Select "Select Folder" option
- Enter the path to "test_folder" directory
- Click "Combine Files"
- Verify that all .txt, .md, and .py files are included in the output
- Check that the content of each file is correctly combined

### 2. Extension Filtering
- Open the frontend application
- Select "Select Folder" option
- Enter the path to "test_folder" directory
- In the extension filter field, enter ".txt .md"
- Click "Combine Files"
- Verify that only .txt and .md files are included in the output
- Confirm that .py and .log files are excluded

### 3. File Upload (Regression Test)
- Open the frontend application
- Select "Upload Files" option
- Upload several files from test_folder
- Click "Combine Files"
- Verify that the functionality still works as expected for file uploads

### 4. Empty Folder/Invalid Path
- Open the frontend application
- Select "Select Folder" option
- Enter an invalid path
- Click "Combine Files"
- Verify that an appropriate error message is displayed

## Expected Results
- Folder processing should work correctly
- Extension filtering should properly include/exclude files
- File upload functionality should remain unaffected
- Error handling should be appropriate for invalid inputs

## Test Results
- [ ] Basic Folder Processing
- [ ] Extension Filtering
- [ ] File Upload (Regression Test)
- [ ] Empty Folder/Invalid Path