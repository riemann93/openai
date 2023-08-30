import shutil
import unittest
import os
import tempfile

from src.file_manager import FileManager


class FileManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()  # Creates a temporary directory
        self.fm = FileManager()
        self.sample_file_path = os.path.join(self.temp_dir, 'sample.txt')
        self.sample_content = 'Hello, World!'

    def tearDown(self):
        shutil.rmtree(self.temp_dir)  # Removes the temporary directory with all its contents

    def test_read_file_non_existent(self):
        result = self.fm.read_file('non_existent.txt')
        self.assertEqual(result, "Error: File not found.")

    def test_write_file(self):
        result = self.fm.write_file(self.sample_file_path, self.sample_content)
        self.assertEqual(result, f"Content written to {self.sample_file_path}")
        with open(self.sample_file_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, self.sample_content)

    def test_append_to_file(self):
        self.fm.write_file(self.sample_file_path, self.sample_content)
        append_content = '\nAppended Content.'
        result = self.fm.append_to_file(self.sample_file_path, append_content)
        self.assertEqual(result, f"Content appended to {self.sample_file_path}")
        with open(self.sample_file_path, 'r') as file:
            content = file.read()
        self.assertEqual(content, self.sample_content + append_content)

    def test_delete_file(self):
        self.fm.write_file(self.sample_file_path, self.sample_content)
        result = self.fm.delete_file(self.sample_file_path)
        self.assertEqual(result, f"Deleted file: {self.sample_file_path}")
        self.assertFalse(os.path.exists(self.sample_file_path))

    # ... Additional test methods for the remaining FileManager methods

if __name__ == '__main__':
    unittest.main()
