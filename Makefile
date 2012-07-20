CC=gcc
CFLAGS=-I$(HOME)/local/python2.7.1/include/python2.7 -L$(HOME)/local/python2.7.1/lib/ -lpython2.7
LD_LIBRARY_PATH=$HOME/local/python2.7.1/include/python2.7

%.c:%.pyx
	cython --embed -o $@ $<

%.c:%.py
	cython --embed -o $@ $<

%:%.c
	 gcc $(CFLAGS) -o $@ $<