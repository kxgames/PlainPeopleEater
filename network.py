import pipe
import random
import settings

class Event(object):
    """ Base class that represents a generic event. """

    def __init__(self, protocol):
        self.sender = protocol.me
        self.receiver = protocol.you

class EatPerson(Event):
    """ Announces that the eater caught their lunch.  This doesn't necessarily
    kill the lunch, but it does damage it.  This message should be sent by the
    eater's client. """

    def __init__(self, protocol):
        Event.__init__(self, protocol)
        self.damage = 0

class GameOver(Event):
    """ Announces that the game is over and that the current eater won.  This
    message should get sent by the winning client. """
    pass

class FlipRoles(Event):
    """ Announces that both clients should simultaneously switch roles.  This
    message is sent by the lunch client, and it doesn't matter how it was
    triggered. """
    pass

class Setup(object):
    """ Assigns an identity number and a role to the client.  This message is
    sent by the host client. """

    def __init__(self, protocol):
        self.me = protocol.me
        self.you = protocol.you
        self.become_eater = not protocol.world.is_eater()

class Refresh(object):

    # Make sure to overwrite the pickling methods of the token classes.  This
    # message pickles player and button instances, but it only cares about the
    # position and the velocity.

    def __init__(self, world):
        self.player = world.get_me()
        self.button = world.get_button()

class Network:

    def __init__(self, world, host, port):
        self.world = world
        self.address = host, port

        self.me = 0
        self.you = 0

        self.express = pipe.Datagram(host, port)
        self.reliable = pipe.Stream(host, port)

        self.elapsed = 0
        self.callbacks = {
                "incoming" : {},
                "outgoing" : {} }

    def host(self):
        self.reliable.host()
        self.express.host()

        self.me = 1
        self.you = 2

        behaviors = True, False

        become_eater = random.choice(behaviors)
        if become_eater: self.world.become_eater()

        setup = Setup(self)
        self.reliable.send(setup)

    def connect(self):
        self.reliable.connect()
        self.express.connect()

        setup = None
        while not setup:
            setup = self.reliable.receive()

        self.me = setup.you
        self.you = setup.me

        if setup.become_eater:
            self.world.become_eater()

    def callback(self, flavor, incoming, outgoing):
        try:
            self.callbacks["incoming"][flavor].append(incoming)
            self.callbacks["outgoing"][flavor].append(incoming)

        except KeyError:
            self.callbacks["incoming"][flavor] = incoming
            self.callbacks["outgoing"][flavor] = incoming

    def update(self, time):
        self.elapsed += time

        if self.elapsed > settings.refresh_timeout:
            world = self.world
            message = Refresh(world)

            self.express.send(message)

        for message in self.express.receive():
            player = message.player
            button = message.button

            self.world.refresh(player, button)

        for message in self.reliable.receive():
            self.execute("incoming", message)

    def execute(self, event, message):
        flavor = type(message)
        callbacks = self.callbacks[event].get(flavor, [])

        if message.sender == self.me:
            message.sender = self.world.me
            messade.receiver = self.world.you

        elif message.sender == self.you:
            message.sender = self.world.you
            message.sender = self.world.me

        else:
            raise AssertionError

        for callback in callbacks:
            callback(message.sender, message.receiver, message)

    def eat_person(self):
        message = EatPerson(self)

        self.execute("outgoing", message)
        self.reliable.send(message)

    def game_over(self):
        message = GameOver(self)

        self.execute("outgoing", message)
        self.reliable.send(message)

    def flip_roles(self):
        message = FlipRoles(self)

        self.execute("outgoing", message)
        self.reliable.send(message)

class Dummy:
    """ A dummy network implementation that simply parrots back any messages it
    receives.  This might be useful for testing and debugging purposes. """

    def __init__(self, world, host, port):
        self.world = world
        self.address = host, port

        self.me = 0
        self.you = 0

        self.messages = []
        self.callbacks = {}

    def host(self):
        pass

    def connect(self):
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
