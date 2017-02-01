import string
class TEA:
    def __init__(self, key):
        key = hex(key)[2:]
        self.k0 = int(key[0:8],16)
        self.k1 = int(key[8:16],16)
        self.k2 = int(key[16:24],16)
        self.k3 = int(key[24:],16)


        self.test = []


    def padArr(self, arr):
        padAmt = (8-len(arr)%8)%8
        for i in range(padAmt):
            arr.append('00')

        return arr


    def encryptBlocks(self, blocks):
        block0 = blocks[0]
        block1 = blocks[1]
        s = 0
        delta = 0x9e3779b9

        for i in range(32):

            s += delta
            s &= 0xffffffff
            block0 += (((block1<<4)&0xffffffff) + self.k0) ^ (block1 + s) ^ (((block1>>5)&0xffffffff) + self.k1)
            block0 &= 0xffffffff
            block1 += (((block0<<4)&0xffffffff) + self.k2) ^ (block0 + s) ^ (((block0>>5)&0xffffffff) + self.k3)
            block1 &= 0xffffffff

        return (block0, block1)

    def decryptBlocks(self, blocks):
        block0 = blocks[0] 
        block1 = blocks[1]
        s = 0xC6EF3720 
        delta = 0x9e3779b9

        for i in range(32):

            block1 -= (((block0<<4)&0xFFFFFFFF) + self.k2) ^ (block0 + s) ^ (((block0>>5)&0xFFFFFFFF) + self.k3)
            block1 &= 0xffffffff
            block0 -= (((block1<<4)&0xFFFFFFFF) + self.k0) ^ (block1 + s) ^ (((block1>>5)&0xFFFFFFFF) + self.k1)
            block0 &= 0xffffffff
            s -= delta
            s &= 0xffffffff

        return (block0, block1) 

    def encrypt(self, plaintext):
        charArr = []
        if isinstance(plaintext, str):
            charArr = [hex(ord(char))[2:] for char in plaintext]

        elif isinstance(plaintext,int):
            charArr = [hex(plaintext)[i:i+2] for i in range(2, len(hex(plaintext))-1, 2)]
            if len(hex(plaintext))%2 !=0:
                charArr.append(hex(plaintext)[-1] + '0')


        charArr = self.padArr(charArr)

        #intArr consists of 32-bit ints
        intArr = [int(''.join(charArr[i:i+4]),16) for i in range(0, len(charArr), 4)]
        
        ciphertext = ''

        newIntArr = []
        for i in range(0, len(intArr), 2):
            blocks = self.encryptBlocks((intArr[i],intArr[i+1]))
            newIntArr.append(blocks[0])
            newIntArr.append(blocks[1])

            str0 = hex(blocks[0])[2:].rjust(8,'0')
            str1 = hex(blocks[1])[2:].rjust(8,'0')

            ciphertext += str0 + str1


        return ciphertext 


    def decrypt(self, ciphertext):

        #ciphertext += hex(blocks[0])[2:] + hex(blocks[1])[2:]

        intArr = [int(ciphertext[i:i+8],16) for i in range(0,len(ciphertext), 8)]

        plaintext = '0x'
        plainCharArr = []
        for i in range(0, len(intArr), 2):
            blocks = self.decryptBlocks((intArr[i],intArr[i+1]))
            blocks = (blocks[0] << 32) | blocks[1]
            blockhex = hex(blocks)[2:]
            plaintext += blockhex

            for i in range(0,16,2):
                plainCharArr.append(chr(int(blockhex[i:i+2],16)))

        count = 0
        # count alphabet letters in result of decryption
        for char in plainCharArr[:-7]: # up to 7 characters can be padded
            if char in string.ascii_letters:
                count +=1

        # if most of the result is alphabet letters, treat the result as a string
        # otherwise return it as a hexidecimal string
        if count > .8*(len(plainCharArr)-7):
            plaintext = ''.join(plainCharArr)


        return plaintext
