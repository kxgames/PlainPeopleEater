import sys
import errno
import socket
import pickle

class Message:
    """ Responsible both for converting objects into strings that can be sent
    over the network and for decoding strings coming in over the network. """

    length = 4096
    delimiter = '\n\n'

    @staticmethod
    def pack(message):
        packet = pickle.dumps(message)
        packet = packet + Message.delimiter

        assert sys.getsizeof(packet) < 4096
        return packet

    @staticmethod
    def unpack(stream):
        messages = []
        packets = stream.split(Message.delimiter)

        for packet in packets:
            if not packet: continue
            
            message = pickle.loads(packet)
            messages.append(message)

        return messages

# Message Tests {{{1
if __name__ == "__main__":

    class TestMessage:

        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return self.value == other.value

    stream = ""
    messages = [
            "Hello%sWorld!" % Message.delimiter,
            TestMessage(1),
            TestMessage(2) ]

    for message in messages:
        stream += Message.pack(message)

    assert messages == Message.unpack(stream)
    print "Message: Ok!"
# }}}1

class Pipe:
    """ Base class for the socket wrapper classes.  This class provides send()
    and receive() methods using the Message translator class. """

    def __init__(self, host, port):
        self.socket = None
        self.address = host, port

    def host(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def ready(self):
        return bool(self.socket)

    def send(self, message):
        message = Message.pack(message)
        self.socket.send(message)

    def receive(self):
        try:
            stream = ""
            length = Message.length

            while True:
                stream += self.socket.recv(length)

        except socket.error, feedback:

            # This exception just means that there are no more bytes to read.
            if feedback.errno == errno.EAGAIN: pass

            # Any other type of exception is a real error.
            else: raise

        return Message.unpack(stream)

    def close(self):
        self.socket.close()

class Stream(Pipe):
    """ Wrapper for a non-blocking TCP socket. """

    def host(self):
        greeter = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = self.address

        greeter.bind(address)
        greeter.listen(5)

        self.socket, ignore = greeter.accept()
        self.socket.setblocking(False)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)
        self.socket.setblocking(False)

class Datagram(Pipe):
    """ Wrapper for a non-blocking UDP socket.  This wrapper enforces a connect
    protocol that mimics the one used by TCP. """

    def host(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)

        data, remote = self.socket.recvfrom(Message.length)

        self.socket.connect(remote)
        self.socket.setblocking(False)

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect(self.address)

        self.socket.send('')
        self.socket.setblocking(False)

# Socket Tests {{{1
if __name__ == "__main__":

    import time
    import threading

    address = 'localhost', 12345

    streams = Stream(*address), Stream(*address)
    datagrams = Datagram(*address), Datagram(*address)

    for server, client in (streams, datagrams):
        hosting = threading.Thread(target=server.host)
        connecting = threading.Thread(target=client.connect)

        hosting.start(); time.sleep(0.5); connecting.start()
        hosting.join(1); connecting.join(1)

        assert client.ready
        assert server.ready

        request = "Hello world!"
        response = "Goodbye world!"

        # These calls should not block or complain at all.
        client.receive()
        server.receive()

        client.send(request)
        assert request == server.receive()[0]

        server.send(response)
        assert response == client.receive()[0]

        client.close()
        server.close()

    print "Pipe: Ok!"

# }}}1
