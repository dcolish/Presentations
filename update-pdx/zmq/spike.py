from time import sleep
from threading import Event, Thread

from zmq import (
    Context,
    HWM,
    NOBLOCK,
    Poller,
    POLLIN,
    PUB,
    PAIR,
    SUB,
    SUBSCRIBE,
    )

shutdown = Event()


class KillThread(Exception):
    """Raised when we want threads to die"""


class Heartbeat(Thread):

    def __init__(self, context, *args, **kw):
        self.context = context
        self.pub = self.context.socket(PAIR)
        self.pub.bind("inproc://#1")
        super(Heartbeat, self).__init__(*args, **kw)

    def cleanup(self):
        self.pub.send("DIE")
        self.pub.close()

    def run(self):
        try:
            x = 0
            while not shutdown.is_set():
                self.pub.send("BEAT.FOO.* %d, %s" % (x + 1, self.name))
                x += 1
                sleep(1)
        finally:
            print "%s exiting..." % self.name
            self.cleanup()


class Stethoscope(Thread):

    def __init__(self, context, *args, **kw):
        self.context = context
        self.recv = self.context.socket(PAIR)
        self.recv.connect("inproc://#1")

        self.pub = self.context.socket(PUB)
        self.pub.connect('tcp://localhost:7003')
        self.pub.setsockopt(HWM, 1000)

        self.poller = Poller()
        self.poller.register(self.recv, POLLIN)
        super(Stethoscope, self).__init__(*args, **kw)

    def cleanup(self):
        self.recv.close()
        self.pub.close()

    def run(self):
        try:
            while not shutdown.is_set():
                socks = dict(self.poller.poll())
                if socks.get(self.recv) == POLLIN:
                    msg = self.recv.recv()
                    self.pub.send(msg, flags=NOBLOCK)
                    if msg == "DIE":
                        raise KillThread
        except KillThread:
            print "%s exiting..." % self.name
        finally:
            self.cleanup()

context = Context()

heart = Heartbeat(context, name="Heartbeat Thread")
stethoscope = Stethoscope(context, name="Stethoscope Thread")


for t in (heart, stethoscope):
    t.start()

while True:
    try:
        # call thread.join to keep some control in the main thread
        while (heart.is_alive() or
               stethoscope.is_alive()):
            heart.join(timeout=0.1)
            stethoscope.join(timeout=0.1)

    except KeyboardInterrupt:
        shutdown.set()
        while (heart.is_alive() or
               stethoscope.is_alive()):
            heart.join(timeout=0.1)
            stethoscope.join(timeout=0.1)

        context.term()
        break
