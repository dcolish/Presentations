from threading import Thread, enumerate as t_enum
from time import sleep, time

from zmq import Context, Poller, NOBLOCK, POLLIN, PUSH, PULL


class DrillingWell(Thread):

    def __init__(self):
        super(DrillingWell, self).__init__(name="DrillingWell")
        self.context = Context()
        self.push = self.context.socket(PUSH)
        self.push.bind("tcp://*:7000")
        self._shutdown = False
        for th in t_enum():
            if th.name == "MainThread":
                self.mainthread = th

    def cleanup(self):
        print "Producer exiting..."
        self.push.close()
        self.context.term()

    def run(self):
        count = 0
        while True:
            if not self.mainthread.is_alive():
                self._shutdown = True
                break
            sleep(0.01)
            count += 1
            self.push.send("SOMETHING " + str(count))
            if self._shutdown:
                break
        self.cleanup()


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
        for th in t_enum():
            if th.name == "MainThread":
                self.mainthread = th

    def cleanup(self):
        print "Workers exiting..."
        self.push.close()
        self.pull.close()
        self.context.term()

    def run(self):
        while True:
            if not self.mainthread.is_alive():
                self._shutdown = True
                break
            socks = dict(self.poller.poll(timeout=1))
            if socks.get(self.pull) == POLLIN:
                msg = self.pull.recv(flags=NOBLOCK)
                msg += " WORK COMPLETE, " + str(time())
                self.push.send(msg, flags=NOBLOCK)
            if self._shutdown:
                break
        self.cleanup()


class HomeBase(Thread):

    def __init__(self):
        super(HomeBase, self).__init__(name="HomeBase")
        self.context = Context()
        self.pull = self.context.socket(PULL)
        self.pull.bind("tcp://*:7001")
        self._shutdown = False
        self.poller = Poller()
        self.poller.register(self.pull, POLLIN)
        for th in t_enum():
            if th.name == "MainThread":
                self.mainthread = th

    def cleanup(self):
        print "Home exiting..."
        self.pull.close()
        self.context.term()

    def run(self):
        while True:
            if not self.mainthread.is_alive():
                self._shutdown = True
                break
            socks = dict(self.poller.poll(timeout=1))
            if socks.get(self.pull) == POLLIN:
                msg = self.pull.recv(flags=NOBLOCK)
                msg += ", WORK RECEIVED "
                print msg
            if self._shutdown:
                break
        self.cleanup()

worker_threads = []
for _ in range(10):
    th = Leatherneck()
    th.start()
    worker_threads.append(th)

well = DrillingWell()
well.start()

home = HomeBase()
home.start()


while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        for th in worker_threads:
            th._shutdown = True
            th.join(timeout=0.1)
        well._shutdown = True
        well.join(timeout=0.1)
        home._shutdown = True
        home.join(timeout=0.1)

        break
print "Exiting..."
