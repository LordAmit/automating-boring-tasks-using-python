import unittest
import library.file_handler as file_handler

file_address = "/home/username/file.bmp"
file_address_with_modified = "/home/username/file_modified.bmp"
filename = "file"
ext = ".bmp"
fake_ext = ".txt"
file_dir = "/home/username/"


class Test_filehandler(unittest.TestCase):
    def test_filename_wo_ext(self):
        global file_address
        global filename
        self.assertEqual(file_handler.extract_filename_wo_ext(
            file_address), filename)

    def test_filepath_modified_prefix(self):
        global file
        global file_address
        global file_address_with_modified
        self.assertEqual(file_handler.filepath_modified_suffix(
            file_address), file_address_with_modified)

    def test_extract_dir(self):
        global file_address
        global file_dir
        self.assertEqual(file_handler.extract_dir(file_address), file_dir)

    def test_extract_ext(self):
        global file_address
        global ext
        self.assertEqual(file_handler.extract_ext(file_address), ext)

    def test_check_ext(self):
        global ext
        self.assertTrue(file_handler.check_ext(ext))
        self.assertFalse(file_handler.check_ext("habijabi"))
