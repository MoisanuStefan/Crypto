import codecs
import collections
import random
import string
import time

global k_frequency
global generated_keystream
k_frequency = [0 for i in range(256)]
generated_keystream = []

def Init(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def Trans(S):
    i = 0
    j = 0
    while i < 256:
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K


def get_keystream(key):
    S = Init(key)
    return Trans(S)


def xor(key, text):
    global k_frequency

    key = [ord(c) for c in key]
    keystream = get_keystream(key)
    res = ''
    for c in text:
        k = next(keystream)
        generated_keystream.append(k)
        k_frequency[k] += 1
        val = chr((ord(c) ^ k))
        res = res + val
    return res


def encrypt_decrypt(key, plaintext_ciphertext):
    return xor(key, plaintext_ciphertext)


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def CountFrequency(arr):
    return collections.Counter(arr)

def get_unique_values(arr):
    unique_values = []
    for i in arr:
        if unique_values.count(i) == 0:
            unique_values.append(i)
    return unique_values


def bias_attack():
    plaintext = randomString(256)
    key = randomString(16)
    encrypt_decrypt(key, plaintext)
    k_frequency = CountFrequency(generated_keystream)
    unique_values = get_unique_values(generated_keystream)
    print(len(unique_values), ' unique values in generated keystream: ', unique_values)
    print('Frequencies of unique values: ', k_frequency)



def main():
    print('Bias attack: ')
    bias_attack()

    key = input("Give me the key: ")
    plaintext = input("Give me the plaintext: ")

    begin_time = time.time()

    ciphertext = encrypt_decrypt(key, plaintext)
    decrypted = encrypt_decrypt(key, ciphertext)

    end_time = time.time()

    print('plaintext:', plaintext)
    print('ciphertext:', ciphertext)
    print('Decrypted: ', decrypted)
    print('Runtime: ', end_time - begin_time)


main()
