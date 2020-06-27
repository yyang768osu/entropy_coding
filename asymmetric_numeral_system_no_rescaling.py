import numpy as np

N = 4  # size of alphabet
K = 90  # number of symbols
pmf_precision = 8

# randomly initialize K symbols,
# each represented as integer from 0 to N-1
symbols = np.random.randint(N, size=K)
symbols = list(symbols)
# randomly initialize a pmf array with length N
while True:
    pmf = np.random.rand(N)
    pmf = pmf / sum(pmf)
    pmf = (pmf * 2 ** pmf_precision).astype(int)
    pmf[0] += 2 ** pmf_precision - sum(pmf)
    if all(pmf != 0):
        print(pmf)
        break

d = np.cumsum(pmf)
c = np.insert(d[:-1], 0, 0)

pmf = [int(x) for x in pmf]
c = [int(x) for x in c]

s = 0
for symbol in symbols:
    if s < c[1]:
        s += 1
    s = 2 ** pmf_precision * (s // pmf[symbol]) + \
        s % pmf[symbol] + c[symbol]

print(s)

decoded_symbols = []


def h(s):
    s = s % 2 ** pmf_precision
    for a in range(N - 1, -1, -1):
        if s >= c[a]:
            return symbol

while s:
    x = h(s)
    decoded_symbols.append(x)
    s = pmf[x] * (s // 2 ** pmf_precision) + \
        s % (2 ** pmf_precision) - c[x]
    if s < c[1]:
        s -= 1

print(list(reversed(decoded_symbols)))
print(symbols)

assert all(x == y for x, y in zip(reversed(decoded_symbols), symbols))
