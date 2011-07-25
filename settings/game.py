from __future__ import division

import pygame
from pygame.locals import *

from tokens import *
from shapes import *

clock_rate = 40
refresh_rate = 100 / 1000

size = Rectangle.from_size(500, 500)
map = Map(size=size, players=2, friction=50)

me = Player("Me", health=10, mass=0.85, force=400, size=20, speed=150)
you = Player("You", health=10, mass=0.85, force=400, size=20, speed=150)

button = Button(size=5, timeout=10)
