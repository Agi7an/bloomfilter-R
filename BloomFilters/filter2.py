import math
import pandas as pd
import numpy as np


class BloomFilter:

    # n => Total amount of elements that are expected to be in the filter
    # p => Probability of false positive occurrence
    # m => Length of the bitarray of the filter
    # k => total hash functions

    # Note : p and size arguments are mutually exclusive.

    def __init__(self, n, m):
        self.n = n
        self.m = m

        # Creating a bitarray of size m
        self.bitarray = [False] * self.m

    @property
    def p(self):
        return self.__calculate_p(self.m, self.n)

    @property
    def k(self):
        return self.__calculate_k(self.m, self.n)

    @staticmethod
    def _hash(key, seed):
        key = bytearray(key.encode())

        def fmix(h):
            h ^= h >> 16
            h = (h * 0x85ebca6b) & 0xFFFFFFFF
            h ^= h >> 13
            h = (h * 0xc2b2ae35) & 0xFFFFFFFF
            h ^= h >> 16
            return h

        length = len(key)
        nblocks = int(length / 4)
        h1 = seed

        c1 = 0xcc9e2d51
        c2 = 0x1b873593

        for block_start in range(0, nblocks * 4, 4):
            k1 = key[block_start + 3] << 24 | \
                 key[block_start + 2] << 16 | \
                 key[block_start + 1] << 8 | \
                 key[block_start + 0]

            k1 = (c1 * k1) & 0xFFFFFFFF
            k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
            k1 = (c2 * k1) & 0xFFFFFFFF
            h1 ^= k1
            h1 = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF
            h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

        tail_index = nblocks * 4
        k1 = 0
        tail_size = length & 3

        if tail_size >= 3:
            k1 ^= key[tail_index + 2] << 16

        if tail_size >= 2:
            k1 ^= key[tail_index + 1] << 8

        if tail_size >= 1:
            k1 ^= key[tail_index + 0]

        if tail_size > 0:
            k1 = (k1 * c1) & 0xFFFFFFFF
            k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  # inlined ROTL32
            k1 = (k1 * c2) & 0xFFFFFFFF
            h1 ^= k1

        unsigned_val = fmix(h1 ^ length)
        if unsigned_val & 0x80000000 == 0:
            return unsigned_val
        else:
            return -((unsigned_val ^ 0xFFFFFFFF) + 1)

    @staticmethod
    def __calculate_p(m, n):
        k = BloomFilter.__calculate_k(m, n)
        return math.exp(k * math.log(1 - math.exp(-k * n / m)))

    @staticmethod
    def __calculate_k(m, n):
        return int((m / n) * math.log(2))

    def add(self, item):
        if not self.search(item):
            for _ in range(self.k):
                digest = self._hash(item, _) % self.m
                self.bitarray[digest] = True
            return True
        else:
            return False

    def search(self, item):
        for _ in range(self.k):
            digest = self._hash(item, _) % self.m
            if not self.bitarray[digest]:
                return False
        return True

    def __len__(self):
        return sum(self.bitarray)

    def __repr__(self):
        return f"n = {self.n}\np = {self.p}\nm = {self.m}\nk = {self.k}\n{[i for i, j in enumerate(self.bitarray) if j]}"


n = int(input("Enter the number of elements: "))
m = int(input("Enter the size of the bit array: "))
bf = BloomFilter(n, m)

# Adding names to the bloom filter from 'facebook-firstnames.txt'
readFile = open('../Data/facebook-firstnames.txt', 'r')
data = pd.DataFrame({"n": np.arange(1, n, 1), "p": np.arange(11, 20, 2)})

for i in range(100):
    name = readFile.readline()
    bf.add(name)
    print(name)
readFile.close()

print(bf)
