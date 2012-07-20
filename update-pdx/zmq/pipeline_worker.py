from threading import Thread, enumerate as t_enum
from time import sleep, time

from zmq import Context, Poller, POLLIN, PUSH, PULL


class Leatherneck(Thread):

    def __init__(self):
        super(Leatherneck, self).__init__(name="Leatherneck")
        self.context = Context()
        self.pull = self.context.socket(PULL)
        self.pull.connect("tcp://localhost:7000")
        self.push = self.context.socket(PUSH)
        self.push.connect("tcp://localhost:7001")
        self.poller = Poller()
        self.poller.register(self.pull, POLLIN)
        self._shutdown = False

    def cleanup(self):
        self.push.close()
        self.pull.close()
        self.context.term()

    def run(self):
        while True:
            socks = dict(self.poller.poll(timeout=1))
            if socks.get(self.pull) == POLLIN:
                msg = self.pull.recv()
                msg += " WORK COMPLETE, " + str(time())
                self.push.send(msg)
            if self._shutdown:
                break
        self.cleanup()

threads = []
for _ in range(10):
    th = Leatherneck()
    th.start()
    threads.append(th)

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        for th in threads:
            th._shutdown = True
            th.join()
        break
print "Exiting..."
