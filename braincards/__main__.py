import json
import os
import sys

from .braincards import run as run_braincards

FILE_NAME = "img_files.json"
HELP_MSG = "braincards (HELP)"


def get_img_files():
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def write_img_files(img_files):
    with open(FILE_NAME, "w") as f:
        json.dump(img_files, f)


def add_img(img_type, img_file):
    if not os.path.exists(img_file):
        sys.exit("braincards: File not found: {}".format(img_file))
    try:
        img_files = get_img_files()
    except FileNotFoundError:
        img_files = {}
    try:
        img_files[img_type].append(img_file)
    except KeyError:
        img_files[img_type] = [img_file]
    write_img_files(img_files)


def clear_img(img_type=None):
    if not os.path.exists(FILE_NAME):
        return
    if not img_type:
        os.remove(FILE_NAME)
    else:
        img_files = get_img_files()
        img_files[img_type] = []
        write_img_files(img_files)


correct_command = {
    "source": "src",
    "input": "inp",
    "clear": "clr",
    "execute": "run",
    "start": "run",
}


def main():
    try:
        command = sys.argv[1].lower()
    except IndexError:
        sys.exit(HELP_MSG)
    command = correct_command.get(command, command)
    if command in ("src", "inp"):
        add_img(command, sys.argv[2])
    elif command == "clr":
        clear_img(sys.argv[2:])
    elif command == "run":
        img_files = get_img_files()
        clear_img()
        run_braincards(**img_files)
    elif command == "quick":
        src_img = sys.argv[2]
        if not os.path.exists(src_img):
            sys.exit("braincards: File not found: {}".format(src_img))
        src_img = [src_img]
        try:
            input_img = [sys.argv[3]]
        except IndexError:
            input_img = None
        img_files = {"src": src_img, "inp": input_img}
        run_braincards(**img_files)
    else:
        print("braincards: Invalid command: {}".format(command))


if __name__ == "__main__":
    main()
