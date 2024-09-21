import numpy as np
N_LOOP = 1_000_000

def while_loop(n=N_LOOP):
    s = 0
    i = 0
    while i < n:
        s += i
        i += 1
    return s

def for_loop(n=N_LOOP):
    s = 0
    for i in range(n):
        s += i
    return s

def sum_range(n=N_LOOP):
    return sum(range(n))

def sum_numpy(n=N_LOOP):
    return np.sum(np.arange(n))

def test_while_loop(benchmark):
    benchmark(while_loop)

def test_for_loop(benchmark):
    benchmark(for_loop)

def test_sum_range(benchmark):
    benchmark(sum_range)

def test_sum_numpy(benchmark):
    benchmark(sum_numpy)