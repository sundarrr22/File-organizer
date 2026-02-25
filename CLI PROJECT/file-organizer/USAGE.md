# Quick Start Guide

## Installation (First Time Only)

### Windows
```bash
# Open PowerShell in the file-organizer directory
python -m venv venv
venv\Scripts\activate
# No packages to install!
```

### Linux/macOS
```bash
# Open terminal in the file-organizer directory
python3 -m venv venv
source venv/bin/activate
# No packages to install!
```

## Running the Tool

### Option 1: Using Python Directly

**Windows:**
```bash
python cli.py "C:\path\to\your\folder"
```

**Linux/macOS:**
```bash
python3 cli.py /path/to/your/folder
```

### Option 2: Using Wrapper Scripts

**Windows (PowerShell/CMD):**
```bash
.\organizer.bat C:\Users\YourName\Downloads
```

**Linux/macOS (Terminal):**
```bash
chmod +x organizer.sh  # First time only
./organizer.sh ~/Downloads
```

## Common Commands

### Preview changes (recommended first step)
```bash
python cli.py "C:\Your\Folder" --dry-run
```

### Actually organize files
```bash
python cli.py "C:\Your\Folder"
```

### Organize recursively (includes subfolders)
```bash
python cli.py "C:\Your\Folder" --recursive
```

### Show available categories
```bash
python cli.py "C:\Your\Folder" --show-categories
```

### Use custom configuration
```bash
python cli.py "C:\Your\Folder" --custom-config config_example.json
```

## Understanding the Output

After running the tool, you'll see:

```
Using categories:
  • Images
  • Documents
  • Videos
  [... more categories ...]

[ACTUAL RUN] Files will be moved. Starting organization...

============================================================
ORGANIZATION SUMMARY
============================================================
Total files processed:    45
Files organized:          42
Files skipped:            2
Failed operations:        1
Categories created:       6
============================================================

Category Summary:
  Documents        : 12 files
  Images           : 15 files
  Videos           : 8 files
  Archives         : 5 files
  Code             : 2 files

Log file: C:\Your\Folder\file_organizer.log
```

## Important Files Created

- **file_organizer.log**: Detailed log of all operations
- **organization_log.json**: Machine-readable record of file movements
- **Category folders**: Images/, Documents/, Videos/, etc.

## Troubleshooting

### "Python is not installed or not in PATH"
Install Python 3.7+ from https://www.python.org/

### "Permission denied" errors
- Run as administrator (Windows) or use `sudo` (Linux/macOS)
- Check folder permissions

### Files not organized?
- Use `--show-categories` to see available categories
- Create a custom config with categories you need
- Use `--dry-run` first to see what would happen

## Tips

1. **Always use `--dry-run` first** to preview changes
2. **Backup important files** before running on important folders
3. **Check the log file** if something goes wrong
4. **Use custom configs** for specific file types
5. **Use `--recursive`** only if you want to organize subfolders too

## Test It First

To safely test the tool:
1. Create a test folder with sample files
2. Run with `--dry-run` first
3. Check the preview output
4. Run without `--dry-run` if everything looks good

## Getting Help

```bash
python cli.py --help
```

This shows all available options and examples.

---

**Need more info?** See README.md for detailed documentation.
