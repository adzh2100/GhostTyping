import pygame
from lib.constants import COLOR_BLACK


class InputField:
    def __init__(self, x_coord, y_coord, width, height, text):
        pygame.init()

        self._box = pygame.Rect(x_coord, y_coord, width, height)
        self._coordinates = x_coord, y_coord
        self._color = pygame.Color(COLOR_BLACK)
        self._text = text

    def get_text(self):
        return self._text

    def set_text(self, new_text):
        self._text = new_text

    def set_coordinates(self, x_coord, y_coord):
        self._coordinates = x_coord, y_coord

    def get_coordinates(self):
        return self._coordinates

    def get_color(self):
        return self._color

    def get_box(self):
        return self._box
