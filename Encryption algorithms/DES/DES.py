import binascii

IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)
IP_INV = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
)
PC1 = (
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
)
PC2 = (
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
)

E = (
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)

Sboxes = {
    0: (
        14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
    ),
    1: (
        15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
    ),
    2: (
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
    ),
    3: (
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
    ),
    4: (
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
    ),
    5: (
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
    ),
    6: (
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
    ),
    7: (
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
    )
}

P = (
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
)


def apply_permutation(to_permute, format_len, table):
    to_permute_binary = bin(to_permute)[2:].zfill(format_len)  # get binary and put 0 before to meet format_len
    permutation = []
    for permutation_value in table:
        permutation.append(to_permute_binary[permutation_value - 1])
    return int(''.join(permutation), 2)  # store permuted bits into an int


# shift nr_of_bits bits so I only get the first nr_of_bits
def split_left(to_split, nr_of_bits):
    return to_split >> nr_of_bits


# get the last nr_of_bits bits by resetting to 0 (by & with 0) the first nr_of_bits and leaving the  other nr_of_bits as they are (by & with 1)
def split_right(to_split, nr_of_bits):
    return to_split & (2 ** nr_of_bits - 1)


def rotate_left(n, nr_of_rot, nr_of_bits):

    return (n << nr_of_rot) & (2**nr_of_bits-1) | (n >> (nr_of_bits - nr_of_rot))


def get_subkeys(key_L, key_R):
    # returns dict of 16 keys (one for each round)
    left_rotations = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

    subkeys = dict.fromkeys(range(0, 17))
    subkeys[0] = (key_L, key_R)

    # create 16 more different key pairs
    i = 0
    for number_of_rotations in left_rotations:
        i += 1
        key_L = rotate_left(subkeys[i - 1][0], number_of_rotations, 28)
        key_R = rotate_left(subkeys[i - 1][1], number_of_rotations, 28)
        subkeys[i] = (key_L, key_R)

    for i, (key_L, key_R) in subkeys.items():
        concatenated_key = (key_L << 28) + key_R
        subkeys[i] = apply_permutation(concatenated_key, 56, PC2)
    return subkeys


def get_6_bit_blocks(plain_R):
    shift_by = 42
    bits_to_interpret = []
    while shift_by >= 0:
        # make & with 111111 and every 6 bits to isolate them, then removing 0's from the end
        bits_to_interpret.append((plain_R & (0b111111 << shift_by)) >> shift_by)
        shift_by -= 6
    return bits_to_interpret


def process_right_member(plain_R, subkey):
    plain_R = apply_permutation(plain_R, 32, E)
    plain_R ^= subkey

    bits_to_interpret = get_6_bit_blocks(plain_R)

    # getting the values from sboxes
    i = -1
    for bits in bits_to_interpret:
        i += 1
        row = ((0b100000 & bits) >> 4) + (0b1 & bits)  # getting the row from the number created from first and last bit
        col = (0b011110 & bits) >> 1  # getting the column from the number created by the inner bits
        bits_to_interpret[i] = Sboxes[i][16 * row + col]

    plain_R = 0
    shift_by = 28
    for bits in bits_to_interpret:
        plain_R += (bits << shift_by)
        shift_by -= 4

    plain_R = apply_permutation(plain_R, 32, P)

    return plain_R


def process_LR_16_times(left, right, decrypt, subkeys):
    previous_L = left
    previous_R = right
    for i in range(1, 17):
        if decrypt:
            i = 17 - i
        initial_R_copy = previous_R
        new_R = previous_L ^ process_right_member(previous_R, subkeys[i])
        previous_L = initial_R_copy
        previous_R = new_R
    # return reversed
    left = new_R
    right = initial_R_copy
    return [left, right]


def encrypt(plain_text, key, decrypt=False):

    plain_text = apply_permutation(plain_text, 64, IP)
    plain_L = split_left(plain_text, 32)
    plain_R = split_right(plain_text, 32)

    key = apply_permutation(key, 64, PC1)
    key_L = split_left(key, 28)
    key_R = split_right(key, 28)
    subkeys = get_subkeys(key_L, key_R)

    left_right = process_LR_16_times(plain_L, plain_R, decrypt, subkeys)
    # concatenate
    cipher_block = (left_right[0] << 32) + left_right[1]

    # final permutation
    cipher_block = apply_permutation(cipher_block, 64, IP_INV)

    return cipher_block



def main():

    key = 0x17a7c6e94f822e83
    plain = 0x2205aa59e2f85cc5

    print('key        = ', hex(key))
    print('plain_text = ', hex(plain))
    cipher_text = encrypt(plain, key)
    print('encrypted  = ', hex(cipher_text))
    plain = encrypt(cipher_text, key, decrypt=True)
    print('decrypted  = ', hex(plain))

main()


