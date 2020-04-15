import random
import time
import sympy
import random


def jacobi(a, n):
    if n <= 0:
        raise ValueError("n must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("n must be odd.")
    b = a % n
    c = n
    s = 1
    while b != 0:
        while b % 2 == 0:
            b /= 2
            if c % 8 in (3, 5):
                s = -s
        b, c = c, b
        if b % 4 == 3 and c % 4 == 3:
            s = -s
        b %= c
    if c == 1:
        return s
    else:
        return 0


def main():
    count1, count0 = 0, 0

    # seed = int(input("Give me a seed: "))
    N = sympy.nextprime(16383)
    sequence = ''
    begin_time = time.time()

    for i in range(100):
        seed = random.randint(pow(2, 512), pow(2, 512))
        for i in range(N):
            bit = jacobi(seed + i, N)
            if bit == -1:
                bit = 0
            if bit == 1:
                count1 += 1
            else:
                count0 += 1
            sequence += str(bit)
        print('seed = ', seed)
        print('N = ', N)
        print('#0 = ', count0)
        print('#1 = ', count1)
        print(sequence)

    end_time = time.time()
    print('Runtime: ', end_time - begin_time)


main()
