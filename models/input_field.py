from lib.constants import COLOR_BLACK
import pygame

class InputField:
    def __init__(self, x, y, width, height, text):
        pygame.init()

        self._box = pygame.Rect(x, y, width, height)
        self._coordinates = x, y
        self._color = pygame.Color(COLOR_BLACK)
        self._text = text

    def get_text(self):
        return self._text

    def set_text(self, new_text):
        self._text = new_text

    def set_coordinates(self, x, y):
        self._coordinates = x, y
            
    def get_coordinates(self):
        return self._coordinates
      
    def get_color(self):
        return self._color

    def get_box(self):
        return self._box