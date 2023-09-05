import os
import shutil


class FileManager:
    def __init__(self, base_directory=""):
        self.base_directory = base_directory

    def _get_full_path(self, filename):
        return os.path.join(self.base_directory, filename)

    def read_file(self, filename):
        full_path = self._get_full_path(filename)
        try:
            with open(full_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "Error: File not found."

    def write_file(self, filename, content):
        full_path = self._get_full_path(filename)
        try:
            with open(full_path, 'w') as file:
                file.write(content)
            return f"Content written to {full_path}"
        except Exception as e:
            return f"Error writing to the file: {e}"

    def append_to_file(self, filename, content):
        try:
            with open(filename, 'a') as file:
                file.write(content)
            return f"Content appended to {filename}"
        except Exception as e:
            return f"Error appending to the file: {e}"

    def delete_file(self, filename):
        try:
            os.remove(filename)
            return f"Deleted file: {filename}"
        except Exception as e:
            return f"Error deleting file: {e}"

    def create_directory(self, dirname):
        try:
            os.makedirs(dirname)
            return f"Directory {dirname} created successfully."
        except Exception as e:
            return f"Error creating directory: {e}"

    def list_directory_contents(self, dirpath="."):
        try:
            return os.listdir(dirpath)
        except Exception as e:
            return f"Error listing directory contents: {e}"

    def move_file(self, src, dest):
        try:
            shutil.move(src, dest)
            return f"Moved {src} to {dest}"
        except Exception as e:
            return f"Error moving file: {e}"

    def copy_file(self, src, dest):
        try:
            shutil.copy2(src, dest)
            return f"Copied {src} to {dest}"
        except Exception as e:
            return f"Error copying file: {e}"
