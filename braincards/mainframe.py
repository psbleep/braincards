import os
import RPi.GPIO as GPIO

from io import BytesIO
from time import sleep

from PIL import Image
from picamera import PiCamera

from .braincards import run as run_braincards

PRINTER_NAME = "HP_OfficeJet_Pro_8720"
OUTPUT_FILE = "output.txt"

SRC_IMG_PIN = 12
INPUT_IMG_PIN = 14
CLEAR_IMG_PIN = 16
RUN_CODE_PIN = 18


CROP_IMG = {
    "src": (1, 1, 1, 1),
    "inp": (9, 9, 9, 9)
}


GPIO.setmode(GPIO.BCM)
GPIO.setup(RUN_CODE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(CLEAR_IMG_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SRC_IMG_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(INPUT_IMG_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


stream = BytesIO()
camera = PiCamera()


def take_img(card_type, braincard_images):
    sleep(2)
    camera.capture(stream, "jpeg")
    stream.seek(0)
    src_img = Image.open(stream)
    src_img = src_img.crop(CROP_IMG[card_type])
    braincard_images["src"].append(list(src_img.getdata()))


def main():
    braincard_images = {"src": [], "inp": []}
    while True:
        take_src_img = GPIO.input(SRC_IMG_PIN) is False
        if take_src_img:
            take_img("src", braincard_images)
        take_input_img = GPIO.input(INPUT_IMG_PIN) is False
        if take_input_img:
            take_img("inp", braincard_images)
        clear_img = GPIO.input(CLEAR_IMG_PIN) is False
        if clear_img:
            braincard_images = {"src": [], "inp": []}
        run_code = GPIO.input(RUN_CODE_PIN) is False
        if run_code:
            result = run_braincards(**braincard_images)
            print(result)
            with open(OUTPUT_FILE, "w") as f:
                f.write(result)
            os.system("lp -d {} {}".format(PRINTER_NAME, OUTPUT_FILE))
            os.remove(OUTPUT_FILE)
            braincard_images = {"src": [], "inp": []}


if __name__ == "__main__":
    main()
