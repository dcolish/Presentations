from multiprocessing import Pool


def lower(str_in):
    return reversed(str_in.lower())

if __name__ == '__main__':
    pool = Pool(processes=4)
    data = ['FOO', 'BAR', 'BAZ'] * 1000
    print pool.map(lower, data)
