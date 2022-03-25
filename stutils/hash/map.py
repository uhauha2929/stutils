import math
import numpy as np

from .common import multiply_hash


class BloomFilter(object):

    def __init__(self, n, p: float = 1e-5):
        """布隆过滤器

        :param n: 存储的元素个数
        :param p: 错误率 默认1e-5
        """
        self.m = int(math.ceil(- (n * math.log(p)) / (math.log(2) ** 2)))
        self.k = int(math.ceil(math.log(2) * self.m / n))
        self.p = (1 - math.exp(-n * self.k / self.m)) ** self.k
        # python的int类型位数动态没有上限，这里按照C的int类型位数，否则Numpy运算可能会报类型错误
        self.array = np.zeros(int(self.m + 31 - 1) // 31, np.int32)
        self.max_size = 2 ** 31 - 1


    def has_bit(self, value: int) -> bool:
        element_idx = value // 31
        byte_idx = value % 31
        return (self.array[element_idx] & (1 << byte_idx)) != 0


    def set_bit(self, value: int) -> bool:
        element_idx = value // 31
        byte_idx = value % 31
        element = self.array[element_idx]
        # 如果该位为0
        if not element & (1 << byte_idx):
            self.array[element_idx] = element | (1 << byte_idx)
            return True
        return False


    def put(self, key: str) -> bool:
        # 这里暂时使用简单的乘法求哈希，其他库使用的是murmur3的高位和低位8字节
        hash1 = multiply_hash(key, 31)
        hash2 = multiply_hash(key, 33)

        bits_changed = False
        combined_hash = hash1

        for _ in range(self.k):
            bits_changed |= self.set_bit((combined_hash & self.max_size) % self.m)
            combined_hash += hash2

        return bits_changed

    def contains(self, key: str) -> bool:
        hash1 = multiply_hash(key, 31)
        hash2 = multiply_hash(key, 33)

        bits_changed = True
        combined_hash = hash1

        for _ in range(self.k):
            bits_changed &= self.has_bit((combined_hash & self.max_size) % self.m)
            combined_hash += hash2

        return bits_changed
