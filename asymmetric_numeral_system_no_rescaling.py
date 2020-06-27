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
    P_int = np.random.rand(N)
    P_int = P_int / sum(P_int)
    P_int = (P_int * 2 ** r).astype(int)
    P_int[0] += 2 ** r - sum(P_int)
    if all(P_int != 0):
        print(P_int)
        break

d = np.cumsum(P_int)
c = np.insert(d[:-1], 0, 0)

P_int = [int(x) for x in P_int]
c = [int(x) for x in c]

s = 0
for x in symbols:
    if s < c[1]:
        s += 1
    s = 2 ** r * (s // P_int[x]) + \
        s % P_int[x] + c[x]

print(s)

decoded_symbols = []


def h(s):
    s = s % 2 ** r
    for a in range(N - 1, -1, -1):
        if s >= c[a]:
            return a

while s:
    x = h(s)
    decoded_symbols.append(x)
    s = P_int[x] * (s // 2 ** r) + \
        s % (2 ** r) - c[x]
    if s < c[1]:
        s -= 1

print(list(reversed(decoded_symbols)))
print(symbols)

assert all(x == y for x, y in zip(reversed(decoded_symbols), symbols))
