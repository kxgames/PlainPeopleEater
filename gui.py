import sys
import joystick
import settings

import pygame
from pygame.locals import *

from shapes import *
from vector import *


class Gui:
    # Constructor {{{1
    def __init__ (self, game):
        self.game = game

    def setup(self):
        self.world = self.game.get_world()
        self.map = self.world.get_map()

        pygame.init()

        self.size = self.map.get_size().get_pygame().size
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.Font(None, 20)

        if pygame.joystick.get_count() == 0:
            print "No joystick! Aborting...."
            sys.exit(0)

        # Callback dictionary for joystick event handling.
        joystick_callbacks = {
                'direction' : self.world.get_me().accelerate,
                'bite' : self.world.get_me().bite }

        self.joystick = joystick.Joystick(joystick_callbacks)
    #}}}1

    def teardown(self):
        pass

    # Update {{{1
    def update(self, time):
        self.react(time)
        self.draw(time)

    # React {{{1
    def react(self, time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.world.game_over()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            
            if event.type == pygame.JOYAXISMOTION:
                self.joystick.axis_event(event)

            if event.type == pygame.JOYBUTTONDOWN:
                self.joystick.button_event(event, True)

            if event.type == pygame.JOYBUTTONUP:
                self.joystick.button_event(event, False)

    # Draw {{{1
    def draw(self, time):
        background_color = Color("black")
        my_color = settings.my_color
        your_color = settings.your_color
        text_color = Color("green")

        screen = self.screen
        screen.fill(background_color)

        # Draw the players.
        if self.world.is_eater():
            my_color = settings.eater_color
            your_color = settings.your_color
        else:
            my_color = settings.my_color
            your_color = settings.eater_color

        me = self.world.get_me(), my_color
        you = self.world.get_you(), your_color
        
        for player, color in me, you:
            position = player.get_position().get_pygame()
            radius = player.get_radius()

            pygame.draw.circle(screen, color, position, radius)

        # Draw the button.
        button = self.world.get_button()
        color = settings.button_color
        position = button.get_position().get_pygame()
        radius = button.get_radius()

        pygame.draw.circle(screen, color, position, radius)

        # Finish the update.
        pygame.display.flip()

    # }}}1

