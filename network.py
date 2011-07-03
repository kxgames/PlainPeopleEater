import socket
import pickle

class EatPerson:
    """ Announces that the eater caught their lunch.  This doesn't necessarily
    kill the lunch, but it does damage it.  This message should be sent by the
    eater's client. """

    def __init__(self, protocol):
        self.target = protocol.you
        self.damage = 0

class GameOver:
    """ Announces that the game is over and that the current eater won.  This
    message should get sent by the winning client. """

    def __init__(self, protocol):
        self.winner = protocol.me

class FlipRoles:
    """ Announces that both clients should simultaneously switch roles.  This
    message is sent by the lunch client, and it doesn't matter how it was
    triggered. """

    def __init__(self, protocol):
        self.eater = protocol.me
        self.lunch = protocol.you

class Update:

    # Make sure the overwrite the pickling methods of the token classes.  This
    # message pickles player and button instances, but it only cares about the
    # position and the velocity.

    def __init__(self, world):
        self.player = world.get_me()
        self.button = world.get_button()

class Network:
    pass

class Dummy:
    """ A dummy network implementation that simply parrots back any messages it
    receives.  This might be usefull for testing and debugging purposes. """

    def __init__(self, world, host, port):
        self.world = world
        self.address = host, port

        self.me = 0
        self.you = 0

        self.messages = []
        self.callbacks = {}

    def setup(self):
        pass

    def callback(self, flavor, function):
        try:
            self.callbacks[flavor].append(function)
        except KeyError:
            self.callbacks[flavor] = [function]

    def update(self, time):
        for message in self.messages:

            flavor = type(message)
            callbacks = self.callbacks.get(flavor, [])

            for callback in callbacks:
                callback(message)

        message = Update(self.world)
        self.messages = [message]

    def eat_person(self):
        message = EatPerson(self)
        self.messages.append(message)

    def game_over(self):
        message = GameOver(self)
        self.messages.append(message)

    def flip_roles(self):
        message = FlipRoles(self)
        self.messages.append(message)
