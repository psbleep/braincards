#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from braincards import braincards


TEST_DIR = os.path.dirname(os.path.realpath(__file__))

DARK_PIXEL = (25, 25, 25)
LIGHT_PIXEL = (200, 200, 200)

SRC_IMG_DATA = [LIGHT_PIXEL, DARK_PIXEL, DARK_PIXEL, DARK_PIXEL,
                LIGHT_PIXEL, LIGHT_PIXEL, LIGHT_PIXEL, LIGHT_PIXEL,
                LIGHT_PIXEL, LIGHT_PIXEL, DARK_PIXEL, LIGHT_PIXEL]

INPUT_IMG_DATA = [LIGHT_PIXEL, DARK_PIXEL, LIGHT_PIXEL, LIGHT_PIXEL, DARK_PIXEL, LIGHT_PIXEL, LIGHT_PIXEL, LIGHT_PIXEL,
                  LIGHT_PIXEL, DARK_PIXEL, LIGHT_PIXEL, DARK_PIXEL, LIGHT_PIXEL, DARK_PIXEL, DARK_PIXEL, DARK_PIXEL]


class GetBinaryTests(unittest.TestCase):

    def test_pixel_dark(self):
        self.assertEqual(braincards.get_pixel_binary(DARK_PIXEL), "1")

    def test_pixel_light(self):
        self.assertEqual(braincards.get_pixel_binary(LIGHT_PIXEL), "0")

    def test_pixel_is_integer(self):
        self.assertEqual(braincards.get_pixel_binary(DARK_PIXEL[0]), "1")

    def test_segment(self):
        self.assertEqual(braincards.get_segment_binary(1, 4, SRC_IMG_DATA),
                         "0000")


class ParseImageTests(unittest.TestCase):

    def test_parse_image_data_instruction(self):
        self.assertEqual(braincards.parse_image_data(SRC_IMG_DATA), "]>+")

    def test_parse_image_data_input(self):
        self.assertEqual(braincards.parse_image_data(
            INPUT_IMG_DATA, segment_length=braincards.INPUT_SEGMENT_BITS,
            encoder=braincards.get_ascii), "HW")


class MainTests(unittest.TestCase):

    def test_main_function_no_input_stream(self):
        img_data = {"src": [os.path.join(TEST_DIR, "test_src.png")]}
        self.assertEqual(
            braincards.run(**img_data), "?")

    def test_main_function_with_input_stream(self):
        img_data = {"src": [os.path.join(TEST_DIR, "test_src_with_input.png")],
                    "inp": [os.path.join(TEST_DIR, "test_input.png")]}
        self.assertEqual(braincards.run(**img_data), "Hello, World!!!!!!!!!!!!!!!!!!!!")
