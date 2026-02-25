import unittest
from pathlib import Path
import tempfile
import shutil
import logging
from organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):
    """Test cases for the FileOrganizer class."""
    
    def setUp(self):
        """Create a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Remove the temporary directory after testing."""
        # Close any logger handlers first
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)
        
        # Try to remove the directory
        try:
            shutil.rmtree(self.test_dir)
        except (PermissionError, OSError):
            # Windows sometimes locks files temporarily
            import time
            time.sleep(0.1)
            try:
                shutil.rmtree(self.test_dir)
            except Exception:
                pass  # Ignore if we can't delete it
    
    def create_test_files(self):
        """Create test files with various extensions."""
        test_files = [
            ('document.pdf', 'Documents'),
            ('image.jpg', 'Images'),
            ('script.py', 'Code'),
            ('video.mp4', 'Videos'),
            ('audio.mp3', 'Audio'),
            ('archive.zip', 'Archives'),
            ('unknown.xyz', 'Others'),
        ]
        
        for filename, _ in test_files:
            (self.test_path / filename).touch()
        
        return test_files
    
    def test_initialization(self):
        """Test FileOrganizer initialization."""
        organizer = FileOrganizer(str(self.test_path))
        self.assertIsNotNone(organizer)
        self.assertEqual(organizer.target_directory, self.test_path)
    
    def test_invalid_directory(self):
        """Test initialization with invalid directory."""
        with self.assertRaises(ValueError):
            FileOrganizer('/non/existent/directory')
    
    def test_get_file_category(self):
        """Test file categorization."""
        organizer = FileOrganizer(str(self.test_path))
        
        test_cases = [
            ('file.pdf', 'Documents'),
            ('image.jpg', 'Images'),
            ('script.py', 'Code'),
            ('video.mp4', 'Videos'),
            ('audio.mp3', 'Audio'),
            ('archive.zip', 'Archives'),
            ('unknown.xyz', 'Others'),
        ]
        
        for filename, expected_category in test_cases:
            file_path = self.test_path / filename
            category = organizer._get_file_category(file_path)
            self.assertEqual(category, expected_category, 
                           f"File {filename} should be categorized as {expected_category}")
    
    def test_create_category_folder(self):
        """Test category folder creation."""
        organizer = FileOrganizer(str(self.test_path))
        
        category_path = organizer._create_category_folder('Documents')
        
        self.assertTrue(category_path.exists())
        self.assertTrue(category_path.is_dir())
        self.assertEqual(category_path.name, 'Documents')
    
    def test_organize_files(self):
        """Test basic file organization."""
        self.create_test_files()
        organizer = FileOrganizer(str(self.test_path))
        
        stats = organizer.organize()
        
        # Check statistics
        self.assertGreater(stats['organized_files'], 0)
        self.assertGreaterEqual(stats['categories_created'], 2)
        
        # Check folder creation
        self.assertTrue((self.test_path / 'Documents').exists())
        self.assertTrue((self.test_path / 'Images').exists())
        self.assertTrue((self.test_path / 'Code').exists())
        
        # Check file movement
        self.assertTrue((self.test_path / 'Documents' / 'document.pdf').exists())
        self.assertTrue((self.test_path / 'Images' / 'image.jpg').exists())
        self.assertTrue((self.test_path / 'Code' / 'script.py').exists())
    
    def test_dry_run(self):
        """Test dry run mode (no actual file movement)."""
        self.create_test_files()
        organizer = FileOrganizer(str(self.test_path))
        
        # Count files before
        files_before = list(self.test_path.glob('*.pdf')) + list(self.test_path.glob('*.jpg'))
        
        stats = organizer.organize(dry_run=True)
        
        # Check that no folders were created
        self.assertEqual(stats['categories_created'], 0)
        
        # Check that files are still in root
        files_after = list(self.test_path.glob('*.pdf')) + list(self.test_path.glob('*.jpg'))
        self.assertEqual(len(files_before), len(files_after))
    
    def test_custom_categories(self):
        """Test FileOrganizer with custom categories."""
        custom_categories = {
            'Media': ['.jpg', '.png', '.mp4'],
            'Text': ['.txt', '.pdf']
        }
        
        organizer = FileOrganizer(str(self.test_path), categories=custom_categories)
        
        # Test categorization with custom categories
        test_path = self.test_path / 'image.jpg'
        test_path.touch()
        
        category = organizer._get_file_category(test_path)
        self.assertEqual(category, 'Media')
    
    def test_duplicate_filename_handling(self):
        """Test handling of duplicate filenames."""
        # Create two files with the same name
        (self.test_path / 'test.txt').write_text("File 1")
        
        # Create a category folder
        doc_folder = self.test_path / 'Documents'
        doc_folder.mkdir()
        (doc_folder / 'test.txt').write_text("Original")
        
        # Try to move the first file
        organizer = FileOrganizer(str(self.test_path))
        
        # Manually test the move operation
        result = organizer._move_file(self.test_path / 'test.txt', doc_folder)
        
        # Check that file was moved with a new name
        self.assertTrue(result)
        self.assertTrue((doc_folder / 'test_1.txt').exists())
    
    def test_logger_setup(self):
        """Test that logger is properly configured."""
        organizer = FileOrganizer(str(self.test_path))
        
        self.assertIsNotNone(organizer.logger)
        self.assertTrue(str(organizer.log_file).endswith('file_organizer.log'))
    
    def test_get_category_summary(self):
        """Test category summary generation."""
        self.create_test_files()
        organizer = FileOrganizer(str(self.test_path))
        
        organizer.organize()
        summary = organizer.get_category_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertGreater(len(summary), 0)
        self.assertIn('Documents', summary)


class TestFileOrganizerEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def setUp(self):
        """Create a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Remove the temporary directory after testing."""
        # Close any logger handlers first
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)
        
        # Try to remove the directory
        try:
            shutil.rmtree(self.test_dir)
        except (PermissionError, OSError):
            # Windows sometimes locks files temporarily
            import time
            time.sleep(0.1)
            try:
                shutil.rmtree(self.test_dir)
            except Exception:
                pass  # Ignore if we can't delete it
    
    def test_empty_directory(self):
        """Test organizing an empty directory."""
        organizer = FileOrganizer(str(self.test_path))
        stats = organizer.organize()
        
        # The log file is created, so total_files will be 1, but should be skipped
        self.assertEqual(stats['total_files'], 1)
        self.assertEqual(stats['organized_files'], 0)
        self.assertEqual(stats['skipped_files'], 1)
    
    def test_files_with_no_extension(self):
        """Test handling files without extensions."""
        (self.test_path / 'README').touch()
        (self.test_path / 'LICENSE').touch()
        
        organizer = FileOrganizer(str(self.test_path))
        stats = organizer.organize()
        
        # Should be categorized as 'Others'
        others_folder = self.test_path / 'Others'
        self.assertTrue(others_folder.exists())
    
    def test_hidden_files_handling(self):
        """Test that hidden files are also organized."""
        (self.test_path / '.hidden_doc.pdf').touch()
        
        organizer = FileOrganizer(str(self.test_path))
        stats = organizer.organize()
        
        # Hidden files should also be organized
        self.assertGreater(stats['organized_files'], 0)


if __name__ == '__main__':
    unittest.main()
