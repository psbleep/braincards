import json
import os
import unittest

import braincards.__main__ as cli

from copy import copy

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(TEST_DIR, "test_img_files.json")
TEST_DATA = {"src": ["/fake.img"], "img": ["/other/fake.img"]}
cli.FILE_NAME = TEST_FILE


def reset_file():
    with open(TEST_FILE, "w") as f:
        json.dump(TEST_DATA, f)


def read_file():
    with open(TEST_FILE, "r") as f:
        return json.load(f)


class CLITests(unittest.TestCase):

    def setUp(self):
        reset_file()

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_get_img_files(self):
        self.assertEqual(cli.get_img_files(), TEST_DATA)

    def test_write_img_files(self):
        new_data = {"src": ["/new.img"]}
        cli.write_img_files(new_data)
        self.assertEqual(read_file(), new_data)

    def test_add_img_file_exists(self):
        cli.add_img("src", "/new.img")
        new_src = copy(TEST_DATA["src"])
        new_src.append("/new.img")
        self.assertEqual(read_file()["src"], new_src)

    def test_add_img_file_does_not_exist(self):
        os.remove(TEST_FILE)
        cli.add_img("src", "begin.img")
        self.assertEqual(read_file(), {"src": ["begin.img"]})

    def test_clear_img_all(self):
        cli.clear_img(img_type="all")
        self.assertFalse(os.path.exists(TEST_FILE))

    def test_clear_img_clears_type(self):
        cli.clear_img(img_type="inp")
        self.assertEqual(read_file()["inp"], [])

    def test_clear_img_does_not_clear_other_type(self):
        old_src = copy(TEST_DATA["src"])
        cli.clear_img(img_type="inp")
        self.assertEqual(read_file()["src"], old_src)
