# by nyLiao, 2020

import os
import random

from PIL import Image


class cryptCoder(object):
    """Object handling visual crypto encryption/decryption."""
    def __init__(self, path_dir="./", name_msg="msg.png", name_sct="sct.png",
                 name_cph="cph.png", name_out="out.png"):
        super(cryptCoder, self).__init__()
        self.path_dir = path_dir
        self.path_msg = os.path.join(self.path_dir, name_msg)
        self.path_sct = os.path.join(self.path_dir, name_sct)
        self.path_cph = os.path.join(self.path_dir, name_cph)
        self.path_out = os.path.join(self.path_dir, name_out)

    def get_msg(self, img_msg):
        """Prepare original image"""
        self.img_msg = img_msg
        self.size = img_msg.size
        return self.img_msg

    def prc_msg(self):
        img_msg = Image.open(self.path_msg)
        self.get_msg(img_msg)

    def get_sct(self):
        """Generate secret image"""
        width, height = self.size
        new_secret_image = Image.new(mode="1", size=(width * 2, height * 2))

        for x in range(0, 2 * width, 2):
            for y in range(0, 2 * height, 2):
                color = random.getrandbits(1)
                new_secret_image.putpixel((x,   y),   color)
                new_secret_image.putpixel((x+1, y),   1-color)
                new_secret_image.putpixel((x,   y+1), 1-color)
                new_secret_image.putpixel((x+1, y+1), color)

        self.img_sct = new_secret_image
        return self.img_sct

    def get_cph(self):
        """Encode ciphered image with img_msg and img_sct"""
        width, height = self.size
        ciphered_image = Image.new(mode="1", size=(width * 2, height * 2))

        for x in range(0, width*2, 2):
            for y in range(0, height*2, 2):
                secret = self.img_sct.getpixel((x, y))
                message = self.img_msg.getpixel((x/2, y/2))
                if (message > 0 and secret > 0) or (message == 0 and secret == 0):
                    color = 0
                else:
                    color = 1
                ciphered_image.putpixel((x,   y),   1-color)
                ciphered_image.putpixel((x+1, y),   color)
                ciphered_image.putpixel((x,   y+1), color)
                ciphered_image.putpixel((x+1, y+1), 1-color)

        self.img_cph = ciphered_image
        return self.img_cph

    def get_out(self, img_sct=None, img_cph=None):
        """Decode ciphered image"""
        width, height = self.size
        img_sct = img_sct if img_sct else self.img_sct
        img_cph = img_cph if img_cph else self.img_cph
        out_image = Image.new(mode="1", size=(width * 2, height * 2))

        for x in range(0, width*2):
            for y in range(0, height*2):
                out_image.putpixel((x, y), max(img_sct.getpixel((x, y)), img_cph.getpixel((x, y))))

        self.img_out = out_image
        return self.img_out
