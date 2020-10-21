import time

import numpy as np
import string
import random


# creates array of ascii codes of characters in string
def convert_to_ascii(text):
    return np.fromiter(map(ord, text), int, count=len(text))


# converts elements of array to binary with 8 bits
def convert_array_to_binary(asciis):
    binary_asciis = []
    for i in range(0, len(asciis)):
        binary_asciis.append(bin(asciis[i])[2:].zfill(8))
    return binary_asciis


#  joins elements in one string and adds a 1
def join_binary_elements(binary_asciis):
    joined_binary_asciis = ''
    for i in binary_asciis:
        joined_binary_asciis += i
    joined_binary_asciis += '1'
    return joined_binary_asciis


#  adds 0 until % 512 = 448
def pad_512_mod_448(binary_string):
    while len(binary_string) % 512 != 448:
        binary_string += '0'
    return binary_string


#  adds 0 to array length in binary until 64 bits
def get_padded_ascii_array_length(joined_binary_asciis):
    return bin(len(joined_binary_asciis) - 1)[2:].zfill(64)


def get_chunks(string_to_chunk, chunk_len):
    return [string_to_chunk[i:i + chunk_len] for i in range(0, len(string_to_chunk), chunk_len)]


def convert_to_int(matrix):
    new_matrix = []
    for array in matrix:
        new_array = []
        for element in array:
            new_array.append(int(element, 2))
        new_matrix.append(new_array)
    return new_matrix


def convert_matrix_to_binary(matrix):
    new_matrix = []
    for array in matrix:
        new_array = []
        for element in array:
            new_array.append(bin(element)[2:].zfill(32))
        new_matrix.append(new_array)
    return new_matrix


def rotate_left(n, d, nr_of_bits):
    return (n << d) | (n >> (nr_of_bits - d))


def get_last_32_bits(number):
    return number & 4294967295


def extend_80(matrix):
    for array in matrix:
        for i in range(16, 80):
            rotated_xor = rotate_left(array[i - 3] ^ array[i - 8] ^ array[i - 14] ^ array[i - 16], 1, 32)
            if rotated_xor > 4294967295:  # that is 32 1's in binary
                rotated_xor = rotated_xor & 4294967295  # taking first 32 bits
            array.append(rotated_xor)

    return matrix


def variable_initialisation(matrix):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for i in range(0, len(matrix)):
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        for j in range(0, 80):
            if 0 <= j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            f = get_last_32_bits(f)
            temp = rotate_left(a, 5, 32) + f + e + k + matrix[i][j]
            e = d
            d = c
            c = rotate_left(b, 30, 32)
            b = a
            a = temp
            a = get_last_32_bits(a)
            b = get_last_32_bits(b)
            c = get_last_32_bits(c)
            d = get_last_32_bits(d)
            e = get_last_32_bits(e)
            # print(hex(a),' ',hex(b),' ', hex(c), ' ', hex(d), ' ',hex(e))
        h0 = get_last_32_bits(h0 + a)
        h1 = get_last_32_bits(h1 + b)
        h2 = get_last_32_bits(h2 + c)
        h3 = get_last_32_bits(h3 + d)
        h4 = get_last_32_bits(h4 + e)
        # print(hex(h0), ' ', hex(h1), ' ', hex(h2), ' ', hex(h3), ' ', hex(h4))

    return (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4


def sha1(plain):
    asciis = convert_to_ascii(plain)
    # print(asciis)
    binary_asciis = convert_array_to_binary(asciis)
    # print(binary_asciis)
    joined_binary_asciis = join_binary_elements(binary_asciis)
    # print(joined_binary_asciis)
    padded_binary_string = pad_512_mod_448(joined_binary_asciis)
    # print(padded_binary_string)
    padded_array_length = get_padded_ascii_array_length(joined_binary_asciis)
    # print(padded_array_length)
    joined_strings = padded_binary_string + padded_array_length
    # print(joined_strings)
    chunks_512 = get_chunks(joined_strings, 512)
    # print(chunks_512)
    chunks_32 = []
    for chunk_512 in chunks_512:
        chunks_32.append(get_chunks(chunk_512, 32))
    # print(chunks_32)
    chunks_32_as_int = convert_to_int(chunks_32)
    extended_matrix = extend_80(chunks_32_as_int)
    binary_extended_matrix = convert_matrix_to_binary(extended_matrix)
    # print(binary_extended_matrix)
    return hex(variable_initialisation(extended_matrix))


def test_vector(plain, hash):
    result = sha1(plain)
    if result == hex(hash):
        print('Success -> ', end=' ')
    else:
        print('Fail -> ', end=' ')

    print('Test with plain: ', plain)


def generate_long_input():
    input = ''
    for i in range(0, 10000):
        input += 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    return input


def validate_function():
    test_vector('', 0xda39a3ee5e6b4b0d3255bfef95601890afd80709)
    test_vector('abc', 0xa9993e364706816aba3e25717850c26c9cd0d89d)
    test_vector('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq', 0x84983e441c3bd26ebaae4aa1f95129e5e54670f1)
    test_vector(
        'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu',
        0xa49b2446a02c645bf419f995b67091253a04a259)
    test_vector(generate_long_input(), 0x34aa973cd4c4daa4f61eeb2bdbad27316534016f)


def get_hamming(string1, string2):
    hamming = 0
    for i in range(0, 160):
        if string1[i] != string2[i]:
            hamming += 1
    return hamming


def avalanche_effect(plain1, plain2):
    hash1 = sha1(plain1)
    hash2 = sha1(plain2)
    hash1 = bin(int(hash1, 16))[2:].zfill(160)
    hash2 = bin(int(hash2, 16))[2:].zfill(160)
    print('Hashing ', plain1, ' and ', plain2, ' ... Results:')
    print(hash1)
    print(hash2)
    hamming = get_hamming(hash1, hash2)
    print('Hamming distance =', hamming, '(', hamming * 100 / 160, '% different)')


def randomString(string_ength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_ength))


def search_dictionary(dictionary, to_search):
    for item in dictionary.items():
        if item[1] == to_search:
            return item[0]
    return 'no_items_found'


def x_to_b_32(hexa):
    return bin(int(hexa, 16))[2:].zfill(160)[0:31]


def search_collision():
    dictionary = dict()

    for i in range(0, 110000):  # 75% possibility of collision
        plain = randomString(random.randint(1, 200))
        cut_hash = x_to_b_32(sha1(plain))
        collision_plain = dictionary.get(cut_hash, '-1')
        if collision_plain != '-1' and collision_plain != plain:
            print('Collision found:')
            print(collision_plain, '\nand\n', plain, '\nhave the same first 32 bits of hash: ', cut_hash)
            return i
        dictionary[cut_hash] = plain
    return 110000


def happy_birthday_sha1():
    print('Starting birthday attack ...')
    start = time.time()
    attempts = search_collision()
    while attempts % 110000 == 0:
        attempts += search_collision()
    end = time.time()
    print('Collision found in ', end - start, 's from ', attempts, 'attempts.')


def main():
    # plain = 'abc'
    # print("Hash value of '", plain, "': ", sha1(plain))
    print('FUNCTION VALIDATION:', end='\n')
    validate_function()
    print(
        '--------------------------------------------------------------------------------------------------------------------------------------------------------------',
        end='\n')
    print('AVALANCHE EFFECT DEMONSTRATION:', end='\n')
    avalanche_effect('abc', 'abb')  # only 1 bit differs between 'b'and 'c')
    print(
        '--------------------------------------------------------------------------------------------------------------------------------------------------------------',
        end='\n')
    happy_birthday_sha1()


main()
