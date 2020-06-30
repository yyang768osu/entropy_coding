def ans_encoder(symbols, p, c, r, r_s, r_t):
    """ ANS encoder

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
    r_s : int
        bit-width precision of encoded integer s
    r_t : int
        bit-width precision of integers in stack t_stack

    Returns
    -------
    s : int
        s < 2 ** r_s
    t_stack : list of int
        each int < 2 ** r_t

    """
    s = 0
    t_stack = []
    for x in symbols:
        if s < c[1]:
            s += 1
        while s >= (2 ** (r_s - r) + 1) * p[x]:
            t = s % (2 ** r_t)
            s >>= r_t
            t_stack.append(t)
        s = 2 ** r * (s // p[x]) + \
            s % p[x] + c[x]
    return s, t_stack


def ans_decoder(s, t_stack, p, c, r, r_s, r_t):
    """ ANS encoder

    Parameters
    ----------
    s : int
        (s, t_stack) together represent the encoded message; s < 2 ** r_s
    t_stack : list of int
        (s, t_stack) together represent the encoded message; t < 2 ** r_t
    p : list of int
        quantized pmf of all input alphabet, sum(p) == 2 ** r
    c : list of int
        quantized cdf of all input alphabet, len(c) = len(p)
        c[0] = 0, and c[-1] = sum(p[:-1])
    r : int
        bit-width precision of the quantized pmf
        sum(p) == 2 ** r
    r_s : int
        bit-width precision of encoded integer s
    r_t : int
        bit-width precision of integers in stack t_stack

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
        while s < 2 ** (r_s - r_t) and len(t_stack):
            t = t_stack.pop()
            s = (s << r_t) + t
    return list(reversed(decoded_symbols))


## Test code
import random
import math

# initialize data distribution and input length
p = [20, 50, 80, 106]
c = [0, 20, 70, 150]
r = 8
r_s = 32
r_t = 16
sequence_length = 1000000

# randomly sample input
random.seed(1)
symbols = random.choices(range(len(p)), weights=p, k=sequence_length)

# encode
s, t_stack = ans_encoder(symbols, p, c, r, r_s, r_t)

# decode
decoded_symbols = ans_decoder(s, t_stack[:], p, c, r, r_s, r_t)

# statistics
average_bps = (r_s + len(t_stack) * r_t) / sequence_length
entropy = sum(-i / 2 ** r * math.log2(i / 2 ** r) for i in p)

# sanity check
assert all(x == y for x, y in zip(decoded_symbols, symbols))

# display results
print(f"average bits per symbol: {average_bps:.5f} bits/symbol")
print(f"data source entropy    : {entropy:.5f} bits/symbol")
