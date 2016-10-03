import logging

from pygame import Rect, Surface, display
from pygame.sprite import DirtySprite

from dungeonpet.conf import GAME_UNIT_PIXELS as SCALAR


class Pet(DirtySprite):

    def __init__(self, *groups):

        # State Values
        self.hunger = 255000
        self.happiness = 255000
        self.cleanliness = 255000

        self.metabolism = 2
        self.filth = 10
        self.moodiness = 1

        # Sprite Initialization
        super().__init__(*groups)
        self.rect = Rect(0, 0, SCALAR, SCALAR)
        self.rect.center = display.get_surface().get_rect().center
        self.image = Surface([SCALAR, SCALAR])
        self.image.fill(self.color)

    def update(self, delta):
        

        # if self.hunger > 0:
        #     self.hunger -= self.metabolism * delta
        # elif self.hunger < 0:
        #     self.hunger = 0
        # if self.happiness > 0:
        #     self.happiness -= self.moodiness * delta
        # elif self.happiness < 0:
        #     self.happiness = 0
        # if self.cleanliness > 0:
        #     self.cleanliness -= self.filth * delta
        # elif self.cleanliness < 0:
        #     self.cleanliness = 0
        self.image.fill(self.color)
        self.dirty = 1

    @property
    def color(self):
        red = int(self.cleanliness / 1000)
        green = int(self.hunger / 1000)
        blue = int(self.happiness / 1000)
        return red, green, blue
