import argparse
from typing import List
import random

def gen_key(val:int) -> List[int]:
    random.seed(val)
    rand_val = random.randint(0, 2**64)

    rand_val = format(rand_val%(2**64), '064b')
    rand_val = [int(i) for i in rand_val]

    return rand_val

def read_from_file(in_file:str) -> str:
    file = open(in_file)
    msg = "".join(file.readlines())

    return msg

def dump_to_file(msg:str, out_file:str):
    file = open(out_file, 'w')

    file.write(msg)

# https://www.geeksforgeeks.org/python/python-convert-string-to-binary/
def str_to_bin(string:str) -> List[List[int]]:
    str_bin = []

    for char in string:
        char_byte = format(ord(char), '08b')
        byte_array = [int(bit) for bit in char_byte]
        str_bin.append(byte_array)

    return str_bin

def bin_to_str(bin:List[List[int]]) -> str:
    res = ""
    for i in range(len(bin)):
        byte = ""
        for bit in bin[i]:
            byte += str(bit)

        res += chr(int(byte,2))
    
    return res 

### Source code above supplied by Professor Leeson
#################################################################

class a5_1:
    def __init__(self, key):
        '''The constructor takes a key (a list of 64 bits) as an argument and loads bits
        from the key into three shift registers. Register 'x' receives 19 bits from the key,
        register 'y' receives 22 bits from the key, and register 'z' receives 23 bits from the key.'''
        assert len(key) == 64, "Key must be of length 64" # ensure key is proper length before proceeding

        # initialize registers to empty lists
        self.x = []
        self.y = []
        self.z = [] 
        
        # load the shift registers using key
        for i in range (len(key)):
            # load first register (x) with the first 19 bits
            if (i < 19):
                self.x.append(key[i])
            # load second register (y) with 22 bits
            if (i >= 19 and i < 41): # next 22
                self.y.append(key[i])
            # load third register (z) with 23 bits
            if (i >= 41): # next 23
                self.z.append(key[i])

    def gen_bit(self) -> int:
        '''The function gen_bit generates the next bit for the stream cipher. It finds the most common
        bit from three bits (all from different registers), exclusive or's bits of each register individually 
        to find 't' (the bit that will be placed at the first slot of the register), shifts bits of the registers,
        and outputs the bit result of XORing one bit from each register.'''
        # get majority from three selected bits
        m = ([self.x[8], self.y[10], self.z[10]].count(1) > 1)

        # check if the eighth bit in first register equals majority
        if (self.x[8] == m):
            # XOR four bits of register together
            t = (self.x[13] ^ self.x[16] ^ self.x[17] ^ self.x[18])

            # shift bits to right
            for i in range(18):
                self.x[i] = self.x[i-1] # set current bit to next bit
            self.x[0] = t # set first bit of first register to t
        
        # check if tenth bit in second register equals majority
        if (self.y[10] == m):
            # XOR two bits of register together
            t = (self.y[20] ^ self.y[21])

            # shift bits to right
            for i in range (21):
                self.y[i] = self.y[i-1]
            self.y[0] = t # first bit becomes t
        
        # check if tenth bit in third register equals majority
        if (self.z[10] == m):
            # XOR four bits of register together
            t = (self.z[7] ^ self.z[20] ^ self.z[21] ^ self.z[22])

            # shift bits to right
            for i in range (22):
                self.z[i] = self.z[i-1]
            self.z[0] = t # first bit becomes t
             
        return (self.x[18] ^ self.y[21] ^ self.z[22])

def encrypt_message(msg_bin:List[List[int]], key_stream:a5_1) -> List[List[int]]:
    '''This function encrypt_message takes two arguments: msg_bin (the binary representation of the plaintext)
    and key_stream (an a5_1 object). The function iterates through each byte in the msg_bin, XOR's each bit in
    the byte with a generated bit from the key stream, and places the encrypted byte into the cipher bin, then
    outputs the binary representation of the ciphertext.'''
    cipher_bin = []

    # go through each bit in representation of plaintext (msg_bin)
    for byte in msg_bin:
        # encrypt each bit
        encrypted_byte = [(bit ^ key_stream.gen_bit()) for bit in byte] # XOR each message bit with a key bit
        cipher_bin.append(encrypted_byte) # place in cypher bin

    return cipher_bin

def decrypt_message(cipher_bin:List[List[int]], key_stream:a5_1) -> List[List[int]]:
    '''This function decrypt_message takes two arguments: cipher_bin (the binary representation of the ciphertext) and
    key_stream (an a5_1 object). The function calls encrypt_message on the cipher_bin and key_stream to decrypt the bits
    in the cipher_bin, then outputs the binary representation of the plaintext.'''
    # call encrypt message function on cipher bin
    decrypt_bin = encrypt_message(cipher_bin, key_stream)
    
    return decrypt_bin

#################################################################
### Source code below supplied by Professor Leeson

parser = argparse.ArgumentParser(prog='HW-2: A5/1')
parser.add_argument("--mode",choices=["encrypt", "decrypt"],  required=True, help="Encrypt or Decrypt mode")
parser.add_argument("--key", type=int, required=True, help="The key value")
parser.add_argument("--in-file", required=True, help="The file to read from")
parser.add_argument("--out-file", help="The file to write to")


def main():
    args = parser.parse_args()

    key = gen_key(args.key)
    key_stream = a5_1(key)
    msg = read_from_file(args.in_file)
    msg_bin = str_to_bin(msg)

    if args.mode == "encrypt":
        out_bin = encrypt_message(msg_bin, key_stream)
    else:
        out_bin = decrypt_message(msg_bin, key_stream)

    out_msg = bin_to_str(out_bin)

    if args.out_file:
        dump_to_file(out_msg, args.out_file)
    else:
        print(out_msg)

main()