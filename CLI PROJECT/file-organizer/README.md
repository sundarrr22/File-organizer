# File Organizer CLI Tool

A powerful command-line tool in Python that scans a target directory, categorizes files by type, and automatically sorts them into subfolders. Built with production-quality code including comprehensive logging, error handling, and testing.

## Features

- **Automatic File Categorization**: Organizes files into categories (Images, Documents, Videos, Audio, Archives, Code, Executables, Data, Others)
- **Directory Traversal**: Supports both shallow and recursive directory organization
- **Dry Run Mode**: Preview changes before actually moving files
- **Comprehensive Logging**: Detailed logging of all operations to file and console
- **Custom Categories**: Support for custom file category configurations via JSON
- **Duplicate Handling**: Automatically handles filename conflicts
- **Operation Log**: JSON log of all file movements for audit trails
- **Error Recovery**: Robust error handling with detailed error messages
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Installation

### Prerequisites
- Python 3.7+
- No external dependencies required (uses standard library)

### Setup

```bash
# Navigate to the file-organizer directory
cd file-organizer

# (Optional) Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# No pip packages needed - uses Python standard library only!
```

## Usage

### Basic Usage

```bash
# Organize files in the current directory
python cli.py .

# Organize a specific directory
python cli.py /path/to/directory

# Organize recursively (includes subdirectories)
python cli.py /path/to/directory --recursive

# Preview changes without moving files (dry run)
python cli.py /path/to/directory --dry-run

# Show available file categories
python cli.py /path/to/directory --show-categories
```

### Advanced Usage

```bash
# Use custom configuration
python cli.py /path/to/directory --custom-config config_example.json

# Specify custom log file location
python cli.py /path/to/directory --log-file organizer.log

# Combine options
python cli.py /path/to/directory --recursive --dry-run --custom-config custom_categories.json
```

## Default File Categories

| Category | Extensions |
|----------|-----------|
| **Images** | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp, .ico, .tiff |
| **Documents** | .pdf, .doc, .docx, .txt, .xlsx, .xls, .ppt, .pptx, .odt |
| **Videos** | .mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .m4v |
| **Audio** | .mp3, .wav, .aac, .flac, .wma, .ogg, .m4a, .opus |
| **Archives** | .zip, .rar, .7z, .tar, .gz, .bz2, .xz, .iso |
| **Code** | .py, .js, .ts, .java, .cpp, .c, .h, .cs, .rb, .php, .go, .rs, .html, .css, .json, .xml, .yaml, .sh, .bat, .ps1 |
| **Executables** | .exe, .msi, .app, .bin, .com, .run, .deb, .rpm |
| **Data** | .csv, .sql, .db, .sqlite |
| **Others** | Anything not in above categories |

## Custom Configuration

Create a JSON file to define custom categories:

```json
{
  "CustomCategory": [".ext1", ".ext2", ".ext3"],
  "AnotherCategory": [".ext4", ".ext5"]
}
```

Use it with:
```bash
python cli.py /path/to/directory --custom-config custom_config.json
```

## Output

The tool provides:

1. **Console Output**: Real-time progress information
2. **Log File** (`file_organizer.log`): Detailed file operation logs
3. **Operation Log** (`organization_log.json`): JSON file with all movements for audit trails
4. **Statistics**: Summary of files organized, errors, and categories created

Example statistics output:
```
============================================================
ORGANIZATION SUMMARY
============================================================
Total files processed:    45
Files organized:          42
Files skipped:            2
Failed operations:        1
Categories created:       6
============================================================
```

## Module Architecture

### `organizer.py`
Core `FileOrganizer` class with the following methods:
- `organize()`: Basic file organization in target directory
- `organize_recursive()`: Recursive organization through subdirectories
- `get_category_summary()`: Get file count per category
- `_get_file_category()`: Determine file category by extension
- `_create_category_folder()`: Create category folders
- `_move_file()`: Move files with duplicate handling
- `_save_operation_log()`: Save operation logs to JSON

### `cli.py`
Command-line interface with argument parsing and user-friendly output

### `test_organizer.py`
Comprehensive test suite covering:
- File categorization
- Directory operations
- Dry run mode
- Custom categories
- Edge cases (empty directories, hidden files, no extensions)
- Duplicate filename handling

## Examples

### Example 1: Basic Organization
```bash
$ python cli.py ~/Downloads --dry-run
```
This previews how files would be organized in the Downloads folder.

### Example 2: Recursive Organization
```bash
$ python cli.py ~/Documents --recursive
```
Organizes all files in Documents and all subdirectories into category folders.

### Example 3: Custom Categories
Create `my_config.json`:
```json
{
  "Projects": [".psd", ".ai", ".xd"],
  "Media": [".mp4", ".jpg", ".png"],
  "Source": [".py", ".js", ".java"]
}
```

Then run:
```bash
$ python cli.py ~/Desktop --custom-config my_config.json
```

## Testing

Run the test suite:
```bash
python -m unittest test_organizer.py -v
```

Run specific test class:
```bash
python -m unittest test_organizer.TestFileOrganizer -v
```

Run specific test:
```bash
python -m unittest test_organizer.TestFileOrganizer.test_organize_files -v
```

## Logging Details

The tool maintains two types of logs:

1. **Human-readable log** (`file_organizer.log`):
   ```
   2026-02-25 14:30:15 - FileOrganizer - INFO - Created category folder: Documents
   2026-02-25 14:30:15 - FileOrganizer - INFO - Moved: report.pdf -> Documents/
   ```

2. **Machine-readable JSON log** (`organization_log.json`):
   ```json
   [
     {
       "timestamp": "2026-02-25T14:30:15.123456",
       "action": "move",
       "source": "/path/to/report.pdf",
       "destination": "/path/to/Documents/report.pdf",
       "status": "success"
     }
   ]
   ```

## Error Handling

The tool gracefully handles:
- Missing or inaccessible directories
- Invalid file paths
- Permission errors
- Duplicate filenames (renames with counter)
- Log file write failures
- Directory creation failures

## Performance Notes

- Tested on directories with 1000+ files
- Minimal memory footprint using Python's `pathlib` and `os.walk()`
- Efficient file categorization using dictionary lookups
- Directory creation is optimized to run once per category

## System Requirements

- **OS**: Windows, Linux, macOS
- **Python**: 3.7 or higher
- **Standard Library Modules**: `os`, `shutil`, `logging`, `pathlib`, `json`

## Known Limitations

1. Symbolic links are followed (on Linux/macOS)
2. Very large files (>5GB) may take time to move
3. Network drives may have slower performance

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to extend the tool by:
- Adding more default categories
- Implementing compression for archives
- Adding GUI interface
- Creating language-specific category presets

## Support

For issues or questions, check the logs first:
- Look in `file_organizer.log` for detailed error messages
- Check `organization_log.json` for operation history
- Use `--dry-run` mode to test changes safely

---

**Created**: February 2026  
**Python Version**: 3.7+  
**Status**: Production Ready
