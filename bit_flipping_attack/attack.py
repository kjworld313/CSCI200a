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

def bit_flip_attack(original:List[List[int]], injected:List[List[int]], encrypted:List[List[int]]) -> List[List[int]]:
    '''The function bit_flip_attack takes three arguments: original (the binary representation of the original message),
    injected (the binary representation of the injected message), encrypted (the binary encryption of the original message).
    The function goes through bits in each argument and XOR's each bit with a bit from the other arguments to acquire the injected
    message XOR'd with the key used to encrypt the original message, and outputs an encrypted bin containing bytes with bits from
    the encrypted injected message.'''
    encryption_bin = [] # holds encrypted bytes
    xor_byte = 0 # counter for bytes in XOR'd argument
    xor_bit = 0 # counter for bits in bytes (in XOR'd argument)

    # iterate through binary representation of the original message
    for byte in original:
        encrypted_byte = []
        for bit in byte:
            # XOR the bit with a bit from the injected binary and a bit from the encrypted binary
            encrypted_byte.append(bit ^ injected[xor_byte][xor_bit] ^ encrypted[xor_byte][xor_bit])
            # make sure current bit does not exceed last possible index
            if (xor_bit < 7): # 7 is last possible index in 8 bit byte
                xor_bit += 1
            else: # reset current bit counter
                xor_bit = 0
        encryption_bin.append(encrypted_byte)
        xor_byte += 1 # go to next byte 

    return encryption_bin


#################################################################
### Source code below supplied by Professor Leeson

parser = argparse.ArgumentParser(prog='HW-2')
parser.add_argument("--original", required=True, type=str, help="The original message for the bit flip attack")
parser.add_argument("--injected", required=True, type=str, help="The injected message for the bit flip attack")
parser.add_argument("--enc", required=True, type=str, help="The encrypted file for bit flip attack")
parser.add_argument("--out-file", required=True, type=str, help="The file to save the attacked encryption to")

def main():
    args = parser.parse_args()

    org_msg = read_from_file(args.original)
    inj_msg = read_from_file(args.injected)
    enc_msg = read_from_file(args.enc)

    org_bin = str_to_bin(org_msg)
    inj_bin = str_to_bin(inj_msg)
    enc_bin = str_to_bin(enc_msg)

    attack = bit_flip_attack(org_bin, inj_bin, enc_bin)

    dump_to_file(bin_to_str(attack), args.out_file)

main()