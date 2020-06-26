import numpy as np

N = 4  # size of alphabet
K = 10  # number of symbols

# randomly initialize K symbols,
# each represented as integer from 0 to N-1
symbols = np.random.randint(N, size=K)
# randomly initialize a pmf array with length N
pmf = np.random.rand(N)
pmf = pmf / sum(pmf)
# initialize output bit-array
bits = []

d = np.cumsum(pmf)
c = np.insert(d[:-1], 0, 0)

# Encoding
a = 0.
b = 1.
s = 0
for symbol in symbols:
    width = b - a
    a, b = a + width * c[symbol], a + width * d[symbol]
    while b <= 1 / 2 or a >= 1 / 2:
        if b <= 1 / 2:  # case 0
            bits.append(0)
            bits += [1] * s
            s = 0
            a *= 2
            b *= 2
        else:  # case 1
            bits.append(1)
            bits += [0] * s
            s = 0
            a = 2 * (a - 1 / 2)
            b = 2 * (b - 1 / 2)
    # a < 1/2 and b > 1/2
    while a > 1 / 4 and b < 3 / 4:
        s += 1
        a = 2 * (a - 1 / 4)
        b = 2 * (b - 1 / 4)
s += 1
# a <= 1/4 or b >= 3/4
if a <= 1 / 4:  # case 2a
    bits.append(0)
    bits += [1] * s
else:  # case 2b
    bits.append(1)
    bits += [0] * s

print(list(symbols))
print(bits)


# Decoding
def decode_one_symbol(z_0, z_1, a, b, c, d):
    """

    Parameters
    ----------
    z_0: lower end of the current binary block
    z_1: higher end of the current binary block
    a: lower end of the current sub-interval
    b: higher end of the current sub-interval
    c: CDF starts with a 0.0
    d: CDF that ends with 1.0

    Returns
    -------
    if [z_0, z_1] is not contained in any of the symbols inside [a, b]:
        return None
    else:
        return the decoded index

    """
    for index, (low, high) in enumerate(zip(c, d)):
        low = a + (b - a) * low
        high = a + (b - a) * high
        if low <= z_0 and z_1 <= high:
            return index
    return None


decoded_symbols = []
z = 0.0
a = 0.0
b = 1.0
for bit_index, bit in enumerate(bits):
    binary_block_size = 2 ** (-bit_index - 1)
    if bit == 1:
        z += binary_block_size
    symbol = decode_one_symbol(z, z + binary_block_size, a, b, c, d)
    while symbol is not None:
        decoded_symbols.append(symbol)
        a, b = a + (b - a) * c[symbol], a + (b - a) * d[symbol]
        symbol = decode_one_symbol(z, z + binary_block_size, a, b, c, d)

print(decoded_symbols)
