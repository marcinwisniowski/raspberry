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
    AMBIENT_COLOR = (64, 0, 0)

    def __init__(self, line=0):
        self._sensehat = SenseHat()
        self.line = line
        self._step = 1

    def run_scanner(self):
        """ Main routine for LED scanner """
        position = 0
        while True:
            if position in range(0, 8):
                self.set_ambient()
                self._sensehat.set_pixel(position, self.line, self.SENSOR_COLOR)
            else:
                sleep(0.1)
                self._step = -self._step
            sleep(0.05)
            position = position + self._step

    def set_ambient(self):
        """ Manages the background of sensor """
        self._sensehat.clear()
        for x in range(0, 8):
            self._sensehat.set_pixel(x, self.line, self.SENSOR_COLOR)


if __name__ == '__main__':
    kitt = KnightRaider()
    kitt.run_scanner()
