from lib.constants import LIFE_SIZE
import pygame

class Life:
    def __init__(self):
        pygame.init()

        icon_active = pygame.image.load("assets/images/life.png")
        icon_inactive = pygame.image.load("assets/images/empty.png")
        
        self._icon_active = pygame.transform.smoothscale(icon_active, LIFE_SIZE)
        self._icon_inactive = pygame.transform.smoothscale(icon_inactive, LIFE_SIZE)

        self._used = False
        
    def get_icon_active(self):
        return self._icon_active
    
    def get_icon_inactive(self):
        return self._icon_inactive
    
    def is_used(self):
        return self._used
    
    def mark_as_unused(self):
        self._used = False
        
    def mark_as_used(self):
        self._used = True

