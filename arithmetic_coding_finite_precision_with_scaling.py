import numpy as np

N = 4  # size of alphabet
K = 90  # number of symbols
range_precision = 16
pmf_precision = 8
range_half = 2 ** (range_precision - 1)
range_quarter = 2 ** (range_precision - 2)

# randomly initialize K symbols,
# each represented as integer from 0 to N-1
symbols = np.random.randint(N, size=K)
# randomly initialize a pmf array with length N
while True:
    pmf = np.random.rand(N)
    pmf = pmf / sum(pmf)
    pmf = (pmf * 2 ** pmf_precision).astype(int)
    pmf[0] += 2 ** pmf_precision - sum(pmf)
    if all(pmf != 0):
        print(pmf)
        break

# initialize output bit-array
bits = []

d = np.cumsum(pmf)
c = np.insert(d[:-1], 0, 0)

d = [int(i) for i in d]
c = [int(i) for i in c]

# Encoding
a = 0.
b = 2 ** range_precision
s = 0
for symbol in symbols:
    width = b - a
    a, b = a + width * c[symbol] // 2 ** pmf_precision, a + width * d[symbol] // 2 ** pmf_precision
    while b <= range_half or a >= range_half:
        if b <= range_half:  # case 0
            bits.append(0)
            bits += [1] * s
            s = 0
            a *= 2
            b *= 2
        else:  # case 1
            bits.append(1)
            bits += [0] * s
            s = 0
            a = 2 * (a - range_half)
            b = 2 * (b - range_half)
    # a < 1/2 and b > 1/2
    while a > range_quarter and b < 3 * range_quarter:
        s += 1
        a = 2 * (a - range_quarter)
        b = 2 * (b - range_quarter)
s += 1
# a <= 1/4 or b >= 3/4
if a < range_quarter:  # case 2a
    bits.append(0)
    bits += [1] * s
else:  # case 2b
    bits.append(1)
    bits += [0] * s

print(bits)

z = 0
for i in range(range_precision):
    z = (z << 1)
    if i < len(bits):
        z += bits[i]
next_bit_index = min(len(bits), range_precision)
z_gap = 1 << max(0, range_precision - len(bits))

decoded_symbols = []
a = 0
b = 2 ** range_precision
while True:
    for index, (low, high) in enumerate(zip(c, d)):
        low = a + (b - a) * low // 2 ** pmf_precision
        high = a + (b - a) * high // 2 ** pmf_precision
        if low <= z and high >= z + z_gap:
            a = low
            b = high
            decoded_symbols.append(index)
            break
    else:
        break
    while b <= range_half or a >= range_half:
        if b <= range_half:
            b = 2 * b
            a = 2 * a
            z = 2 * z
            if next_bit_index < len(bits):
                z += bits[next_bit_index]
                next_bit_index += 1
            else:
                z_gap <<= 1
        else:
            b = 2 * (b - range_half)
            a = 2 * (a - range_half)
            z = 2 * (z - range_half)
            if next_bit_index < len(bits):
                z += bits[next_bit_index]
                next_bit_index += 1
            else:
                z_gap <<= 1
    while a > range_quarter and b < 3 * range_quarter:
        a = 2 * (a - range_quarter)
        b = 2 * (b - range_quarter)
        z = 2 * (z - range_quarter)
        if next_bit_index < len(bits):
            z += bits[next_bit_index]
            next_bit_index += 1
        else:
            z_gap <<= 1

print(decoded_symbols)
print(list(symbols))

assert len(symbols) == len(decoded_symbols) and all(x == y for x, y in zip(symbols, decoded_symbols))
