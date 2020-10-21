import cmath
import time
import sympy


def cmmdc(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def areCoprime(a, b):
    if cmmdc(a, b) == 1:
        return True
    return False


#  first e that is coprime with n and phi
def getE(phi, n):
    for i in range(2, phi - 1):
        if areCoprime(i, phi) and areCoprime(i, n):
            return i
    return -1


#  invers modular
def getD(a, m):
    m0 = m
    y = 0
    x = 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x


#  char ord ** e % n
def encrypt(e, n, plaintext):
    cipher = []
    for char in plaintext:
        charr = ord(char) - 96
        poww = pow(charr, e, n)
        cipher.append(poww)
    return cipher


# nr to char ** d % n
def decrypt(d, n, ciphertext):
    plain = ''
    for char in ciphertext:
        poww = pow(char, d, n)
        toadd = chr(poww + 96)
        plain = plain + toadd
    return plain


#  TCR
def decryptFast(d, p, q, ciphertext):
    dp = d % (p - 1)
    dq = d % (q - 1)
    qInv = getD(q, p)
    plain = ''
    for char in ciphertext:
        m1 = pow(char, dp, p)
        m2 = pow(char, dq, q)
        h = (qInv * (m1 - m2)) % p
        m = m2 + h * q
        plain = plain + chr(m + 96)
    return plain


def time_slow_decrypt(d, n, crypto):
    begin = time.time()
    decrypt(d, n, crypto)
    end = time.time()
    print('Slow decrypt in ', end - begin, ' s')


def time_fast_decrypt(d, p, q, crypto):
    begin = time.time()
    decryptFast(d, p, q, crypto)
    end = time.time()
    print('Fast decrypt in ', end - begin, ' s')


def getContinousFunction(n, d):
    convergents = []
    a = n
    b = d
    while b != 0:
        q = a // b
        r = a % b
        a = b
        b = r
        convergents.append(q)
    return convergents


def getSuccesiveConvergents(a):
    l = len(a)
    fractions = []
    h0 = 1
    h1 = 0
    k0 = 0
    k1 = 1
    count = 0
    while count < l:
        h = a[count] * h1 + h0
        h0 = h1
        h1 = h
        k = a[count] * k1 + k0
        k0 = k1
        k1 = k
        fractions.append((k, h))
        count += 1
    return fractions


def wienerAttack(e, n):
    fractions = getSuccesiveConvergents(getContinousFunction(e, n))
    for count in range(0, len(fractions)):
        k, d = fractions[count]
        if k == 0 or d == 1:
            continue
        if d % 2 == 0:
            continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) / k
        # solve quadric equation
        a = 1
        b = -(n - phi + 1)
        c = n
        delta = (b ** 2) - (4 * a * c)
        sol1 = (-b - cmath.sqrt(delta)) / (2 * a)
        sol2 = (-b + cmath.sqrt(delta)) / (2 * a)
        if sol1 * sol2 != n:
            continue
        return d
    return -1


if __name__ == '__main__':

    print('Part1. Key, encrypt, decrypt:\n')
    plain = 'plaintext'
    p = sympy.nextprime(pow(2, 511))
    q = sympy.nextprime(p + 1)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = getE(phi, n)
    d = getD(e, phi)
    crypto = encrypt(e, n, plain)
    decrypted = decryptFast(d, p, q, crypto)
    print('plaintext = ', plain)
    print('p = ', p)
    print('q = ', q)
    print('Public key: (e, n) = (', e, ', ', n, ')')
    print('Private key: (d, n) = (', d, ', ', n, ')')
    print('Encrypted: ', crypto)
    print('Decrypted: ', decrypted)

    print(
        '\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n')

    print('Part 2. Time comparison: ')
    time_slow_decrypt(d, n, crypto)
    time_fast_decrypt(d, p, q, crypto)

    print(
        '\n----------------------------------------------------------------------------------------------------------------------------------------------------------------\n')

    print('Part3. Wiener attack:')
    e = 42667
    n = 64741
    d = wienerAttack(e, n)
    if d != -1:
        print('For public key (', e, ', ', n, ') attack found private key (', d, ', ', n, ')')
    else:
        print('Private key could not be found')
