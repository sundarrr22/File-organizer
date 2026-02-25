#!/usr/bin/env python3
"""
File Organizer CLI - A command-line tool to organize files into categories.

Usage:
    python cli.py <target_directory> [--recursive] [--dry-run] [--custom-config CONFIG_FILE]
"""

import argparse
import sys
from pathlib import Path
import json
from organizer import FileOrganizer


def load_custom_config(config_file: str) -> dict:
    """
    Load custom category configuration from a JSON file.
    
    Args:
        config_file: Path to JSON configuration file
        
    Returns:
        Dictionary with category mappings
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"Loaded custom configuration from: {config_file}")
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in configuration file: {config_file}")
        sys.exit(1)


def display_categories(categories: dict):
    """Display available file categories."""
    print("\nFile Categories:")
    print("-" * 60)
    for category, extensions in categories.items():
        ext_str = ", ".join(extensions)
        print(f"{category:15} | {ext_str}")
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by categorizing them into subfolders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py /path/to/directory                    # Organize files
  python cli.py /path/to/directory --recursive        # Organize recursively
  python cli.py /path/to/directory --dry-run          # Preview changes
  python cli.py /path/to/directory --custom-config config.json  # Use custom config
        """
    )
    
    parser.add_argument(
        'directory',
        type=str,
        help='Target directory to organize'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Organize files recursively in all subdirectories'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be done without actually moving files'
    )
    
    parser.add_argument(
        '--custom-config',
        type=str,
        help='Path to custom JSON configuration file with category mappings'
    )
    
    parser.add_argument(
        '--show-categories',
        action='store_true',
        help='Display available file categories and exit'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        help='Custom path for the log file'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    target_dir = Path(args.directory)
    if not target_dir.exists():
        print(f"Error: Directory does not exist: {args.directory}")
        sys.exit(1)
    
    if not target_dir.is_dir():
        print(f"Error: Path is not a directory: {args.directory}")
        sys.exit(1)
    
    # Load configuration
    categories = None
    if args.custom_config:
        categories = load_custom_config(args.custom_config)
    
    # Initialize organizer
    try:
        organizer = FileOrganizer(
            target_directory=str(target_dir),
            categories=categories,
            log_file=args.log_file
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Show categories if requested
    if args.show_categories:
        display_categories(organizer.categories)
        sys.exit(0)
    
    # Display categories being used
    print("\nUsing categories:")
    for category in organizer.categories.keys():
        print(f"  • {category}")
    
    if args.dry_run:
        print("\n[DRY RUN MODE] Files will not be moved. Preview results:\n")
    else:
        print("\n[ACTUAL RUN] Files will be moved. Starting organization...\n")
    
    # Perform organization
    try:
        if args.recursive:
            print(f"Organizing files recursively in: {target_dir}\n")
            stats = organizer.organize_recursive(dry_run=args.dry_run)
        else:
            print(f"Organizing files in: {target_dir}\n")
            stats = organizer.organize(dry_run=args.dry_run)
        
        # Display results
        print("\n" + "=" * 60)
        print("ORGANIZATION SUMMARY")
        print("=" * 60)
        print(f"Total files processed:    {stats['total_files']}")
        print(f"Files organized:          {stats['organized_files']}")
        print(f"Files skipped:            {stats['skipped_files']}")
        print(f"Failed operations:        {stats['failed_files']}")
        print(f"Categories created:       {stats['categories_created']}")
        
        if 'directories_processed' in stats:
            print(f"Directories processed:    {stats['directories_processed']}")
        
        print("=" * 60)
        
        # Show category summary (unless it's a dry run)
        if not args.dry_run:
            summary = organizer.get_category_summary()
            if summary:
                print("\nCategory Summary:")
                for category, count in sorted(summary.items()):
                    print(f"  {category:15} : {count} files")
        
        print(f"\nLog file: {organizer.log_file}")
        
        # Return exit code based on results
        if stats['failed_files'] > 0:
            return 1
        return 0
        
    except Exception as e:
        print(f"Error during organization: {e}")
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())
