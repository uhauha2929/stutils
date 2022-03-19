import random

class Reservoir(object):

    def __init__(self, size):
        self.size = size
        self.i = 0
        self.sample = []
    
    def feed(self, item):
        self.i += 1
        # 第i个元素(i <= k)，直接放入池子
        if len(self.sample) < self.size: 
            self.sample.append(item)
        else:
            # 第i个元素(i>k)，以k/i的概率替换放入池中
            rand_int = random.randint(1, self.i)
            if rand_int <= self.size:
                self.sample[rand_int - 1] = item
            