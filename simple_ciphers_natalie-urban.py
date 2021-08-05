#!/usr/bin/env python
"""CSCI 1106 Assignment 2: Simple Ciphers

Author: Natalie Urban
A command-line program which can encipher files using simple ROT letter substitution  ciphers or
decipher the same by exhaustive search."""

import sys

DICTIONARY_FILEPATH = "some_words.txt"

def main(argv):
    if len(sys.argv) == 1:
        print("Usage:")
        print("simple_ciphers.py encode (input filepath) [optional rot val] [optional rot shift]")
        print("simple_ciphers.py decode (input filepath)")
    else:
        mode = sys.argv[1]
        input_filepath = sys.argv[2]
        fin = open(input_filepath,"r")
        input_text = fin.read()
        fin.close()
        
        if mode == "encode":
            rot_val = 3
            if len(sys.argv) > 3:
                rot_val = int(sys.argv[3])
            rot_shift = 0
            if len(sys.argv) > 4:
                rot_shift = int(sys.argv[4])
            print(cipher(input_text,rot_val,rot_shift))
        elif mode == "decode":
            print(decipher(input_text))

#########################################################################
#
# This function begins with taking in input text and a rotational shift value
# and then generates an associated character to the input text characters.
# These new shifted characters are place into the output string and returned.
# If a character is not recognized as a letter, the function keeps it as it is.
#
#########################################################################

def cipher(input_text,rot_val,rot_shift):

    output_string = ""
    for x in input_text:
        y = rotate_character(x,rot_val)
        if y != "false":
            output_string += y
            rot_val = (rot_val + rot_shift) % 26
        else:
            output_string += x
    return output_string

#########################################################################
#
# This function calls read_dictionary to read a text file dictionary. The
# function loops through to find every possible combination of letters within
# the text file. The combinations are then compared to the dictionary file
# letters. The combination that has the most matches in the dictionary file
# is then returned and the phrase is printed.
#
#########################################################################

def decipher(input_text):

    dictionary = read_dictionary(DICTIONARY_FILEPATH)
    rot_val = -1
    rot_shift = 0
    max_grade = 0
    decoded_message = ""
    while (rot_val < 25):
        rot_val += 1
        rot_shift = 0
        while rot_shift < 25:
            output_cipher = cipher(input_text,rot_val,rot_shift)
            rot_shift += 1
            message_grade = grade_message(output_cipher.split(), dictionary)
            if message_grade > max_grade:
                max_grade = message_grade
                decoded_message = output_cipher

    if max_grade > 0: 
        return(decoded_message)
        print(decoded_message)
    elif max_grade < 1:
        print("Not enough word matches")
        
#########################################################################
#
# This function takes in two arguments both a single-character string
# converted to uppercase and an integer on the value of rotation. If the
# arguments passes the test to see if a letter is present and a number is
# between 25 and -25, then it is added to a string. The rotate value loops
# through the string and changes the characters by the number of rotate value.
#
#########################################################################

def rotate_character(the_character,rot_val):
    
    if len(the_character) > 1:
        return("false")
    elif ord(the_character.upper()) < 65 or ord(the_character.upper()) > 90:
        return("false")
    elif rot_val > 25 or rot_val < -25:
        return("false")   
    else:
        upper_alphabet = ""
        for i in range(ord("A"),ord("Z")+1):
            upper_alphabet += chr(i)

        lower_alphabet = ""
        for i in range(ord("a"),ord("z")+1):
            lower_alphabet += chr(i)

        if the_character in lower_alphabet:
            index_character = lower_alphabet.index(the_character)
            rot_index = index_character + rot_val
            mod_rot_index = rot_index % 26
            final_value = lower_alphabet[mod_rot_index]
            return(final_value)

        if the_character in upper_alphabet:
            index_character = upper_alphabet.index(the_character)
            rot_index = index_character + rot_val
            mod_rot_index = rot_index % 26
            final_value = upper_alphabet[mod_rot_index]
            return(final_value)

#########################################################################
#
# This function takes in a filepath containing a list of all capital words
# with one per line. The function opens a file, and reads it. If the file
# cannot be read, the function exits. Each new line in the file is stripped
# and the words are put into a list.
#
#########################################################################

def read_dictionary(filepath):

    file_list=[]
    
    try:
        dict_file = open(filepath,"r")
    except:
        print("Could not open dictionary file: " + filepath)
        sys.exit()
        
    for line in dict_file:
        file_list.append(line.strip())
    return file_list

#########################################################################
#
# This function converts the plaintext to uppercase, so known_words
# and plaintext can be compared. The function divides the plaintext words
# into separate groups in a list. A similar_word list is created to
# hold the number of similar words between plaintext and known_words.
# The words in plain_text and known_words are then compared and the total
# number of similar words between the two lists and outputs the total number.
#
#########################################################################

def grade_message(plaintext,known_words):

    case_plaintext = [x.upper() for x in plaintext]
    case_known_words = [x.upper() for x in known_words]
    similar_words = 0
    for x in case_plaintext:
        for y in case_known_words:
            if x == y:
                similar_words += 1
    return similar_words


#########################################################################
#
# Main code
#
#########################################################################

if __name__ == "__main__":
    main(sys.argv[1:])


