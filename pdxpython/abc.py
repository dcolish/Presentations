from abc import ABCMeta, abstractmethod, abstractproperty


class Meh(object):
    __metaclass__ = ABCMeta

    @property
    def easy_as(self):
        return '123'

    @abstractmethod
    def baby_its(self):
        #: To be implemented
        return

    @abstractproperty
    def doh_ray_me(self):
        #: To be implemented
        return


class Mork(Meh):
    #: Not implementing say_hello

    def doh_ray_me(self):
        return "ABC"


class Neep(Meh):

    def baby_its(self):
        print self.easy_as

    @property
    def doh_ray_me(self):
        return "ABC"

# m = Mork()
# print m.easy_as

try:
    m = Mork()
    print m.easy_as
except TypeError:
    n = Neep()
    n.baby_its()
    print n.doh_ray_me
