import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import json


class FileOrganizer:
    """
    A utility class to organize files in a directory by categorizing them into subfolders.
    Supports file categorization by type and maintains a log of all operations.
    """
    
    # Default file type categories
    DEFAULT_CATEGORIES = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.odt'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
        'Audio': ['.mp3', '.wav', '.aac', '.flac', '.wma', '.ogg', '.m4a', '.opus'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso'],
        'Code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.cs', '.rb', '.php', '.go', '.rs',
                 '.html', '.css', '.json', '.xml', '.yaml', '.yml', '.sh', '.bat', '.ps1'],
        'Executables': ['.exe', '.msi', '.app', '.bin', '.com', '.run', '.deb', '.rpm'],
        'Data': ['.csv', '.sql', '.db', '.sqlite', '.json', '.xml', '.yaml']
    }
    
    def __init__(self, target_directory: str, categories: Dict[str, List[str]] = None, log_file: str = None):
        """
        Initialize the FileOrganizer.
        
        Args:
            target_directory: The directory to organize
            categories: Custom category mappings (optional)
            log_file: Path to log file (optional)
        """
        self.target_directory = Path(target_directory)
        self.categories = categories or self.DEFAULT_CATEGORIES
        self.operations_log = []
        
        if not self.target_directory.exists():
            raise ValueError(f"Target directory does not exist: {target_directory}")
        
        if not self.target_directory.is_dir():
            raise ValueError(f"Target path is not a directory: {target_directory}")
        
        # Setup logging
        self.log_file = log_file or self.target_directory / "file_organizer.log"
        self._setup_logger()
    
    def _setup_logger(self):
        """Configure logging system."""
        self.logger = logging.getLogger('FileOrganizer')
        self.logger.setLevel(logging.DEBUG)
        
        # Remove any existing handlers to avoid duplicates
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def _get_file_category(self, file_path: Path) -> str:
        """
        Determine the category of a file based on its extension.
        
        Args:
            file_path: Path object of the file
            
        Returns:
            Category name or 'Others' if no match found
        """
        file_extension = file_path.suffix.lower()
        
        for category, extensions in self.categories.items():
            if file_extension in extensions:
                return category
        
        return 'Others'
    
    def _create_category_folder(self, category: str) -> Path:
        """
        Create a category folder if it doesn't exist.
        
        Args:
            category: Name of the category
            
        Returns:
            Path object of the category folder
        """
        category_path = self.target_directory / category
        
        if not category_path.exists():
            try:
                category_path.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Created category folder: {category}")
            except Exception as e:
                self.logger.error(f"Failed to create category folder {category}: {e}")
                raise
        
        return category_path
    
    def _move_file(self, file_path: Path, destination: Path) -> bool:
        """
        Move a file to the destination folder.
        
        Args:
            file_path: Source file path
            destination: Destination folder path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Handle duplicate filenames
            destination_file = destination / file_path.name
            counter = 1
            
            while destination_file.exists():
                name_parts = file_path.stem, file_path.suffix
                new_name = f"{name_parts[0]}_{counter}{name_parts[1]}"
                destination_file = destination / new_name
                counter += 1
            
            shutil.move(str(file_path), str(destination_file))
            self.logger.info(f"Moved: {file_path.name} -> {destination.name}/")
            
            # Log operation
            self.operations_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'move',
                'source': str(file_path),
                'destination': str(destination_file),
                'status': 'success'
            })
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to move {file_path.name}: {e}")
            self.operations_log.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'move',
                'source': str(file_path),
                'destination': str(destination),
                'status': 'failed',
                'error': str(e)
            })
            return False
    
    def organize(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Organize files in the target directory into category subfolders.
        
        Args:
            dry_run: If True, print what would be done without actually moving files
            
        Returns:
            Dictionary with statistics about the organization (files moved, errors, etc.)
        """
        stats = {
            'total_files': 0,
            'organized_files': 0,
            'skipped_files': 0,
            'failed_files': 0,
            'categories_created': 0
        }
        
        self.logger.info(f"Starting file organization in: {self.target_directory}")
        if dry_run:
            self.logger.info("DRY RUN MODE - No files will be moved")
        
        try:
            # Get all files in target directory (non-recursive by default)
            files = [f for f in self.target_directory.iterdir() if f.is_file()]
            stats['total_files'] = len(files)
            
            self.logger.info(f"Found {stats['total_files']} files to process")
            
            # Create a dict to track categories created
            created_categories = set()
            
            for file_path in files:
                # Skip the log file itself
                if file_path.name == 'file_organizer.log' or file_path.name == 'organization_log.json':
                    stats['skipped_files'] += 1
                    continue
                
                category = self._get_file_category(file_path)
                
                if dry_run:
                    self.logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
                    stats['organized_files'] += 1
                else:
                    # Create category folder
                    if category not in created_categories:
                        try:
                            self._create_category_folder(category)
                            created_categories.add(category)
                            stats['categories_created'] += 1
                        except Exception:
                            stats['failed_files'] += 1
                            continue
                    
                    # Move file
                    destination = self.target_directory / category
                    if self._move_file(file_path, destination):
                        stats['organized_files'] += 1
                    else:
                        stats['failed_files'] += 1
            
            self.logger.info(f"Organization complete: {stats['organized_files']} files organized, "
                           f"{stats['failed_files']} failed, {stats['skipped_files']} skipped")
            
            # Save operation log
            if not dry_run:
                self._save_operation_log()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Fatal error during organization: {e}", exc_info=True)
            raise
    
    def organize_recursive(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Recursively organize files in the target directory and all subdirectories.
        
        Args:
            dry_run: If True, print what would be done without actually moving files
            
        Returns:
            Dictionary with statistics about the organization
        """
        stats = {
            'total_files': 0,
            'organized_files': 0,
            'skipped_files': 0,
            'failed_files': 0,
            'categories_created': 0,
            'directories_processed': 0
        }
        
        self.logger.info(f"Starting recursive file organization in: {self.target_directory}")
        
        try:
            created_categories = set()
            
            # Walk through all directories
            for root, dirs, files in os.walk(self.target_directory):
                root_path = Path(root)
                
                # Skip the main directory for now (will process it separately)
                if root_path == self.target_directory:
                    continue
                
                stats['directories_processed'] += 1
                self.logger.debug(f"Processing directory: {root}")
                
                for filename in files:
                    file_path = root_path / filename
                    
                    # Skip log files
                    if filename in ['file_organizer.log', 'organization_log.json']:
                        stats['skipped_files'] += 1
                        continue
                    
                    stats['total_files'] += 1
                    category = self._get_file_category(file_path)
                    
                    if dry_run:
                        self.logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
                        stats['organized_files'] += 1
                    else:
                        if category not in created_categories:
                            try:
                                self._create_category_folder(category)
                                created_categories.add(category)
                                stats['categories_created'] += 1
                            except Exception:
                                stats['failed_files'] += 1
                                continue
                        
                        destination = self.target_directory / category
                        if self._move_file(file_path, destination):
                            stats['organized_files'] += 1
                        else:
                            stats['failed_files'] += 1
            
            # Now process files in the main directory
            files_in_root = [f for f in self.target_directory.iterdir() 
                           if f.is_file() and f.name not in ['file_organizer.log', 'organization_log.json']]
            
            for file_path in files_in_root:
                stats['total_files'] += 1
                category = self._get_file_category(file_path)
                
                if dry_run:
                    self.logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")
                    stats['organized_files'] += 1
                else:
                    if category not in created_categories:
                        try:
                            self._create_category_folder(category)
                            created_categories.add(category)
                            stats['categories_created'] += 1
                        except Exception:
                            stats['failed_files'] += 1
                            continue
                    
                    destination = self.target_directory / category
                    if self._move_file(file_path, destination):
                        stats['organized_files'] += 1
                    else:
                        stats['failed_files'] += 1
            
            self.logger.info(f"Recursive organization complete: {stats['organized_files']} files organized")
            
            if not dry_run:
                self._save_operation_log()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Fatal error during recursive organization: {e}", exc_info=True)
            raise
    
    def _save_operation_log(self):
        """Save operation log to JSON file."""
        log_path = self.target_directory / "organization_log.json"
        
        try:
            with open(log_path, 'w') as f:
                json.dump(self.operations_log, f, indent=2)
            self.logger.info(f"Operation log saved to: {log_path}")
        except Exception as e:
            self.logger.error(f"Failed to save operation log: {e}")
    
    def get_category_summary(self) -> Dict[str, int]:
        """
        Get a summary of files in each category.
        
        Returns:
            Dictionary with category names and file counts
        """
        summary = {}
        
        for category_path in self.target_directory.iterdir():
            if category_path.is_dir() and category_path.name in self.categories:
                file_count = len([f for f in category_path.iterdir() if f.is_file()])
                summary[category_path.name] = file_count
        
        return summary
