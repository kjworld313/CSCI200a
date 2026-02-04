import argparse
import string

parser = argparse.ArgumentParser(prog='HW-1')
parser.add_argument("--cipher", choices=["caesar", "keyword"], required=True, help="What type of cipher to use")
parser.add_argument("--mode", choices=["encrypt", "decrypt"], default="encrypt", help="SHould it be used in encrypt or decrypt mode")
parser.add_argument("--keyword", type=str, help="What keyword the keyword cipher should use")
parser.add_argument("--shift", type=int, help="What shift the caesar cipher should use")
parser.add_argument("--text", type=str, help="Text to cipher or decipher")

def cipher(mode:str, alphabet:dict, text:str) -> str:
    '''The cipher function takes three arguments: mode (string), alphabet (dictionary),
    and text (string). The function determines the operation depending on the mode argument and 
    uses the argument alphabet to either encrypt or decrypt the argument text. The function outputs
    the resulting encryption or decryption, a string, if argument mode is a valid option.'''
    if (mode == "encrypt"):
        ciphertext = "" # empty string to hold encrypted text
        
        # iterate through the letters in the text to map to alphabet
        for character in text:
            # make sure character is a letter before adding to the ciphertext 
            if (character in alphabet.values()):
                # locate the letter in the alphabet and get the encrypted value
                ciphertext += alphabet.get(character) # add encrypted letter to the ciphertext
            else: # do not encrypt but add to ciphertext
                ciphertext += character 
        return ciphertext
    elif (mode == "decrypt"):
        plaintext = "" # empty string to hold decrypted text
        inverted_alphabet = {} # dictionary to hold reversed key value pairs

        # invert the alphabet dictionary
        for key in alphabet:
            # reverse the key value pair
            inverted_alphabet[alphabet.get(key)] = key

        # iterate through characters in the text to map to inverted alphabet
        for character in text:
            # check if character is a letter, if so add to plaintext
            if (character in inverted_alphabet.values()):
                # locate letter in alphabet and get decrypted value
                plaintext += inverted_alphabet.get(character) # add decrypted letter to plaintext
            else: # do not encrypt, add to plaintext
                plaintext += character          
        return plaintext
    else:
        return "Invalid mode."
    
def caesar_helper(left_bound:int, right_bound:int, shift:int, alphabet:list)->dict:
    '''The caesar_helper function takes four arguments: left_bound (integer), right_bound (integer), 
    shift (integer), and alphabet (list of strings). The function shifts letters and handles cases where the 
    encrypted letter value may exceed the right bound value by wrapping around to beginning of alphabet
    using ASCII values. The function outputs a dictionary of letters mapped to encrypted letters.'''
    encrypted_letters = {}

    # go through each letter in the alphabet and map letters to encrypted values
    for letter in alphabet:
        encryption = ord(letter) + shift # shifted letter

        # make sure encrypted alphabet wraps around after last possible ascii letter
        if (encryption > right_bound): 
            # find letter position in alphabet (subtract left bound), then find remaining shift value on 26 letter scale
            encryption = ((encryption - left_bound) % 26) + left_bound # adjust to start at left bound (first ascii letter, ex: 'a' or 'A')

        # create a key value pair for the letter and encrypted value
        encrypted_letters[letter] = chr(encryption) # get character with new ASCII value
        
    return encrypted_letters

def caesar_alphabet(shift:int) -> dict:
    '''The caesar_alphabet function takes an integer argument, shift. The function shifts
    the uppercase and lowercase alphabets by the shift and outputs a dictionary mapping the 
    alphabet to the cipher alphabet.'''

    # call caesar helper function and create uppercase and lowercase alphabet dictionaries 
    uppercase_alphabet = caesar_helper(65, 90, shift, string.ascii_uppercase) # use ascii 'A' (65) as left bound and ascii 'Z' (90) as right bound
    lowercase_alphabet = caesar_helper(90, 122, shift, string.ascii_lowercase) # use ascii 'a' (90) as left bound and ascii 'z' (122) as right bound

    # merge the dictionaries into one
    uppercase_alphabet.update(lowercase_alphabet) # referenced function from geeksforgeeks (append argument dictionary to calling dictionary)
    caesar_alphabet = uppercase_alphabet

    return caesar_alphabet

def keyword_helper(ascii_position:int, right_bound:int, keyword:str, alphabet:list)->dict:
    '''The keyword_helper function takes four arguments: ascii_position (int), right_bound (integer),
    keyword (string), and alphabet (list of strings). The function takes an ascii position to start producing keys for,
    assigns letters in the keyword to alphabet letters as keys, and fills the dictionary with remaining letters
    after letters from the keyword have been used as values. The function outputs a dictionary, the alphabet
    mapped to encrypted alphabet.'''
    keyword_alphabet = {} # empty dictionary to hold alphabet mapped to keyword alphabet
    remaining_letters = [] # empty list to hold and keep track of remaining letters available for use
    position = 0 # iterator to keep track of index in keyword 

    for letter in alphabet:
        remaining_letters.append(letter)

    # go through keyword and map each letter to sequential letters in alphabet
    while (position < len(keyword)): # once keyword letters are exhausted, stop
        # make sure the letter is a unique value
        if (keyword[position] not in keyword_alphabet.values()):
            # create a key value pair with the letter as key and encrypted letter as value
            keyword_alphabet[chr(ascii_position)] = keyword[position]
            remaining_letters.remove(keyword[position]) # remove letter from available letters
            ascii_position += 1 # go to next letter in alphabet
        position += 1 # go to next letter in keyword

    # start at next letter and iterate up until right bound (ex: ascii 'z' (122) or ascii 'Z' (90)) to fill remaining letters
    while (ascii_position <= right_bound and len(remaining_letters) != 0): 
        # create a key value pair with letter as key and the first remaining letter as a value
        keyword_alphabet[chr(ascii_position)] = remaining_letters[0]
        remaining_letters.remove(remaining_letters[0]) # remove the letter from the list
        ascii_position += 1

    return keyword_alphabet

def keyword_alphabet(keyword:str) -> dict:
    '''The keyword_alphabet function takes a string argument, keyword. The function produces
    the cipher alphabet from the keyword and outputs a dictionary mapping the alphabet to the
    cipher alphabet.'''
    # get both uppercase and lowercase versions of the keyword
    uppercase_keyword = keyword.upper() # disclaimer: know .upper() from grading intro CS
    lowercase_keyword = keyword.lower()

    # call keyword helper function and create uppercase and lowercase alphabet dictionaries 
    uppercase_alphabet = keyword_helper(65, 90, uppercase_keyword, string.ascii_uppercase) # use ascii 'A' (65) as left bound and ascii 'Z' (90) as right bound
    lowercase_alphabet = keyword_helper(97, 122, lowercase_keyword, string.ascii_lowercase) # use ascii 'a' (90) as left bound and ascii 'z' (122) as right bound

    # merge the dictionaries into one
    uppercase_alphabet.update(lowercase_alphabet) # referenced function from geeksforgeeks (append argument dictionary to calling dictionary)
    keyword_alphabet = uppercase_alphabet

    return keyword_alphabet

def main():
    args = parser.parse_args()

    if args.cipher == "caesar":
        alphabet = caesar_alphabet(shift=args.shift)
    else:
        alphabet = keyword_alphabet(keyword=args.keyword)

    res = cipher(mode=args.mode, alphabet=alphabet, text=args.text)

    print(res)

main()