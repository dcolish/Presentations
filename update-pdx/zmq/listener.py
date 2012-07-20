from time import sleep
from threading import Thread

from zmq import (
    Context,
    NOBLOCK,
    Poller,
    POLLIN,
    SUB,
    SUBSCRIBE,
    )

class KillThread(Exception):
    """Raised when we want threads to die"""


class Listener(Thread):
    def __init__(self):
        super(Listener, self).__init__(name="Listener")

        self._shutdown = False
        self.context = Context()
        self.sub = self.context.socket(SUB)
        self.sub.bind('tcp://*:7000')
        self.sub.setsockopt(SUBSCRIBE, "")

        self.poller = Poller()
        self.poller.register(self.sub, POLLIN)

    def cleanup(self):
        self.sub.close()
        self.context.term()

    def run(self):
        while True:
            socks = dict(self.poller.poll(timeout=1))
            if socks.get(self.sub) == POLLIN:
                msg = self.sub.recv(flags=NOBLOCK)
                print msg
            if self._shutdown:
                break
        self.cleanup()

listener = Listener()
listener.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        listener._shutdown = True
        listener.join()
        break
print "Exiting..."
