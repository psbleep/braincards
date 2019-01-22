#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bfi

from PIL import Image

INSTRUCTION_SEGMENT_BITS = 4
INPUT_SEGMENT_BITS = 8
COLUMNS = 16
ROWS = 16

INSTRUCTIONS = {
    "0000": ">",
    "0001": "<",
    "0010": "+",
    "0011": "-",
    "0100": ".",
    "0101": ",",
    "0110": "[",
    "0111": "]",
}


def load_image_data(img_file, strict=True):
    try:
        img = Image.open(img_file)
    except FileNotFoundError as e:
        if strict:
            raise e
        return []
    img = img.resize((COLUMNS, ROWS))
    img_data = list(img.getdata())
    return img_data


def get_instruction(binary_str):
    return INSTRUCTIONS.get(binary_str, "")


def get_ascii(binary_str):
    if binary_str:
        return chr(int(binary_str, 2))
    return ""


def get_segment_binary(segment, segment_length, img_data):
    segment_start = segment * segment_length
    segment_end = segment * segment_length + segment_length
    return "".join(map(get_pixel_binary, img_data[segment_start:segment_end]))


def get_pixel_binary(pixel):
    binary = "0"
    try:
        if pixel[0] < 128:
            binary = "1"
    except TypeError:
        if pixel < 128:
            binary = "1"
    return binary


def execute(src_code, input_stream=""):
    output = bfi.interpret(
        src_code, input_data=input_stream, buffer_output=True)
    return output


def parse_image_list(image_list, **kwargs):
    img_list_str = ""
    if not image_list:
        return img_list_str
    for img in image_list:
        img_data = load_image_data(img)
        img_list_str += parse_image_data(img_data, **kwargs)
    return img_list_str


def parse_image_data(img_data, segment_length=INSTRUCTION_SEGMENT_BITS, encoder=get_instruction):
    parsed_str = ""
    num_segments = int(len(img_data) / segment_length)
    for segment in range(num_segments):
        segment_binary = get_segment_binary(segment, segment_length, img_data)
        parsed_str += encoder(segment_binary)
    return parsed_str


def run(src, inp=None):
    src_code = parse_image_list(src, encoder=get_instruction)
    input_stream = parse_image_list(inp, segment_length=INPUT_SEGMENT_BITS, encoder=get_ascii)
    return execute(src_code, input_stream)
