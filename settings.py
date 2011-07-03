import arguments

import pygame
from pygame.locals import *

from tokens import *
from shapes import *

host = arguments.option("host", default='localhost')
port = arguments.option("port", default=0, cast=int) + 11249

size = Rectangle.from_size(500, 500)
map = Map(size=size, players=2, friction=50)

me = Player("Me", mass=0.85, force=200, size=10)
you = Player("You", mass=0.85, force=200, size=10)

my_color = Color("green")
you_color = Color("yellow")

