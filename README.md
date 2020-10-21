# Crypto
Python implementations written as tasks for Introduction to cryptography course:
  - Random number generators:
    - BBS.py --> Blum-Blum-Shub
    - Jacobi.py --> Random number generator using Jacobi Symbol
    - LSFR.py --> Linear-feedback shift register
  - Encryption algorithms:
    - DES.py --> DES (Data Encryption Standard) is a block cipher algorithm that takes plain text in blocks of 64 bits and converts them to ciphertext using keys of 48 bits. It is a symmetric key algorithm, which means that the same key is used for encrypting and decrypting data.
      - MeetInTheMiddle.py -> The meet-in-the-middle attack is one of the types of known plaintext attacks. The intruder has to know some parts of plaintext and their ciphertexts. Using meet-in-the-middle attacks it is possible to break ciphers, which have two or more secret keys for multiple encryption using the same algorithm.
    - RSA.py --> The RSA (Rivest–Shamir–Adleman) algorithm is an asymmetric cryptography algorithm; this means that it uses a public key and a private key (i.e two different, mathematically linked keys). As their names suggest, a public key is shared publicly, while a private key is secret and must not be shared with anyone.
    - SHA-1 --> SHA-1 (Secure Hash Algorithm 1) is a cryptographic hash function which takes an input and produces a 160-bit (20-byte) hash value. This hash value is known as a message digest. This message digest is usually then rendered as a hexadecimal number which is 40 digits long.
