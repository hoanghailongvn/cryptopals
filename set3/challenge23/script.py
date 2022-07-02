from math import ceil
from random import randint
from turtle import clone
from MT19937 import MT19937_32
from time import sleep, time     

def invert_rightshift_xor(y_moi: int, shift: int):
    original = 0

    for i in range(32):
        original = (y_moi >> (32 - i - 1)) ^ (original >> (shift - 1))

    return original

def invert_leftshift_and_xor(y_moi: int, shift: int, andd: int) -> int:
    original = 0

    for i in range(32):
        original = (y_moi & ((1 << (i + 1)) - 1)) ^ 
        print(f"original: {original:32b}")

def untemper(y: int):
    y = invert_rightshift_xor(y, 18)
    y = invert_leftshift_and_xor(y, 15, 0xefc60000)
    y = invert_leftshift_and_xor(y, 7, 0x9d2c5680)
    y = invert_rightshift_xor(y, 11)

    return y

def attack():
    # just for this challenge, don't use time() for seed
    seed = int(time())
    rng = MT19937_32(seed)
    recv = []
    for i in range(624):
        recv.append(rng.extract_number())

    ####################################################
    # Có recv
    # Clone rng gốc
    ####################################################
    
    states = []
    for i in range(624):
        states.append(untemper)

    clone_rng = MT19937_32()
    clone_rng.MT = states

    print(all([rng.extract_number() == clone_rng.extract_number() for _ in range(624)]))




if __name__ == "__main__":
    # attack()
    y = 0b11110100111100101111000011110000
    invert_leftshift_and_xor(y, 5, 0xab)