#!/usr/bin/env python

from game import Game

try:
    game = Game(host=False)

    game.setup()
    game.play()
    game.teardown()

except KeyboardInterrupt:
    print
