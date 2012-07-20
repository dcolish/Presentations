from threading import Thread, enumerate as t_enum
from time import sleep

from zmq import Context, Poller, POLLIN, PUSH, PULL


class HomeBase(Thread):

    def __init__(self):
        super(HomeBase, self).__init__(name="HomeBase")
        self.context = Context()
        self.pull = self.context.socket(PULL)
        self.pull.bind("tcp://*:7001")
        self._shutdown = False
        self.poller = Poller()
        self.poller.register(self.pull, POLLIN)

    def cleanup(self):
        self.pull.close()
        self.context.term()

    def run(self):
        while True:
            socks = dict(self.poller.poll(timeout=1))
            if socks.get(self.pull) == POLLIN:
                msg = self.pull.recv()
                msg += ", WORK RECEIVED "
                print msg
            if self._shutdown:
                break
        self.cleanup()

th = HomeBase()
th.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        th._shutdown = True
        th.join()
        break
print "Exiting..."
