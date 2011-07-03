from __future__ import division

import settings

from tokens import *

class World:
    def __init__ (self):
        self.me = Player()
        self.you = Player()

    def setup (self):
        pass

    def update (self, time):
        self.me.update()
        self.you.update()

    def get_me (self):
        return self.me
    
    def get_you (self):
        return self.you

