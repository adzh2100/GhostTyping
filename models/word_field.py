from lib.constants import COLOR_ACTIVE, COLOR_INACTIVE, INITIAL_GHOST_SIZE
from models.input_field import InputField
import pygame

class WordField(InputField):
    _ghost_size = INITIAL_GHOST_SIZE
    
    def __init__(self, x, y, text):
        box_height = 35
        box_width = len(text) * 25

        InputField.__init__(self, x, y, box_width, box_height, text)

        ghost = pygame.image.load("assets/images/ghost.png")
        self._ghost = pygame.transform.smoothscale(ghost, self._ghost_size)
        self._original_ghost = ghost

        self._color_inactive = pygame.Color(COLOR_INACTIVE)
        self._color_active = pygame.Color(COLOR_ACTIVE)
        self._color = self._color_inactive
        self._active = False
        self._original_text = text

    def set_text(self, new_text):
        InputField.set_text(self, new_text)
        self._active = True
        self._color = self._color_active

    def get_original_text(self):
        return self._original_text

    def get_ghost(self):
        return self._ghost
    
    def get_ghost_size(self):
        return self._ghost_size

    def is_active(self):
        return self._active    

    def enlarge_ghost(self):
        width, height = self._ghost_size
        width = width + 1
        height = width + 1
        self._ghost_size = width, height
        self._ghost = pygame.transform.smoothscale(self._original_ghost, self._ghost_size)

        self._box.x = self._box.x + 0.5
        self._box.y = self._box.y + 1
        