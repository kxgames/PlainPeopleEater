import arguments

from tokens import *
from shapes import *

host = arguments.option("host", default='localhost')
port = arguments.option("port", default=0, cast=int) + 11249

size = Rectangle.from_size(500, 500)
map = Map(size=size, players=2, points=40, friction=50)

players = [
        Sight("Player", mass=0.85, force=200, size=10) ]

