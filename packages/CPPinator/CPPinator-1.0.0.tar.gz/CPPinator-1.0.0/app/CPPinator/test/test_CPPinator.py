import unittest
from CPPinator import compile_and_run_cpp_files
import os


class TestCPPinator(unittest.TestCase):

    def test_basic_folder(self):
        compile_and_run_cpp_files(directory="./Basic Problems/")
        self.assertFalse(os.path.exists("Basic Problems/a.exe"))
