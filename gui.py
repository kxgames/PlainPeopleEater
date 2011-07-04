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
        else:
            print 'Number of Joysticks:', pygame.joystick.get_count()

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

    def react(self, time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            
            if event.type == pygame.JOYAXISMOTION:
                self.joystick.axis_event(event)

            if event.type == pygame.JOYBUTTONDOWN:
                self.joystick.button_event(event, True)

            if event.type == pygame.JOYBUTTONUP:
                self.joystick.button_event(event, False)

    def draw(self, time):
        # Draw {{{2
        background_color = Color("black")
        my_color = settings.my_color
        your_color = settings.your_color
        text_color = Color("green")

        if self.world.is_eater():
            my_color = Color("purple")
        else:
            your_color = Color("purple")

        screen = self.screen
        screen.fill(background_color)

        # Draw the players.
        me = self.world.get_me()
        you = self.world.get_you()
        
        for player in me, you:
            position = player.get_position()
            radius = player.get_size()
            color = my_color
            if player == you:
                color = your_color

            pygame.draw.circle(screen, color, position.pygame, radius)

        # Finish the update.
        pygame.display.flip()
        # }}}2
    # }}}1

