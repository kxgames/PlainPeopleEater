from __future__ import division

import sys, math

import settings
import controls

import pygame
from pygame.locals import *

from shapes import *
from vector import *

class Gui:
    # Constructor {{{1
    def __init__ (self, game):
        self.game = game

        self.controls = {
                "joystick" : controls.Joystick(self),
                "keyboard" : controls.Keyboard(self),
                "experimental" : controls.Experimental(self) }

    # Attributes {{{1
    def get_game(self):
        return self.game

    def get_world(self):
        return self.world

    #}}}1

    # Update {{{1
    def setup(self):
        pygame.init()

        # Save references to other game systems.
        self.world = self.game.get_world()
        self.map = self.world.get_map()

        # Create a window to run the game in.
        self.size = self.map.get_size().get_pygame().size
        self.screen = pygame.display.set_mode(self.size)

        self.status_font = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 50)

        # Set up the user controls.
        self.input = self.controls[settings.controller]
        self.input.setup()

        player = self.world.get_me()

        self.input.on_motion(player.accelerate)
        self.input.on_button(player.bite)

    def update(self, time):
        self.input.update()
        self.draw()

    def teardown(self):
        pass

    # Draw {{{1
    def draw(self):
        world = self.world
        screen = self.screen

        # Draw the background.
        screen.fill(settings.background_color)

        # Draw the players.
        if self.world.is_eater():
            my_color = settings.eater_color
            your_color = settings.your_color
        else:
            my_color = settings.my_color
            your_color = settings.eater_color

        me = world.get_me(), my_color
        you = world.get_you(), your_color
        
        for player, color in me, you:
            position = player.get_position().get_pygame()
            radius = player.get_radius()

            pygame.draw.circle(screen, color, position, radius)

        # Draw the button.
        button = world.get_button()

        color = settings.button_color
        position = button.get_position().get_pygame()
        radius = button.get_radius()

        if world.is_eater(): progress = 1
        else: progress = 1 - button.get_elapsed() / button.get_timeout()
        
        points = [position]

        for index in range(50):
            fraction = index / 50
            angle = 2 * math.pi * fraction

            if fraction > progress:
                break

            x = position[0] + radius * math.cos(angle)
            y = position[1] + radius * math.sin(angle)

            point = x, y
            points.append(point)

        if len(points) > 2:
            pygame.draw.polygon(screen, color, points)

        # Draw a status message.
        template = "%s: %d HP"

        me = world.get_me()
        you = world.get_you()

        my_status = template % (settings.my_name, me.get_health())
        your_status = template % (settings.your_name, you.get_health())

        map = world.get_map().get_size()
        width, height = self.status_font.size(your_status)

        my_position = 5, 5
        your_position = map.width - width - 5, 5

        my_message = self.status_font.render(my_status, True, settings.text_color)
        your_message = self.status_font.render(your_status, True, settings.text_color)

        screen.blit(my_message, my_position)
        screen.blit(your_message, your_position)

        # Finish the update.
        pygame.display.flip()

    # }}}1

