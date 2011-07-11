import pygame
from pygame.locals import *

class Joystick:
    """ Control the game using a joystick.  This is the preferred mode of user
    input; the mouse-pad controller is really just meant to emulate this. """

    def __init__(self, gui):
        """ Set up some basic class attributes.  Not too much can be done in
        the constructor, since it is called from the settings scripts. """

        self.gui = gui

        self.x = self.y = 0
        self.joystick = None

        self.handlers = {
                QUIT : self.quit_event
                JOYAXISMOTION : self.motion_event
                JOYBUTTONDOWN: self.button_event }

        self.callbacks = {
                "motion" : lambda *ignore: pass,
                "button" : lambda *ignore: pass }

    def setup(self):
        """ Connect to the joystick and prepare to begin accepting input.  If
        no joystick is found, the game will exit with an error message. """

        pygame.joystick.init()

        if not pygame.joystick.get_count():
            print "No joystick found."
            print "Consider using the mouse-pad controller."
            sys.exit()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def update(self, event):
        """ Check to see if any joystick events have occurred since the last
        update cycle.  If so, perform any necessary processing and execute the
        appropriate callback. """

        for event in pygame.event.get():
            self.handlers[event.type](event)

    def on_button(self, callback):
        """ Register a callback for a button event. """
        self.callbacks["button"] = callback

    def on_motion(self, callback):
        """ Register a callback for a motion event. """
        self.callbacks["motion"] = callback

    def quit_event(self, event):
        """ This is an internal handler for any quit events.  This works by
        simply instructing the world to send a game over message. """
        world = self.gui.get_world()
        world.game_over()

    def motion_event(self, event):
        """ This is an internal handler to joystick motion events.  Only motion
        along the x and y coordinates is acted upon. """

        X, Y, Z = 0, 1, 2

        if event.axis in (X, Y):
            if event.axis == X: self.x = event.value
            if event.axis == Y: self.y = event.value

            direction = vector.Vector (self.x, self.y)
            self.callbacks["motion"](direction)

        elif event.axis == Z:
            pass

        else:
            raise AssertionError

    def button_event(self, event):
        """ This is an internal handler for joystick button events.  No
        processing is done; the callback is just executed immediately. """
        self.callbacks["button"]()

class MousePad:
    """ Control the game using the keyboard.  For optimal gameplay, this
    controller should not be used.  It is instead supposed to be a joystick
    replacement for debugging purposes. """

    def __init__(self):
        pass

    def setup(self):
        pass

    def update(self, event):
        pass

    def on_button(self, callback):
        pass

    def on_motion(self, callback):
        pass

