#!/usr/bin/env python

from game import Game

try:
    game = Game("host")
    with game: game.play()

except KeyboardInterrupt:
    print
