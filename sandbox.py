#!/usr/bin/env python

from game import Game

try:
    game = Game("sandbox")
    with game: game.play()

except KeyboardInterrupt:
    print
