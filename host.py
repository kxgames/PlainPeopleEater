#!/usr/bin/env python

from game import Game

try:
    game = Game(host=True)

    game.setup()
    game.play()
    game.teardown()

except KeyboardInterrupt:
    print
