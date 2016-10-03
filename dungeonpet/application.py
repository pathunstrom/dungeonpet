import logging

import pygame

from dungeonpet import conf
from dungeonpet.scenes import Game


class Application(object):
    def __init__(self):
        self.current_scene = None

    def run(self):
        logging.basicConfig(level=conf.LOG_LEVEL)
        pygame.init()
        pygame.display.set_mode((conf.GAME_WIDTH * conf.GAME_UNIT_PIXELS,
                                 conf.GAME_HEIGHT * conf.GAME_UNIT_PIXELS))
        self.current_scene = Game()
        while self.current_scene:
            self.current_scene = self.current_scene.run()
        pygame.quit()
