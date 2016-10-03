from pygame import display, event, QUIT
from pygame.sprite import LayeredDirty
from pygame.time import Clock

from dungeonpet.sprites import Pet
from dungeonpet.image import background


class Scene(object):

    def __init__(self):
        self.running = False
        self.next_scene = None

    def handle_event(self, e):
        if e.type == QUIT:
            self.running = False


class Game(Scene):

    def __init__(self):
        super().__init__()
        self.background = background()
        self.group1 = LayeredDirty()
        self.pet = Pet(self.group1)
        self.display = display.get_surface()
        self.clock = Clock()
        self.delta = 0

    def run(self):

        self.running = True
        while self.running:
            for e in event.get():
                self.handle_event(e)
            self.group1.update(self.delta)
            display.update(self.group1.draw(self.display))
            self.display.blit(self.background, (0, 0))
            self.delta = self.clock.tick()
