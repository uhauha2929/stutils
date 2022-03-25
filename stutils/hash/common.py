

def additive_hash(key: str, prime: int):
    hash = 0
    for c in key:
        hash += ord(c)
    return hash % prime


def multiply_hash(key: str, prime: int = 33):
    hash = 0
    for c in key:
        hash = hash * prime + ord(c)
    return hash
