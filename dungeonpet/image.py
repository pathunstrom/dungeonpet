import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from dungeonpet import conf


def background():
    surface = Surface(pygame.display.get_surface().get_size())
    surface.fill(conf.BORDER_COLOR)
    border_width = conf.GAME_BORDER_WIDTH * conf.GAME_UNIT_PIXELS
    play_area_width = surface.get_width() - (border_width * 2)
    play_area_height = surface.get_height() - (border_width * 2)
    pygame.draw.rect(surface,
                     conf.BACKGROUND_COLOR,
                     Rect(border_width,
                          border_width,
                          play_area_width,
                          play_area_height
                          )
                     )
    return surface
