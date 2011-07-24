from __future__ import division

import settings
import network

from tokens import *
from collisions import *

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

    def get_message(self):
        return self.message
    # }}}1

    # Setup and Update {{{1
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
                flavor=network.FlipRoles,
                incoming=self.handle_flip_roles,
                outgoing=self.handle_flip_roles)

        self.network.callback(
                flavor=network.GameOver,
                incoming=self.handle_game_over,
                outgoing=self.handle_game_over)

    def update (self, time):
        for token in self:
            token.update(time)

        if self.is_person():
            person = self.get_me().get_circle()
            button = self.get_button().get_circle()

            # Switch roles if the person has reached the button.
            if Collisions.circles_touching(person, button):
                self.flip_roles()

    # Methods {{{1
    def teardown(self):
        for token in self:
            token.teardown()

    def refresh (self, you, button):
        # The two arguments are technically token objects, but they came over
        # the network and were never fully set up.  They only have circle and
        # velocity attributes.  

        self.you.refresh(you)
        self.button.refresh(button)

    def handle_eat_player(self, eater, person, message):
        if eater is self.me:
            self.you.lose_health(1)
            you = self.you.get_health()

            if self.you.get_health() <= 0:
                self.game_over()

        elif eater is self.you:
            self.me.lose_health(1)
            me = self.me.get_health()

        else:
            raise AssertionError

    def handle_flip_roles(self, eater, person, message):
        if eater is self.me:
            self.become_eater()
        elif eater is self.you:
            self.become_person()
            self.move_button()

            self.button.elapsed = 0

        else: raise AssertionError


    def handle_game_over(self, winner, loser, message):
        self.playing = False
        self.message = "You win!" if winner is self.me else "You lose!"
        print self.message

    def eat_player(self):
        self.network.eat_person()

    def become_eater(self):
        self.behavior = True

    def become_person(self):
        self.behavior = False

    def place_token(self):
        return self.map.place_token()

    def game_over(self):
        self.network.game_over()

    def flip_roles(self):
        self.network.flip_roles()

    def move_button(self):
        position = self.place_token()
        self.button.set_position(position)
    # }}}1

