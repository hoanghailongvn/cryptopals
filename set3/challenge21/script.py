def MT19937_32(seed=5489):
    # seed: 5489 is used in reference C code
    # coefficients for MT19937 32-bit
    w, n, m, r = 32, 624, 397, 31
    a = 0x9908b0df
    u, d = 11, 0xffffffff
    s, b = 7, 0x9d2c5680
    t, c = 15, 0xefc60000
    l = 18
    f = 1812433253

    MT = [0] * n
    index = n + 1
    lower_mask = (1 << r) - 1
    upper_mask = (1 << w) - 1 - lower_mask

    def seed_mt(seed: int):
        index = n
        MT[0] = seed
        for i in range(1, n):
            MT[i] = (f * (MT[i - 1] ^ (MT[i - 1] >> (w - 2))) + i) & ((1 << w) - 1)
    
    def twist():
        for i in range(n):
            x = (MT[i] & upper_mask) + (MT[(i + 1) % n] & lower_mask)
            xA = x >> 1
            if x % 2 != 0: # lowest bit of x is 1
                xA = xA ^ a
            MT[i] = MT[(i + m) % n] ^ xA
        index = 0
    
    def extract_number():
        if index >= n:
            if index > n:
                assert "Generator was never seeded"
            twist()
        
        y = MT[index]
        y = y ^ ((y >> u) & d)
        y = y ^ ((y << s) & b)
        y = y ^ ((y << t) & c)
        y = y ^ (y >> l)

        index = index + 1

        yield y & ((1 << w) - 1)

    seed_mt(seed)
    return extract_number()


if __name__ == "__main__":
    rng = MT19937_32()
    for i in range(10):
        print(next(rng))