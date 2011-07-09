#!/usr/bin/env python

from game import Game

try:
    game = Game("client")
    with game: game.play()

except KeyboardInterrupt:
    print
