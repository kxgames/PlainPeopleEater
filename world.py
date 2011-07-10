from __future__ import division

import settings
import network

from tokens import *

class World:
    # Constructor {{{1
    def __init__ (self, game):
        self.game = game

        self.me = None 
        self.you = None 

        self.map = None
        self.button = None 

        self.behavior = False
        self.playing = True

    def __iter__(self):
        tokens = self.me, self.you, self.button, self.map
        #tokens = self.me, self.you, self.map
        return iter(tokens)

    def setup (self):
        self.me = settings.me
        self.you = settings.you

        self.map = settings.map
        self.button = settings.button

        for token in self:
            token.setup(self)

        self.network = self.game.get_network()

        self.network.callback(
                flavor=network.EatPerson,
                incoming=self.handle_eat_player,
                outgoing=self.handle_eat_player)

        self.network.callback(
                flavor=network.GameOver,
                incoming=self.handle_game_over,
                outgoing=self.handle_game_over)
    # }}}1

    def update (self, time):
        for token in self:
            token.update(time)

    # Methods {{{1
    def teardown(self):
        for token in self:
            token.teardown()

    def refresh (self, you, button):
        # The two arguments are technically token objects, but they are really
        # degenerate since they came over the network and were never set up.
        # In fact, they only have circle and velocity attributes.  

        self.you.refresh(you)
        self.button.refresh(button)

    def handle_eat_player(self, eater, person, message=None):
        if eater is self.me:
            self.you.lose_health(1)
            you = self.you.get_health()
            print "You have bitten the other player! Their health: %i" % you

            if self.you.get_health() <= 0:
                self.game_over()

        elif eater is self.you:
            self.me.lose_health(1)
            me = self.me.get_health()
            print "The other player has bitten you! Your health: %i" % me

        else:
            raise AssertionError

    def handle_game_over(self, winner, loser, message=None):
        print "You win!" if winner is self.me else "You lose!"
        self.playing = False

    def eat_player(self):
        self.network.eat_person()

    def become_eater (self):
        self.behavior = True

    def place_token(self):
        return self.map.place_token()

    def game_over(self):
        self.network.game_over()

    # }}}1

    # Attributes {{{1
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
    # }}}1
