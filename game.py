from __future__ import division

import pygame, settings
from pygame.locals import *

from gui import Gui
from world import World
from network import Host, Client, Sandbox

class Game:

    def __init__(self):
        self.world = World(self)
        self.gui = Gui(self)

        # A dictionary of *class* objects.  The network system will be
        # instantiated from one of these classes.
        protocols = {
                "host" : Host,
                "client" : Client,
                "sandbox" : Sandbox }

        Protocol = protocols[settings.role]
        self.network = Protocol(self, settings.host, settings.port)

    def __iter__(self):
        yield self.world
        yield self.gui
        yield self.network

    def __enter__(self):
        for system in self:
            system.setup()

    def __exit__(self, *args):
        for system in self:
            system.teardown()

    def get_world(self):
        return self.world

    def get_gui(self):
        return self.gui

    def get_network(self):
        return self.network

    def play(self):
        clock = pygame.time.Clock()
        frequency = settings.clock_rate

        while self.world.is_playing():
            time = clock.tick(frequency) / 1000
            for system in self:
                system.update(time)

        raw_input("Press any key to exit the game.")

if __name__ == "__main__":
    try: 
        game = Game()
        with game:
            game.play()

    except KeyboardInterrupt:
        print
