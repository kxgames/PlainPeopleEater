from __future__ import division

import settings

from tokens import *

class World:

    def __init__ (self, game):
        self.game = game

        self.me = None 
        self.you = None 

        self.map = None
        self.button = None 

        self.behavior = False
        self.playing = True

    def __iter__(self):
        #tokens = self.me, self.you, self.button, self.map
        tokens = self.me, self.you, self.map
        return iter(tokens)

    def setup (self):
        self.me = settings.me
        self.you = settings.you

        self.map = settings.map
        self.button = None

        for token in self:
            token.setup(self)
    
    def teardown(self):
        for token in self:
            token.teardown()

    def update (self, time):
        for token in self:
            token.update(time)

    def refresh (self, you, button):
        # The two arguments are technically token objects, but they are really
        # degenerate since they came over the network and were never properly
        # set up.  In fact, they only have position and velocity attributes.
        # (Well, I haven't actually implemented this yet, but I will.) 
        #
        # Also, I think it would be a good idea to give the token objects a
        # refresh() method that takes care of updating the existing objects.

        self.you.refresh(you)
        self.button.refresh(button)

    def handle_eat_player(self, eater, person, message=None):
        # Do hp and stuff
        self.handle_game_over(eater, person, message)

    def handle_game_over(self, winner, loser, message=None):
        print "You win!" if winner is self.me else "You lose!"
        self.playing = False

    def eat_player(self):
        #network = self.hub.get_network()
        self.handle_eat_player(self.me, self.you)

    def become_eater (self):
        self.behavior = True

    def is_eater (self):
        return self.behavior

    def is_person (self):
        return not self.behavior

    def is_playing (self):
        return self.playing

    def get_me (self):
        return self.me
    
    def get_you (self):
        return self.you

    def get_button (self):
        return self.button

    def get_map (self):
        return self.map
