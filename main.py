
import tea

def main():

    cipher = tea.TEA(0xA56BABCD00000000FFFFFFFFABCDEF01)

    ciphertext = cipher.encrypt(0x123456789ABCDEF)

    print('ciphertext 1: ',ciphertext)

    cipher2 = tea.TEA(0xA56BABCD00000000FFFFFFFFABCDEF01)

    plaintext = cipher2.decrypt(ciphertext)

    print('plaintext 1: ', plaintext)

    plainIn = open('plain_in.txt','r')
    cipher3 = tea.TEA(0xA56BABCD00000000FFFFFFFFABCDEF01)
    text = plainIn.read().rstrip('\n')
    ciphertext2 = cipher3.encrypt(text)
    plainIn.close()
    cipherOut = open('cipher_out.txt','w')
    cipherOut.write(ciphertext2)
    cipherOut.close()


    cipherIn = open('cipher_in.txt','r')
    cipher4 = tea.TEA(0xA56BABCD00000000FFFFFFFFABCDEF01)
    plaintext2 = cipher4.decrypt(cipherIn.read().rstrip('\n'))
    cipherIn.close()
    plainOut = open('plain_out.txt','w')
    plainOut.write(plaintext2)
    plainOut.close()


if __name__ == '__main__':
    main()



