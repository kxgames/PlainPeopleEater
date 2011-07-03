import random

from vector import *
from collisions import *
from shapes import *
from flocking import *

class Player:

    def __init__(self, address):
        self.address = address
        self.points = 0

    def score(self, points):
        self.points += points

    def get_points(self):
        return self.points

class Map:
    """ Stores information about the game world.  This currently includes the size
    of the map, the number of players in the game, the cumulative point value
    of all the quaffles, and the amount of friction on the map. """
    # Map {{{1
    def __init__(self, size, players, points, friction):
        self.size = size
        self.friction = friction

        self.points = points
        self.players = players

    def setup(self, world):
        self.world = world

    def update(self, time):
        pass

    def place_sight(self):
        return self.size.center

    def place_target(self):
        x = random.random() * self.size.width
        y = random.random() * self.size.height
        return Vector(x, y)

    def get_size(self):
        return self.size

    def get_friction(self):
        return self.friction

    def get_points(self):
        return self.points

    def get_players(self):
        return self.players
    # }}}1


class Player(Sprite):
    """ Represents a player.  The motion of these objects is primarily
    controlled by the player, but they will bounce off of walls. """
    # Player {{{1
    def __init__(self, name, mass, force, size):
        Sprite.__init__(self)

        self.name = name

        self.mass = mass
        self.force = force
        self.direction = Vector.null()

        self.size = size

    def get_size(self):
        return self.size

    def setup(self, world):
        self.world = world

        position = world.get_map().place_sight()
        Sprite.setup(self, position, self.size, self.force, 0.0)

    def update(self, time):
        map = self.world.get_map()

        # Set the acceleration.
        force = self.force * self.direction
        friction = -self.mass * self.velocity   # This is actually drag.

        self.acceleration = force + friction
        Sprite.update(self, time)

        # Bounce the sight off the walls.
        boundary = self.world.get_map().get_size()
        Sprite.bounce(self, time, boundary)

    def accelerate(self, direction):
        self.direction = direction

    def shoot(self):
        touching = Collisions.circles_touching

        for target in self.world.targets:
            if touching(self.circle, target.circle):
                target.injure(self)
    # }}}1

