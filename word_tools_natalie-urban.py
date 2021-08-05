"""CSCI 1106 Assignment 3: Word Tools

Program: word_tools.py

Author: Natalie Urban

The purpose of this program is to allow the user to input a set of words (both 
manually and via file input) and then to search within that space of words for
single-insertion, single-deletion, single-substitution, and anagram
adjacencies. Further, the user can provide two words and search for a word
ladder (a series of single-substitution steps) that connects them.
"""

import re   
import os.path
import sys

known_words = set()

def main():
    """Takes user input and executes it until receiving the QUIT command."""
    while True:
        user_input = input(">> ")
        tokenized_user_input = user_input.split()
        first_word = tokenized_user_input[0]
        command = first_word.upper()

        if command == "QUIT":
            print("")
            break
        elif command == "LEARNFILE":
            remove_command = tokenized_user_input.pop(0)
            if len(tokenized_user_input) == 1:
                try:
                    os.path.exists(tokenized_user_input[0])
                    learn_file_words(tokenized_user_input[0])
                except FileNotFoundError:
                    print(f'File "{tokenized_user_input[0]}" not found.')
            else:
                print("LEARNFILE requires exactly one filepath.")
        elif command == "LEARN":
            remove_command = tokenized_user_input.pop(0)
            if len(tokenized_user_input) >= 1:
                cap_tokenized_input = [x.upper() for x in tokenized_user_input]
                learn_words(cap_tokenized_input)
            else:
                print("LEARN requires one or more words.")
        elif command == "FORGET":
            remove_command = tokenized_user_input.pop(0)
            if len(tokenized_user_input) >= 1:
                cap_tokenized_input = [x.upper() for x in tokenized_user_input]
                unlearn_words(cap_tokenized_input)
            else:
                print("FORGET requires one or more words.")
        elif command == "EXPLORE":
            remove_command = tokenized_user_input.pop(0)
            if len(tokenized_user_input) == 1:
                cap_tokenized_input = [x.upper() for x in tokenized_user_input]
                explore_word(cap_tokenized_input)
            else:
                print("EXPLORE requires exactly one word.")
        elif command == "LADDER":
            remove_command = tokenized_user_input.pop(0)
            if len(tokenized_user_input) == 3:
                try:
                    first_word = tokenized_user_input[0].upper()
                    second_word = tokenized_user_input[1].upper()
                    max_depth = int(tokenized_user_input[2])
                    find_ladder(first_word, second_word, max_depth)
                except ValueError:
                    print("The third argument to LADDER must be an integer.")
            else:
                print("LADDER requires two words and an integer maximum depth")
        else:
            print(f"I don't know the command \"{command}\".")
            print_help()
            
def print_help():
    """Prints all commands the program's prompt recognizes. Should be called when the user provides an invalid command."""
    print("I understand the following commands:")
    print("QUIT: Exit the program")
    print("LEARNFILE [filepath]: Add every word in the file at [filepath] to my known words.")
    print("LEARN [word] [word] ...: Add one or more specified words to my known words.")
    print("FORGET [word] [word] ...: Remove one or more specified words from my known words.")
    print("EXPLORE [word]: List all known words separated from [word] by one insertion, deletion, substitution, or by rearrangement.")
    print("LADDER [word1] [word2] [max_depth]: Find a word ladder (of length up to max_depth) connecting two words, using only single-letter substitutions.")

def learn_file_words(input_file_path):
    """
    *Opens a file
    *For each line:
        *Uses regex to replace all characters other than letters, apostrophes, and hyphens with a space
        *Splits the line into space-separated tokens
        *Uses isalpha to find the tokens that consist only of letters
        *Adds all these letter-only tokens to a temporary/local set of words found in the file
    *Adds all words found in the file to the list of known words, reporting how many were already known
    """
    input_file = open(input_file_path,'r',encoding='utf-8')
    dict_file = re.sub('[^a-zA-Z\'\-]', " ",input_file.read()).split()
    cap_dict_file = set([x.upper() for x in dict_file])
    new_words = set()
    for x in cap_dict_file:
        if x.isalpha() == True:
            new_words.add(x)
        else:
            pass
    print(f"{len(new_words)} words in {input_file_path}")
    num_words_unknown = []
    for x in new_words:
        if x not in known_words:
            num_words_unknown.append(x)
        else:
            pass
    print(f"{len(num_words_unknown)} previously unknown")
    known_words.update(new_words)

    
def learn_words(new_word_list):
    """Takes in a list of words and either adds each one to the list of known
    words or reports that it's already known."""
    for x in new_word_list:
        if x in known_words:
            print(f'I already know the word "{x}".')
        else:
            known_words.add(x)
            print(f'"{x}" learned.')

def unlearn_words(unwanted_word_list):
    """Takes in a list of words and either removes each one from the list of
    known words or reports that it was already absent."""
    for x in unwanted_word_list:
        if x in known_words:
            known_words.remove(x)
            print(f'"{x}" unlearned.')
        else:
            print(f'I don\'t know the word "{x}"')
        
def substitution_neighbors(search_words):
    """Takes in words and returns the set of all known words that are a single
    letter substitution away from it."""
    for search_word in search_words:
        substituted_words = set()
        for x in range(len(search_word)):
            first_half = search_word[:x]
            last_half = search_word[x+1:]
            for i in [chr(x) for x in range(ord("A"), ord("Z")+1)]:
                sub_word = first_half + i + last_half
                if sub_word in known_words:
                    substituted_words.add(sub_word)
                else:
                    pass
        if search_word in substituted_words:
             substituted_words.remove(search_word)
        else:
            pass
    return substituted_words

def insertion_neighbors(search_words):
    """Takes in words and returns the set of all known words that are a single
    letter insertion away from it."""
    for search_word in search_words:
        insertion_words = set()
        for char in range(len(search_word)+1):
            first_half = search_word[:char]
            last_half = search_word[char:]
            for i in [chr(x) for x in range(ord("A"), ord("Z")+1)]:
                new_word = first_half + i + last_half
                if new_word in known_words:
                    insertion_words.add(new_word)
                else:
                    pass
        if search_word in insertion_words:
             insertion_words.remove(search_word)
        else:
            pass
    return insertion_words

def deletion_neighbors(search_words):
    """Takes in words and returns the set of all known words that are a single
    letter deletion away from it."""
    for search_word in search_words:
        deletion_words = set()
        for char in range(len(search_word)):
            first_half = search_word[:char]
            last_half = search_word[char+1:]
            word = first_half + last_half
            if word in known_words:
                deletion_words.add(word)
            else:
                pass
        if search_word in deletion_words:
             deletion_words.remove(search_word)
        else:
            pass
    return deletion_words
        

def letter_bag(word):
    """Takes in a word and returns a dictionary indicating how many times each
    letter occurs in the word."""
    letter_list = list(word)
    letter_num_dict = {i:letter_list.count(i) for i in letter_list}
    return letter_num_dict
    
def anagrams(search_words):
    """Takes in words and returns the set of all (other) known words that can
    be produced by rearranging its letters. 
    
    Unlike the substitution_neighbors, insertion_neighbors, and deletion_neighbors
    functions, this function does this by searching the space of known words
    for things that happen to have the property of being an anagram of the
    search_word, rather than generating the set of words that have the property
    of being an anagram and then checking to see which ones are known words."""
    for search_word in search_words:
        anagram_words = set()
        for word in known_words:
            if len(word) == len(search_word):
                dict_word = letter_bag(word)
                if dict_word == letter_bag(search_word):
                    anagram_words.add(word)
                else:
                    pass
            else:
                pass   
        if search_word in anagram_words:
             anagram_words.remove(search_word)
        else:
            pass
    return anagram_words

def explore_word(search_word):
    """Takes in a list of a word and, by calling other functions, finds all known words
    which are an insertion, deletion, substitution, or rearrangement away.
    Prints all words in each of these sets."""
    insertions = insertion_neighbors(search_word)
    print("\nInsertions: ")
    for each in insertions:
        print(f"{each}")
    deletions = deletion_neighbors(search_word)
    print("\nDeletions: ")
    for each in deletions:
        print(f"{each}")
    replacements = substitution_neighbors(search_word)
    print("\nReplacements: ")
    for each in replacements:
        print(f"{each}")
    anagram_words = anagrams(search_word)
    print("\nAnagrams: ")
    for each in anagram_words:
        print(f"{each}")
    

def find_ladder(word1,word2,max_depth):
    """Takes in two words and attempts to find and print a "ladder" of
    single-letter substitutions that connects the two through the space
    of known words. Stops after finding minimum-length paths or after not
    finding any paths of length max_depth or less."""
    paths1 = [[word1]]
    paths2 = [[word2]]
    
    full_paths = _find_paths(paths1,paths2,max_depth)
    print(f"Ladders {word1}>{word2}")
    for path in full_paths:
        print(">".join(path))


def _find_paths(paths1,paths2,max_depth,words_traversed1=set(),words_traversed2=set(),depth=0):
    """Helper function for find_ladder."""
    full_paths = []
    for path1 in paths1:
        for path2 in paths2:
            if path1[-1] == path2[-1]:
                full_paths.append(path1 + path2[::-1][1:])
    if len(full_paths) > 0:
        return full_paths
    
    if depth > max_depth:
        return []
    
    print(f"Expanding to depth {depth}")
    
    if depth % 2 == 0:
        selected_paths = paths1
        selected_words_traversed = words_traversed1
    else:
        selected_paths = paths2
        selected_words_traversed = words_traversed2
    
    new_paths = []
    new_words_traversed = set()
    for path in selected_paths:
        lastWord = [path[-1]]
        for adjacent_word in substitution_neighbors(lastWord) - selected_words_traversed:
            new_paths.append(path + [adjacent_word])
            new_words_traversed.add(adjacent_word)
    
    if depth % 2 == 0:
        paths1 = new_paths
        words_traversed1 = words_traversed1 | new_words_traversed
    else:
        paths2 = new_paths
        words_traversed2 = words_traversed2 | new_words_traversed
    
    return _find_paths(paths1,paths2,max_depth,words_traversed1,words_traversed2,depth+1)
    

if __name__ == "__main__":
    main()

