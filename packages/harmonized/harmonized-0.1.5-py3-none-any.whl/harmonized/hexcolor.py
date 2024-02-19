#!/usr/bin/env python3

"""
HexColor class helps on working with colors in RGB space.
Especially converting from RGB to HSV.
It aims to be working with floats [0.0 - 1.0] in general
as proposed by harmonized.

Copyright by SuperUdo3000, February 2024
Version = 0.1   (harmonized-type-1)
"""

import colorsys
import logging

import re

logging.basicConfig(
    format='[{levelname:7s}] {asctime} {message}',
    style='{',
    # datefmt='d%d %H:%M',
    datefmt='-',
    level=logging.INFO
)


class HexColor:
    """
        :param value: provide HexString like "#FF0000" for red
        :returns:
        :raises:

        Full Example:
        hc = HexColor('#FF0000') -> Full Red

        HexColor class helps on working with colors in RGB space.
        Especially converting from RGB to HSV.
        It aims to be working with floats [0.0 - 1.0] in general
        as proposed by harmonized.

    """

    def __init__(self, value='#000000', throwing=False):

        # ensure its a string with capital letter
        hex_string = str(value).upper()
        hex_string = hex_string.replace('#', '')

        p = re.compile('[0-9a-fA-F]{6}')
        is_hex = not p.match(hex_string) is None

        if not is_hex:
            logging.warning(f'`{hex_string} is not valid. Using #000000')
            r = b = g = 0
            if throwing:
                raise ValueError
        elif len(hex_string) < 6:
            logging.warning(
                f'hex_string too short {len(hex_string)} from {hex_string}'
            )
            # dbg.w(f'... will use black #000000 as fallback')
            r = g = b = 0
            if throwing:
                raise ValueError
        else:
            r = int(hex_string[0:2], 16)
            g = int(hex_string[2:4], 16)
            b = int(hex_string[4:6], 16)
        self.r = r / 255
        self.g = g / 255
        self.b = b / 255
        self.update()

    def update(self):
        hsv_raw = colorsys.rgb_to_hsv(self.r, self.g, self.b)
        self.h = hsv_raw[0]
        self.s = hsv_raw[1]
        self.v = hsv_raw[2]

    def __str__(self):
        res = f'#{int(self.r * 255):02X}' + \
              f'{int(self.g * 255):02X}' + \
              f'{int(self.b * 255):02X}'
        return res

    def nf(value):
        """ normed float: between 0.0 and 1.0 """
        res = float(value)
        if res > 1.0:
            return 1.0
        if res < 0.0:
            return 0.0
        return res

    def set_from_rgb(self, r=None, g=None, b=None):
        if r is not None:
            self.r = HexColor.nf(r)
        if g is not None:
            self.g = HexColor.nf(g)
        if b is not None:
            self.b = HexColor.nf(b)
        self.update()

    def set_from_hsv(self, h=None, s=None, v=None):
        if h is not None:
            h = HexColor.nf(h)
        if s is not None:
            s = HexColor.nf(s)
        if v is not None:
            v = HexColor.nf(v)

        res = colorsys.hsv_to_rgb(h, s, v * 255)
        self.r = res[0] / 255
        self.g = res[1] / 255
        self.b = res[2] / 255
        self.update()

    def debug(self, print_it=True):
        info = f'{self} rgb=({self.r}, {self.g}, {self.b})' + \
               f' AND hsv=({self.h}, {self.s}, {self.v})'
        if print_it:
            logging.info(info)
        return info


class HexColorTest:

    def __init__(self):
        self.hex_check('#FFFFFF')
        self.hex_check('#000000')
        self.hex_check('#FF0000')
        self.hex_check('#7F0000')
        self.hex_check('#0000FF')
        self.hex_check('00ff00', '#00FF00')
        self.hex_check('otto', '#000000')

        self.hex_check('')
        self.hex_check('FF0000', '#FF0000')
        self.hex_check('#FF0000')
        self.hex_check('#FG0000')

        self.hex_check('#FF0')
        self.hex_check(None)
        self.hex_check(12)
        self.hex_check(None)
        h = HexColor()
        h.set_from_rgb(0, 1, 0)
        logging.debug(h.debug())

        h = HexColor()
        h.set_from_hsv(1 / 3, 1, 1)
        logging.debug(h.debug())

        h = HexColor()
        h.set_from_hsv(0.2, 1, 1)
        logging.debug(h.debug())

        h = HexColor()
        h.set_from_hsv(0, 1, 1)
        logging.debug(h.debug())

    def hex_check(self, value=None, expectation=None):

        try:
            h = HexColor(value)
            logging.debug(f'{value} --> {h.debug()}')
            if expectation is None:
                if not value == str(h):
                    logging.warning(f'hex_check E01: {value} != {h}')
            else:
                if not str(h) == expectation:
                    logging.warning(f'hex_check E02: {h} != {expectation}')
        except ValueError:
            h = '#000000'


if __name__ == '__main__':
    logging.info("If running standalone a test will be executed:")
    HexColorTest()
