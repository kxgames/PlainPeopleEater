from __future__ import division

import pipe
import random
import settings

# Message Types {{{1
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

class FlipRoles(Event):
    """ Announces that both clients should simultaneously switch roles.  This
    message is sent by the lunch client, and it doesn't matter how it was
    triggered. """
    pass

class GameOver(Event):
    """ Announces that the game is over and that the current eater won.  This
    message should get sent by the winning client. """
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
# }}}1

class Protocol:
    """ Sends and receives the messages that keep the two clients in sync.  All
    in game network communication is implemented by this protocol. """

    # Setup {{{1
    def __init__(self, game, host, port):
        self.game = game
        self.address = host, port

        self.me = 0
        self.you = 0

        self.express = pipe.Datagram(host, port)
        self.reliable = pipe.Stream(host, port)

        self.elapsed = 0
        self.callbacks = {
                "incoming" : {},
                "outgoing" : {} }

    def setup(self):
        self.world = self.game.get_world()

    # Incoming {{{1
    def callback(self, flavor, incoming, outgoing):
        try:
            self.callbacks["incoming"][flavor].append(incoming)
            self.callbacks["outgoing"][flavor].append(incoming)

        except KeyError:
            self.callbacks["incoming"][flavor] = [incoming]
            self.callbacks["outgoing"][flavor] = [outgoing]

    def update(self, time):
        self.elapsed += time

        if self.elapsed > settings.refresh_rate:
            message = Refresh(self.world)
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
            message.sender = self.world.get_me()
            message.receiver = self.world.get_you()

        elif message.sender == self.you:
            message.sender = self.world.get_you()
            message.receiver = self.world.get_me()

        else:
            raise AssertionError

        for callback in callbacks:
            callback(message.sender, message.receiver, message)

    # Outgoing {{{1
    def eat_person(self):
        message = EatPerson(self)

        self.execute("outgoing", message)
        self.reliable.send(message)

    def flip_roles(self):
        message = FlipRoles(self)

        self.execute("outgoing", message)
        self.reliable.send(message)

    def game_over(self):
        message = GameOver(self)

        self.execute("outgoing", message)
        self.reliable.send(message)

    # }}}1

class Host(Protocol):
    """ A version of the network protocol that accepts connections on a known
    part.  During the game, this protocol is no different from the peer's. """

    # Setup {{{1
    def setup(self):
        Protocol.setup(self)

        self.me = 1
        self.you = 2

        behaviors = True, False

        become_eater = random.choice(behaviors)
        if become_eater: self.world.become_eater()

        # The host() methods of the reliable and express pipe objects are both
        # blocking, and this causes some timing problems.  One way to work
        # around those problems is to establish the express connection after
        # the reliable connection has been created and set up.
        self.reliable.host()

        setup = Setup(self)
        self.reliable.send(setup)

        self.express.host()
    # }}}1

class Client(Protocol):
    """ A version of the network protocol that connects to a known port.
    During the game, this protocol is no different from the host's. """

    # Setup {{{1
    def setup(self):
        Protocol.setup(self)

        # Connect to the reliable pipe first.
        self.reliable.connect()

        incoming = []
        while not incoming:
            incoming = self.reliable.receive()

        setup = incoming.pop()
        assert not incoming

        self.me = setup.you
        self.you = setup.me

        if setup.become_eater:
            self.world.become_eater()

        # Don't connect to the express pipe until after a setup message has
        # been received over the reliable pipe.  This prevents a strange race
        # condition.
        self.express.connect()

    # }}}1

class Dummy:
    """ A dummy network implementation that simply parrots back any messages it
    receives.  This might be useful for testing and debugging purposes. """

    # Setup {{{1
    def __init__(self, game, host="", port=0):
        self.game = game
        self.address = host, port

        self.me = 0
        self.you = 0

        self.messages = []

        self.incoming = {}
        self.outgoing = {}

    def setup(self):
        self.world = self.game.get_world()

    def teardown(self):
        pass

    # Incoming {{{1
    def callback(self, flavor, incoming, outgoing):
        try:
            self.incoming[flavor].append(incoming)
            self.outgoing[flavor].append(outgoing)

        except KeyError:
            self.incoming[flavor] = [incoming]
            self.outgoing[flavor] = [outgoing]

    def update(self, time):
        for message in self.messages:
            flavor = type(message)
            identity = self.world.get_me()

            incoming = self.incoming.get(flavor, [])
            outgoing = self.outgoing.get(flavor, [])

            message.sender = identity
            message.receiver = identity

            for callback in incoming + outgoing:
                callback(message.sender, message.receiver, message)

        message = Refresh(self.world)
        self.messages = [message]

    # Outgoing {{{1
    def eat_person(self):
        message = EatPerson(self)
        self.messages.append(message)

    def game_over(self):
        message = GameOver(self)
        self.messages.append(message)

    def flip_roles(self):
        message = FlipRoles(self)
        self.messages.append(message)
    # }}}1
