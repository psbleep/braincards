import json
import os
import sys

from .braincards import run as run_braincards

FILE_NAME = "img_files.json"


def get_img_files():
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def write_img_files(img_files):
    with open(FILE_NAME, "w") as f:
        json.dump(img_files, f)


def add_img(img_type, img_file):
    try:
        img_files = get_img_files()
    except FileNotFoundError:
        img_files = {}
    try:
        img_files[img_type].append(img_file)
    except KeyError:
        img_files[img_type] = [img_file]
    write_img_files(img_files)


def clear_img(img_type="all"):
    if img_type == "all":
        os.remove(FILE_NAME)
    else:
        img_files = get_img_files()
        img_files[img_type] = []
        write_img_files(img_files)


correct_command = {
    "source": "src",
    "input": "inp"
}


def main():
    command = sys.argv[1].lower()
    command = correct_command.get(command, command)
    if command in ("src", "inp"):
        add_img(command, sys.argv[2])
    elif command in ("clear", "clr"):
        clear_img(sys.argv[2:])
    elif command in ("run", "execute", "start"):
        img_files = get_img_files()
        clear_img()
        run_braincards(**img_files)


if __name__ == "__main__":
    main()
