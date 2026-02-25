#!/bin/bash
# File Organizer CLI - Linux/macOS Wrapper Script
# 
# Usage:
#   ./organizer.sh <directory> [options]
#
# Examples:
#   ./organizer.sh .
#   ./organizer.sh ~/Downloads --recursive
#   ./organizer.sh ~/Documents --dry-run
#   ./organizer.sh . --recursive --dry-run
#
# Make this script executable with: chmod +x organizer.sh

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the CLI using python3
python3 "$SCRIPT_DIR/cli.py" "$@"

exit $?
