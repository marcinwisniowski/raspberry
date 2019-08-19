# coding=utf-8
"""
Raspberry Pi SenseHAT Snake Game

This is a simple clone of classic snake game that is implemented on Raspberry Pi Sense HAT.
It uses 8x8 pixels LED frame buffer as a game board and tiny joystick for steering the snake.

Copyright 2019 Marcin Filip Wiśniowski
Licensed under MIT License
"""

from sense_hat import SenseHat, InputEvent, ACTION_HELD, ACTION_PRESSED, ACTION_RELEASED, DIRECTION_MIDDLE
from random import randint
from enum import Enum
from collections import deque
from time import sleep


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

    def __eq__(self, other):
        """ Override the default Equals behavior """
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        """ Override the default Unequal behavior """
        return self.x != other.x or self.y != other.y

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

    @property
    def value(self) -> tuple:
        """
        Coordinates in tuple representation
        :return: tuple
        """
        return self._position


class PositionError(ValueError):
    """
    PositionError
    Describes situation where
    """
    def __init__(self):
        message = "Position need to be defined as (x, y) or x, y"
        super().__init__(message)


class Direction(Enum):
    """
    Defines direction on Sense HAT
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class SnakeGame(object):
    """
    Implementation of snake game logic
    """
    def __init__(self):
        self._sensehat = SenseHat()
        self._sensehat.stick.direction_any = self.joystick_listener
        self.__held_time = 0.0
        self.__score = 0
        self._sensehat.show_message("Snake", 0.1, (0, 128, 0))
        self.new()
        self.draw()

    def __del__(self):
        self._sensehat.clear()

    def new(self):
        """
        Resets the environment
        """
        self._sensehat.show_message(">===", 0.05, (0, 64, 0))
        sleep(0.5)
        self.__score = 0
        self.__new_snake()
        self.__new_apple()

    def draw(self):
        """
        Draws the board
        """
        self._sensehat.clear()
        self._draw_snake()
        self._draw_apple()

    def joystick_listener(self, event: InputEvent):
        """
        Listens for Sense Hat joystick events as a main user input source
        :param event:
        """
        if event.direction != DIRECTION_MIDDLE and event.action == ACTION_PRESSED:
            try:
                self._snake.move(Direction[event.direction.upper()])
            except ValueError:
                self.__game_over()
            else:
                if self._snake.eat(self._apple):
                    self.__score = self.__score + 1
                    self.__new_apple()

        elif event.direction == DIRECTION_MIDDLE and event.action == ACTION_HELD:
            if self.__held_time == 0.0:
                self.__held_time = event.timestamp
        elif event.direction == DIRECTION_MIDDLE and event.action == ACTION_RELEASED:
            if event.timestamp - self.__held_time >= 2.0 and self.__held_time > 0.0:
                self.__held_time = 0.0
                self.new()
        try:
            self.draw()
        except ValueError:
            self.__game_over()

    def __game_over(self):
        self._sensehat.clear()
        self._sensehat.show_message("GAME OVER")
        self._sensehat.show_message("Score: %d" % self.__score)
        sleep(1.5)
        self.new()

    def __new_snake(self):
        """
        Setups snake at initial state
        """
        self._snake = self.Snake(Direction.RIGHT, Position(4, 4), Position(3, 4), Position(2, 4))

    def __new_apple(self):
        """
        Setups apple at random position
        """
        apple_position = Position(randint(0, 7), randint(0, 7))
        while apple_position in self._snake.body:
            apple_position = Position(randint(0, 7), randint(0, 7))

        self._apple = self.Apple(apple_position)

    def _draw_snake(self):
        """
        Draws snake on a display
        """
        if self._snake is not None:
            for pixel in self._snake.body:
                self._sensehat.set_pixel(pixel.x, pixel.y, self._snake.color)

    def _draw_apple(self):
        """
        Draws apple on a display
        """
        if self._apple is not None:
            self._sensehat.set_pixel(self._apple.position.x, self._apple.position.y, self._apple.color)

    class Snake(object):
        """
        Snake object, it implements a snake behavior logic
        """
        COLOR = (0, 128, 0)  # Green

        def __init__(self, direction: Direction, *args):
            self.body: list = list(args)
            self.direction = direction
            self._head: Position = self.body[0]
            self.__trace: deque = deque(list(), 8)

        def move(self, direction: Direction):
            """
            moves the snake in a given direction
            :param direction: Direction tuple
            """
            def opposite(dir1: Direction, dir2: Direction) -> bool:
                if not isinstance(dir1, Direction) or not isinstance(dir2, Direction):
                    raise ValueError("This method can compare only directions")
                if dir1.value[0] == dir2.value[0] == 0 and dir1.value[1] == -dir2.value[1]:
                    return True
                elif dir1.value[1] == dir2.value[1] == 0 and dir1.value[0] == -dir2.value[0]:
                    return True
                else:
                    return False

            if not opposite(self.direction, direction):
                new_head = Position(self._head.x + direction.value[0], self._head.y + direction.value[1])
                if new_head not in self.body:
                    self.body.insert(0, new_head)
                    self._head = new_head
                    self.direction = direction
                    tail = self.body.pop()
                    self.__trace.append(tail)
                else:
                    raise ValueError("Snake bite itself")

        def _grow(self):
            """
            Grow the snake
            """
            if len(self.__trace) > 0:
                self.body.append(self.__trace.pop())

        def eat(self, apple):
            """

            :param apple:
            :return:
            """
            if apple.position == self._head:
                self._grow()
                return True
            return False

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
    #snake.run()
