from __future__ import division

import pygame, settings
from pygame.locals import *

from gui import Gui
from world import World
from network import Host, Client

class Game:

    def __init__(self, host=False):
        self.world = World(self)
        self.gui = Gui(self)
        self.network = Host(self) if host else Client(self)

    def __iter__(self):
        yield self.world
        yield self.gui
        yield self.network

    def get_world(self):
        return self.world

    def get_gui(self):
        return self.gui

    def get_network(self):
        return self.network

    def setup(self):
        for system in self:
            system.setup()

    def play(self):
        clock = pygame.time.Clock()
        frequency = settings.clock_rate

        while self.world.is_playing():
            time = clock.tick(frequency) / 1000
            for system in self:
                system.update(time)

    def teardown(self):
        for system in self:
            system.teardown()

