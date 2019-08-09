# coding=utf-8
"""
Raspberry Pi SenseHAT Knight Raider

This module contains LED demo which replicates the functionality of Front scanner of KITT car, which is known form 80's
TV series called 'Knight Raider'

Copyright 2019 Marcin Filip Wiśniowski
Licensed under MIT License
"""

from sense_hat import SenseHat
from time import sleep


class KnightRaider(object):
    """
    Object that handles SenseHAT framebuffer LED screen and manages a displaying effect
    """

    SENSOR_COLOR = (255, 0, 0)

    def __init__(self, line=0):
        self._sensehat = SenseHat()
        self.line = line
        self._step = 1

    def run_scanner(self):
        """ Main routine for LED scanner"""
        x = 0
        while True:
            if x in range(0, 8):
                sleep(0.05)
                self._sensehat.clear()
                self._sensehat.set_pixel(x, self.line, self.SENSOR_COLOR)
            else:
                sleep(0.1)
                self._step = -self._step
            x = x + self._step


if __name__ == '__main__':
    kitt = KnightRaider()
    kitt.run_scanner()
