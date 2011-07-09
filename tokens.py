import random

from vector import *
from collisions import *
from shapes import *
from flocking import *

class Map:
    # Map {{{1
    def __init__(self, size, players, friction):
        self.size = size
        self.friction = friction

        self.players = players

    def setup(self, world):
        self.world = world

    def teardown(self):
        pass

    def update(self, time):
        pass

    def place_token(self):
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

class Player (Sprite):
    # Constructor {{{1
    def __init__(self, name, mass, force, size, speed):
        Sprite.__init__(self)

        self.name = name

        self.mass = mass
        self.force = force
        self.direction = Vector.null()
        self.speed = speed

        self.size = size

        self.mode = 'Person'


    def setup(self, world):
        self.world = world

        position = world.get_map().place_token()
        Sprite.setup(self, position, self.size, self.force, self.speed)
    # }}}1

    def teardown (self):
        pass

    # Update {{{1
    def update(self, time):
        map = self.world.get_map()

        # Set the acceleration.
        force = self.force * self.direction
        #friction = -self.mass * self.velocity   # This is actually drag.

        #self.acceleration = force + friction
        self.acceleration = force
        Sprite.update(self, time)

        # Bounce the sight off the walls.
        boundary = self.world.get_map().get_size()
        Sprite.bounce(self, time, boundary)

    def accelerate(self, direction):
        self.direction = direction

    def bite(self):
        me = self.get_circle()
        you = self.world.get_you().get_circle()
        if Collisions.circles_touching (me, you):
            self.world.eat_player()
    # }}}1

    # Attributes {{{1
    def is_eater(self):
        monster = self.world.is_eater()
        player = self.world.get_me() is self

        if player and monster:
            return True
        elif not player and not monster:
            return True
        else:
            return False

    def is_person(self):
        return not self.is_eater()

    def get_size(self):
        return self.size
    # }}}1


