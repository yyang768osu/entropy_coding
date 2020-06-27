import numpy as np

N = 4  # size of alphabet
K = 90  # number of symbols
r = 8

# randomly initialize K symbols,
# each represented as integer from 0 to N-1
symbols = np.random.randint(N, size=K)
symbols = list(symbols)
# randomly initialize a pmf array with length N
while True:
    p = np.random.rand(N)
    p = p / sum(p)
    p = (p * 2 ** r).astype(int)
    p[0] += 2 ** r - sum(p)
    if all(p != 0):
        print(p)
        break

d = np.cumsum(p)
c = np.insert(d[:-1], 0, 0)

p = [int(x) for x in p]
c = [int(x) for x in c]


def ans_encoder(symbols, p, c, r):
    """ ANS encoder (no rescaling)

    Parameters
    ----------
    symbols : list of int
        list of input symbols represented by index
        value should not be larger than len(p)
    p : list of int
        quantized pmf of all input alphabet, sum(p) == 2 ** r
    c : list of int
        quantized cdf of all input alphabet, len(c) = len(p)
        c[0] = 0, and c[-1] = sum(p[:-1])
    r : int
        bit-width precision of the quantized pmf
        sum(p) == 2 ** r

    Warnings
    --------
    int type for all the input arguments should be python int type,
    which does not overflow (yes, search it)

    Returns
    -------
    s : integer representation of the encoded message

    """
    s = 0
    for x in symbols:
        if s < c[1]:
            s += 1
        s = 2 ** r * (s // p[x]) + \
            s % p[x] + c[x]
    return s


def ans_decoder(s, p, c, r):
    """ ANS encoder (no rescaling)

    Parameters
    ----------
    s : int
        integer representation of the encoded message
    p : list of int
        quantized pmf of all input alphabet, sum(p) == 2 ** r
    c : list of int
        quantized cdf of all input alphabet, len(c) = len(p)
        c[0] = 0, and c[-1] = sum(p[:-1])
    r : int
        bit-width precision of the quantized pmf
        sum(p) == 2 ** r

    Warnings
    --------
    int type for all the input arguments should be python int type,
    which does not overflow (yes, search it)

    Returns
    -------
    decoded_symbols : list of int
        list of decoded symbols

    """
    def h(s):
        s = s % 2 ** r
        # this loop can be improved by binary search
        for a in reversed(range(len(c))):
            if s >= c[a]:
                return a
    decoded_symbols = []
    while s:
        x = h(s)
        decoded_symbols.append(x)
        s = p[x] * (s // 2 ** r) + \
            s % (2 ** r) - c[x]
        if s < c[1]:
            s -= 1
    return list(reversed(decoded_symbols))

s = ans_encoder(symbols, p, c, r)
print(s)
decoded_symbols = ans_decoder(s, p, c, r)

print(decoded_symbols)
print(symbols)

assert all(x == y for x, y in zip(decoded_symbols, symbols))

## Test code
import random
import math

# initialize data distribution and input length
p = [20, 50, 80, 106]
c = [0, 20, 70, 150]
r = 8
sequence_length = 100

# randomly sample input
random.seed(1)
symbols = random.choices(range(len(p)), weights=p, k=sequence_length)

# encode
s = ans_encoder(symbols, p, c, r)

# decode
decoded_symbols = ans_decoder(s, p, c, r)

# statistics
average_bps = math.log2(s)/sequence_length
entropy = sum(-i/2**r * math.log2(i/2**r) for i in p)

# sanity check
assert all(x == y for x, y in zip(decoded_symbols, symbols))

# display results
print(f"encoded integer        : {s}")
print(f"average bits per symbol: {average_bps:.5f} bits/symbol")
print(f"data source entropy    : {entropy:.5f} bits/symbol")

