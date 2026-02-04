import argparse

parser = argparse.ArgumentParser(prog='HW-0')
parser.add_argument("--file", type=str, help="What file to XOR")
parser.add_argument("--mod", type=int, help="What number to use as the modulo base")
parser.add_argument("--num", type=int, help="What number to calculate using modulo")


### Source code above supplied by Professor Leeson
#################################################################

def XOR(file_loc:str):
    '''The XOR function takes a string argument, file_loc, which represents
    the location of a file containing two binary numbers. The function outputs None,
    opens the file, extracts the binaries from the file, pads binaries with 0 if the binaries
    have unequal numbers of bits, and compares bits (representing exclusive or, of the two bits only
    one can be 1 in order to evaluate the comparison to true or 1) to form the XOR binary result. The
    function prints the result.'''
    # find file and open
    binaries_file = open(file_loc)
    binaries = binaries_file.read().strip().splitlines() # grab both binaries

    # grab length of binaries
    first_size = len(binaries[0])
    second_size = len(binaries[1])

    # check size of both binaries and pad with 0's if unequal size
    if (first_size != second_size):
        # check which is smaller
        if (first_size < second_size):
            # pad with 0's to get first binary same length as second
            for i in range(0, second_size-first_size):
                binaries[0] = "0" + binaries[0] # concatenate with 0
        else: # second binary is smaller
            # pad with 0's for amount needed for second binary
            for i in range(0, first_size-second_size):
                binaries[1] = "0" + binaries[1] # concatenate with 0

    # go through both binaries and compare bits
    XOR_result = "" # output string
    for i in range(0, len(binaries[0])):
        # check if bit of the first binary and second binary are equal
        if (binaries[0][i] == binaries[1][i]):
            XOR_result += "0"
        else: # either bit is 1 but not both
            XOR_result += "1"

    # print result and close file
    print(XOR_result)
    binaries_file.close()

def MOD(dividend:int, divisor:int):
    '''The MOD function takes two arguments: dividend, an int, and divisor, an int. The function outputs None,
    checks base cases (one or both inputs are 0), handles cases where dividend is less than divisor, recursively calls
    itself with dividend argument decremented by divisor, and prints the remainder of dividing the dividend by the divisor.'''
    # check if the dividend is zero
    if dividend == 0:
        if divisor == 0: # divisor is 0 so operation result is undefined
            print("Undefined")
        else: # nonzero value, valid input
            print(dividend)
    elif dividend < divisor: # check if dividend is less than divisor
        print(dividend)
    else:
        # recursively call MOD, decrementing dividend by divisor, until dividend is less than divisor
        MOD(dividend-divisor, divisor)

#################################################################
### Source code below supplied by Professor Leeson

def main():
    args = parser.parse_args()

    if args.file:
        XOR(args.file)
    else:
        MOD(args.num, args.mod)

main()