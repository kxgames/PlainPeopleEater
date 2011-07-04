from __future__ import division

import settings

from tokens import *

class World:
    def __init__ (self):
        self.map = None
        self.me = None 
        self.you = None 
        self.button = None 
        self.behavior = False

        self.playing = True

    def setup (self):
        self.map = settings.map
        self.me = settings.me
        self.you = settings.you
        self.button = None

        self.me.setup(self)
        self.you.setup(self)
        #self.button.setup(self)

    def update (self, time):
        self.me.update(time)
        self.you.update(time)
        #self.button.update(time)

    def refresh (self, you, button):
        self.you = you
        self.button = button

    def handle_bite (self, eater, person, message=None):
        if eater == self.me:
            print 'You win!'
        else:
            print 'You lose!'
        
    def bite (self):
        #let network know somehow....
        self.handle_bite(self.me, self.you)

    def become_eater (self):
        self.behavior = True

    def is_eater (self):
        return self.behavior

    def is_person (self):
        return not self.behavior

    def get_me (self):
        return self.me
    
    def get_you (self):
        return self.you

    def get_button (self):
        return self.button

    def get_map (self):
        return self.map
    
    def is_playing (self):
        return self.playing

