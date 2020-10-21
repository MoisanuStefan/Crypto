import DES


def generate_keys():
    keys = []
    for i in range(0, 256):
        key = i
        for j in range(0,7):
            key = key * (2 ** 8) + i
        keys.append(key)
    return keys


def generate_encryption_dict(plain, keys):

    encryption_pairs = dict.fromkeys(keys)
    for i in encryption_pairs.keys():
        encryption_pairs[i] = DES.encrypt(plain, i)
    return encryption_pairs


def attack(plain, crypto):
    key_pairs = {}
    keys = generate_keys()
    encryption_pairs = generate_encryption_dict(plain, keys)
    for i in keys:
        decrypted = DES.encrypt(crypto, i, True)
        for item in encryption_pairs.items():
            if item[1] == decrypted:
                key_pairs[item[0]] = i  # add the pair (key_from_encryption, key_from_decryption)
    return key_pairs


def main():
    plain = 0x2205aa59e2f85cc5
    key1 = 0x1212121212121212
    key2 = 0xf3f3f3f3f3f3f3f3
    crypto1 = DES.encrypt(plain, key1)
    crypto2 = DES.encrypt(crypto1, key2)

    successful_attack = False
    key_pairs = attack(plain, crypto2)
    print("Key pairs returned by attack: ")
    for item in key_pairs.items():
        print('key1: ',hex(item[0]), ' key2: ', hex(item[1]))
        if item[0] == key1 and item[1] == key2:
            successful_attack = True
    if successful_attack:
        print('Algorithm successfully found both keys.')


main()
