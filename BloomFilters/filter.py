import math
import pandas as pd
import numpy as np

class BloomFilter:

    # n => Total amount of elements that are expected to be in the filter
    # p => Probability of false positive occurrence
    # m => Length of the bitarray of the filter
    # k => total hash functions

    # Note : p and size arguments are mutually exclusive.

    def __init__(self, n, p, k = None, m = None):
        self.n = n
        self.p = p
        self.collisions = 0

        self.is_k = k
        self.is_m = m
        # Calculating m and k
        # self.m = self.__calculate_m(self.n, self.p)
        # self.k = self.__calculate_k(self.n, self.p)

        # Creating a bitarray of size m
        self.bitarray = [False] * self.m

    @property
    def m(self):
        if self.is_m:
            return self.is_m
        return self.__calculate_m(self.n, self.p)
    
    @property
    def k(self):
        if self.is_k:
            return self.is_k
        return self.__calculate_k(self.n, self.p)

    @staticmethod
    def _hash(key, seed):
        key = bytearray(key.encode())

        def fmix(h):
            h ^= h >> 16
            h  = ( h * 0x85ebca6b ) & 0xFFFFFFFF
            h ^= h >> 13
            h  = ( h * 0xc2b2ae35 ) & 0xFFFFFFFF
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
                 key[block_start + 1] << 8  | \
                 key[block_start + 0]
            
            k1 = (c1 * k1) & 0xFFFFFFFF
            k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
            k1 = (c2 * k1) & 0xFFFFFFFF
            h1 ^= k1
            h1  = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF
            h1  = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF
        
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
            k1  = ( k1 * c1 ) & 0xFFFFFFFF
            k1  = ( k1 << 15 | k1 >> 17 ) & 0xFFFFFFFF # inlined ROTL32
            k1  = ( k1 * c2 ) & 0xFFFFFFFF
            h1 ^= k1

        unsigned_val = fmix(h1 ^ length)
        if unsigned_val & 0x80000000 == 0:
            return unsigned_val
        else:
            return -((unsigned_val ^ 0xFFFFFFFF) + 1)

    @staticmethod
    def __calculate_m(n, p):
        return int(-(n * math.log(p)) // (math.log(2) ** 2))

    @staticmethod
    def __calculate_k(n, p):
        m = BloomFilter.__calculate_m(n, p)
        return int((m / n) * math.log(2))

    def add(self, item):
        if not self.search(item):
            for _ in range(self.k):
                digest = self._hash(item, _) % self.m
                self.bitarray[digest] = True
            return True
        else:
            self.collisions += 1
            return False

    def search(self, item):
        for _ in range(self.k):
            digest = self._hash(item, _) % self.m
            if not self.bitarray[digest]:
                return False
        return True

    def __len__(self):
        return sum(self.bitarray)

    def collisionCount(self):
        return self.collisions

    def __repr__(self):
        return f"n = {self.n}\np = {self.p}\nm = {self.m}\nk = {self.k}\n{[i for i, j in enumerate(self.bitarray) if j]}"

# data = open("facebook-firstnames.txt")
# lines = []
# for i in range(1000):
#     lines.append(data.readline())

# bf = BloomFilter(100, 0.01)

#Adding names to the bloom filter from 'facebook-firstnames.txt'
n = int(50e3)
data = []
readFile = open('../Data/dataset.txt', 'r')
names = list(map(lambda x: x.replace('\n', ''), readFile.readlines()))[:n]
print(len(names))
first_collision = []
for k in range(4, 32, 4):
    for p in list(np.arange(1e-04, 1, 0.01)):
        bf = BloomFilter(n, p, k, 32 * n)
        no_collision = True
        for i, data in enumerate(names):
            if not bf.add(data):
                no_collision = False
                print("k = ", k, "p = ", p, " While adding : ", data, " @ position : ", i)
                first_collision.append(str(i))
                break
        
        if no_collision:
            print("p = ", p, " No Collision")

    with open('../Data/first_collision_k' + str(k), 'w') as f:
        f.write("\n".join(first_collision))
    first_collision.clear()