# coding=utf-8
"""
Raspberry Pi SenseHAT Hello World!

This module contains "Hello World" like program for Raspberry Pi Sense HAT

Copyright 2019 Marcin Filip Wiśniowski
Licensed under MIT License
"""

from sense_hat import SenseHat

hat = SenseHat()
hat.show_message("Hello World!")
