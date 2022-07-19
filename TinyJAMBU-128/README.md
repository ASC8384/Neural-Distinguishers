# TinyJAMBU-128

## Version

`tiny.py` is the code that generates data.

`ver_1.7z` is a compressed file containing the training and validation sets of version 1, with a training set of size $2^20$, a input difference of `0x80000000000000000000000000000000`, a plaintext length of 32, and an AD length of 32.

```
# 1, 2**20, 0x8000, CT = 32, AD_LEN = 32
# 2, 2**20, 0x2000, CT = 32  AD_LEN = 32
# 3, 2**20, 0x8000, CT = 64  AD_LEN = 32
# 4, 2**20, 0x2000, CT = 64  AD_LEN = 32
# 5, 2**20, 0x8000, CT = 32, AD_LEN = 64
# 6, 2**20, 0x2000, CT = 32  AD_LEN = 64
# 7, 2**20, 0x8000, CT = 64  AD_LEN = 64
# 8, 2**20, 0x2000, CT = 64  AD_LEN = 64
```
