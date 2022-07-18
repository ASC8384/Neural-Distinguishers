import tinyjambu as tj
import random as rnd
import numpy as np


def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> (7 - shift)) & 0x1


# 0 1 2 3 4 5 6 7
# 4 5 6 7 0 1 2 3

# https://stackoverflow.com/a/47521145/10005411
def vec_bin_array(arr, m):
    """
    Arguments:
    arr: Numpy array of positive integers
    m: Number of bits of each integer to retain

    Returns a copy of arr with every element replaced with a bit vector.
    Bits encoded as int8's.
    """
    to_str_func = np.vectorize(lambda x: np.binary_repr(x).zfill(m))
    strs = to_str_func(arr)
    ret = np.zeros(list(arr.shape) + [m], dtype=np.int8)
    for bit_ix in range(0, m):
        fetch_bit_func = np.vectorize(lambda x: x[bit_ix] == '1')
        ret[..., bit_ix] = fetch_bit_func(strs).astype("int8")
    return ret


def bin_array(num, m):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)


AD_LEN = 64  # 32 -bytes of associated data
CT_LEN = 64  # 64 -bytes of plain/ cipher text


def create_data(diff, n):
    # random secret key of 128 -bit
    key = rnd.randbytes(16)
    # print(key, len(key))
    # tm1 = np.frombuffer(key, dtype='b')
    # print(tm1, len(tm1))
    Y = np.random.choice([0, 1], n, p=[0.5, 0.5])
    Y = Y & 1

    x1 = []
    x2 = []

    for i in range(n):
        # random nonce of 96 -bit
        nonce = rnd.randbytes(12)
        # random associated data
        data = rnd.randbytes(AD_LEN)
        # random plain text
        text1 = rnd.randbytes(CT_LEN)
        if Y[i] == 1:
            text2 = bytes(a ^ b for a, b in zip(text1, diff))
        else:
            text2 = rnd.randbytes(CT_LEN)
        # print(bytes(a ^ b for a, b in zip(text1, text2)))
        # text2 = bytes(a ^ b for a, b in zip(rnd.randbytes(CT_LEN), diff))
        # print('first', text1)
        # print('second', text2)
        enc1, _ = tj.tinyjambu_128_encrypt(key, nonce, data, text1)
        enc2, _ = tj.tinyjambu_128_encrypt(key, nonce, data, text2)
        # print(enc1, len(enc1))
        x1.append(np.frombuffer(enc1, dtype=np.uint8))
        x2.append(np.frombuffer(enc2, dtype=np.uint8))
        # print(enc1, len(enc1), enc1[0], enc1[1])
        # t1 = [access_bit(enc1,i) for i in range(len(enc1)*8)]
        # print(t1, len(t1))
        # x1.append([access_bit(data,i) for i in range(len(enc1)*8)])
        # x1.append("{:08b}".format(int(enc1.hex(),16)))
        # print(x1)
        # x1.append(''.join(format(ord(byte), '08b') for byte in enc1))
        # x1.append(BitArray(hex=enc1))

    x1 = np.array(x1)  # , dtype=np.uint16)
    x2 = np.array(x2)  # , dtype=np.uint16)
    # x1 = np.frombuffer(x1, dtype=np.uint16)
    # print(x1, '\n')
    X = np.array(x1 ^ x2)
    X = vec_bin_array(X, 8)
    return (X, Y)


if __name__ == "__main__":
    diff = [0x0] * CT_LEN
    diff[0] = 0x2
    # diff[1] = 0x0
    # diff[5] = 0x0
    # print(diff)
    # print(data(diff, 1))
    n = 2 ** 20

    X, Y = create_data(diff, n)
    # print(X[0])
    # print(Y)
    version = '8'
    # 1, 2**20, 0x8000, CT = 32, AD_LEN = 32
    # 2, 2**20, 0x2000, CT = 32  AD_LEN = 32
    # 3, 2**20, 0x8000, CT = 64  AD_LEN = 32
    # 4, 2**20, 0x2000, CT = 64  AD_LEN = 32
    # 5, 2**20, 0x8000, CT = 32, AD_LEN = 64
    # 6, 2**20, 0x2000, CT = 32  AD_LEN = 64
    # 7, 2**20, 0x8000, CT = 64  AD_LEN = 64
    # 8, 2**20, 0x2000, CT = 64  AD_LEN = 64
    np.save(version + '_X.npy', X)
    np.save(version + '_Y.npy', Y)
    #
    n = 2 ** 17
    X, Y = create_data(diff, n)
    np.save(version + '_Xv.npy', X)
    np.save(version + '_Yv.npy', Y)
    n = 2 ** 17
    X, Y = create_data(diff, n)
    np.save(version + '_Xt.npy', X)
    np.save(version + '_Yt.npy', Y)
