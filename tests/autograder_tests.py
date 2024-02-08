import unittest
import pandas as pd
import sys
from distutils.version import LooseVersion
import os
import subprocess
import json


class TestCodespace(unittest.TestCase):

    def random_hex_string(self, length=6):
        return os.urandom(length).hex()

    def test_codespace(self):
        
        # Get current machine name
        command = "gh codespace view --json name"
        # Execute the command and capture the output
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Convert the output (JSON string) to a Python dictionary
        output_dict = json.loads(process.stdout)

        # Rename machine
        new_name = self.random_hex_string(20)
        command = f"gh codespace edit -c '{output_dict['name']}' -d '{new_name}'"
        # Execute the command and capture the output
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Get current display name
        command = "gh codespace view --json displayName"
        # Execute the command and capture the output
        process = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Convert the output (JSON string) to a Python dictionary
        output_dict = json.loads(process.stdout)

        # Test
        self.assertEqual(new_name.capitalize, output_dict['displayName'])

        
class TestFileExistence(unittest.TestCase):

    def test_files_existence(self):
        # List of file paths to check
        files_to_check = [
            "requirements.txt",
            ".devcontainer/devcontainer.json",
            ".devcontainer/Dockerfile"
        ]
        
        # Iterate over the list of files and check each one
        for file_path in files_to_check:
            # Check if the file exists
            self.assertTrue(os.path.exists(file_path), f"File does not exist: {file_path}")



class TestConfiguration(unittest.TestCase):

    def test_python_version(self):
        # Check Python version is 3.10.x
        python_version = sys.version_info
        self.assertTrue(python_version.major == 3 and python_version.minor == 10,
                        f"Python version should be 3.10.x, but is {python_version.major}.{python_version.minor}.{python_version.micro}")
        
    def test_pandas_version(self):
        # Get the current version of pandas
        current_version = pd.__version__
        
        # Check if the version is greater than or equal to 1.5 and less than 2.1
        self.assertTrue(LooseVersion("1.5") <= LooseVersion(current_version) < LooseVersion("2.1"),
                        f"Pandas version should be >= 1.5 and < 2.1, but is {current_version}")

if __name__ == '__main__':
    unittest.main()
