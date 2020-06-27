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
    s = 0
    for x in symbols:
        if s < c[1]:
            s += 1
        s = 2 ** r * (s // p[x]) + \
            s % p[x] + c[x]
    return s

s = ans_encoder(symbols, p, c, r)
print(s)


def ans_decoder(s, p, c, r):
    def h(s):
        s = s % 2 ** r
        for a in range(N - 1, -1, -1):
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

decoded_symbols = ans_decoder(s, p, c, r)

print(decoded_symbols)
print(symbols)

assert all(x == y for x, y in zip(decoded_symbols, symbols))
