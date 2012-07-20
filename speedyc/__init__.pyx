import cython

cpdef long crunit(int var):
    cdef long ll = 0
    cdef int x
    for x from 0 <= x < var by 1:
        ll += x**2
    return ll

