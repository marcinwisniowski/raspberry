# coding=utf-8
"""
Raspberry Pi SenseHAT Snake Game

This is a simple clone of classic snake game that is implemented on Raspberry Pi Sense HAT.
It uses 8x8 pixels LED frame buffer as a game board and tiny joystick for steering the snake.

Copyright 2019 Marcin Filip Wiśniowski
Licensed under MIT License
"""

from sense_hat import SenseHat
from random import randint


class Position(object):
    """
    2D Position object
    """
    def __init__(self, *args):
        """
        Initialize position object using 2D coordinates
        :param args: Position described as pair x and y of coordinates, or tuple (x, y)
        """
        if len(args) == 1:
            position = args[0]
            if len(position) != 2:
                raise PositionError
            self._position = args
        elif len(args) == 2:
            self._position = args
        else:
            raise PositionError

    @property
    def x(self):
        """
        X coordinate
        :return: x
        """
        return self._position[0]

    @property
    def y(self):
        """
        Y coordinate
        :return: y
        """
        return self._position[1]


class PositionError(ValueError):
    """
    PositionError
    Describes situation where
    """
    def __init__(self):
        message = "Position need to be defined as (x, y) or x, y"
        super().__init__(message)


class SnakeGame(object):
    """
    Implementation of snake game logic
    """
    def __init__(self):
        self._sensehat = SenseHat()
        self.__new_snake()
        self.__new_apple()

    def __new_snake(self):
        """
        Setups snake at initial state
        """
        self._snake = self.Snake(Position(4, 2), Position(4, 3), Position(4, 4))

    def __new_apple(self):
        """
        Setups apple at random position
        """
        self._apple = self.Apple(Position(randint(0, 7), randint(0, 7)))

    def run(self):
        """

        """
        self.draw_snake()
        self.draw_apple()

    def draw_snake(self):
        """
        Draws snake on a display
        """
        for pixel in self._snake.body:
            self._sensehat.set_pixel(pixel.x, pixel.y, self._snake.color)

    def draw_apple(self):
        """
        Draws apple on a display
        """
        self._sensehat.set_pixel(self._apple.position.x, self._apple.position.y, self._apple.color)

    class Snake(object):
        """
        Snake object, it implements a snake behavior logic
        """
        COLOR = (0, 128, 0)  # Green

        def __init__(self, *args):
            self._alive = True
            self.body = args

        @property
        def color(self):
            """
            Snakes color in RGB scale
            :return: tuple
            """
            return self.COLOR

    class Apple(object):
        """
        Apple
        Defines where apple need to be shown
        """
        COLOR = (128, 0, 0)  # Red

        def __init__(self, position):
            if not isinstance(position, Position):
                raise ValueError
            self._position = position

        @property
        def position(self):
            return self._position

        @property
        def color(self):
            return self.COLOR


if __name__ == '__main__':
    snake = SnakeGame()
    snake.run()
