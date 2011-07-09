#!/usr/bin/env python

import settings

import pygame
from pygame.locals import *

from gui import Gui
from world import World
from network import Network

class Game:

    def __init__(self):
        self.world = World(self)
        self.gui = Gui(self)
        self.network = Host(self, host, port)

    def __init__(self):
        return [self.world, self.gui, self.network]

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

        while world.is_playing():
            time = clock.tick(frequency) / 1000
            for system in self:
                system.update(time)

    def teardown(self):
        for system in self:
            system.teardown()

if __name__ == "__main__":

    try:
        game = Game()

        game.setup()
        game.play()
        game.teardown()

    except KeyboardInterrupt:
        print
