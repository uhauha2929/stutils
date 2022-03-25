from decimal import Decimal
import random
from typing import Union


def split_money(total: Union[str, Decimal], n: int) -> Decimal:
    """随机将红包分成若干份"""
    min_money = Decimal('0.01')
    total = Decimal(total)
    if total < min_money * n:
        raise ValueError('Each one should be greater than 0.01.')
    remain = Decimal(total) - min_money * n
    while n > 0:
        if n == 1:
            n -= 1
            yield remain + min_money
        else:
            money = Decimal(0)
            if remain > min_money:
                max_money = remain / n * 2
                if max_money > min_money:
                    money = Decimal(random.uniform(0, 1)) * max_money
                    if money < min_money:
                        money = min_money
                else:
                    money = min_money * random.choice((0, 1))
            money = money.quantize(Decimal('0.00'))
            remain -= money
            n -= 1
            yield money + min_money
