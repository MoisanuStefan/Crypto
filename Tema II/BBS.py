import random
import time

import sympy


def getPrime(x):
    p = sympy.nextprime(x)
    while p % 4 != 3:
        p = sympy.nextprime(p)
    return p


def main():


    N = sympy.nextprime(16383)
    # x = int(input("Give me a number and I will find the next prime number ( p % 4 = 3 ): "))
    # y = int(input("Give me another one, of same length please: "))
    # seed = int(input("Give me the seed: "))
    # N = int(input("How many bits would you like to generate? "))
    begin_time = time.time()

    for i in range(100):
        x = random.randint(pow(2, 512), pow(2, 513))
        y = random.randint(pow(2, 512), pow(2, 513))
        seed = random.randint(pow(2, 512), pow(2, 513))
        p = getPrime(x)
        q = getPrime(y)
        M = p * q

        print("Input: \n")
        print("p = ", p)
        print("\np = ", q)

        print("\nM = ", M)
        print("\nSeed = ", seed)
        print("\nNumber of bits to generate: ", N, '\n\nResult:\n')

        bit_sequence = ""

        for i in range(N):
            seed = seed * seed % M
            bit = seed % 2
            bit_sequence += str(bit)

        print(bit_sequence)
        print("\n#0 = ", bit_sequence.count("0"))
        print("\n#1 = ", bit_sequence.count("1"))

    end_time = time.time()
    print('Runtime: ', end_time - begin_time)


main()
