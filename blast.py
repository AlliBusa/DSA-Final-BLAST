"""
Note: the code and pseudocode written in the .py file are assuming that there is a dictionary
which contains all of the unique words in the database, and the positions where
they appear in the database


The blast algorithm is made from a sequence of steps, denoted below:
-take the input query (DNA, for now) and create a list of words from it

-take all those words, and create a nested list that contains all of the positions of all of the
    words in the query, that are in the database

-take those positions of the words in the database, and experiment with shifting them back and
    forth, in order to get the best sequence to put in the Smith-Waterman algorithm

-run the Smith-Waterman algorithm and receive seeds

-input the seeds in a DP minimum edit distance algorithm, that compares it with the
    original input sequence

-return the top five minimum edit distance seeds, or the seeds in increasing order of
    edit distance, or something else TBD


"""
import pickle
import numpy as np
import time
from copy import deepcopy
import pandas as pd
from tabulate import tabulate

#from colinscode import databasedict

def load_text_file(filename):
    """ Loads a text file and returns a file pointer"""
    f = open(filename, 'r')
    return f

def load_file(filename):
    """ Loads a compressed file and returns its contents"""
    data = pickle.load(open(filename, "rb"))
    return data

def create_list_of_words(input_seq):
    """
    takes the input sequence, and returns all of the possible words from it
    as of now, we're only looking at DNA, so words are 11 bases long

    input_seq : sequence that the user inputs, given as a string

    returns input_words, list of words in input sequence
    """

    #checking that input string is correct
    assert len(input_seq) >= 11, "input string too small"

    #if there's only one word
    if len(input_seq) == 11:
        return [input_seq]
    #else
    input_words = []
    for i in range(len(input_seq)-10):
        input_words.append(input_seq[i:i+11])
    return input_words

def create_positions_list(input_words, database_file_name):
    """
    takes in a list of words in input sequence and the dictionary of the data
    returns a nested list of all the positions of the words in the database

    input_words: list of words in input_seq
    databasedict: dictionary that contains all unique words in the database
        and the positions where they occur

    returns position_list, nested list
    """
    (names, databasedict) = load_file(database_file_name)

    position_list = [] #output list
    #find the corresponding positions for each word
    for word in input_words:
        if word in databasedict: #make sure the word is there
            position_list.extend(databasedict[word])
    return position_list

def find_possible_sequences(source_file_name, positions, seq_len):
    """ Takes a source file and a list of positions in that file and
        returns a list of sequences that have the length seq_len and
        center at the position """

    f = load_text_file(source_file_name)
    sequences = []

    for position in positions:
        f.seek(position - seq_len // 2)
        sequences.append(f.read(seq_len))

    return sequences


def sequence_alignment(input_seq, sequences):
    """
    Run smith-waterman on input_seq and each of the sequences
    """

    output = []
    for sequence in sequences:
        _, cost = smith_waterman(input_seq, sequence)
        output.append((sequence, cost))
    #sort by best
    output.sort(key=lambda tup: tup[1], reversed=True)
    return output

def sw_scoring(s1,s2, DP, TM, gap_penalty = 3, match = 1, mismatch = -1):
    """
    Implementing the scoring matrix part of the smith waterman algorithm, currently being used as helper function for smith_waterman function below

    Takes in the input sequence and seq strings, and returns their scoring matrix and traceback matrix

    In this case, the scoring matrix keeps track of what move was needed to land on a particular spot in the scoring matrix. This will be used for traceback later

    The scoring parameters are gap_penalty, match and mismatch. These can be changed by the user

    s1: input_seq
    s2: seq
    DP: initialized scoring matrix
    TM: initialized traceback matrix

    returns last value, but also updates matrices globally
    """
    if np.isnan(DP[len(s1),len(s2)]) != True:
        return DP[len(s1),len(s2)] , TM[len(s1),len(s2)]

    if len(s1) == 0 or len(s2) == 0:
        #print("s1, s2", s1,s2)
        return 0, 0

    val1, _ = sw_scoring(s1[:-1], s2[:-1], DP, TM)
    val1 = val1 + (match if s1[-1]==s2[-1] else mismatch) #diag 1
    val2,  _ = sw_scoring(s1[:-1], s2, DP, TM) #left 2
    val2 = val2 -gap_penalty
    val3, _ = sw_scoring(s1, s2[:-1], DP, TM) #top 3
    val3= val3 -gap_penalty
    vals = [0, val1, val2, val3]
    TM[len(s1),len(s2)] = np.argmax(vals)
    DP[len(s1),len(s2)] = max(vals)
    return DP[len(s1),len(s2)], TM[len(s1),len(s2)]


def smith_waterman(s1, s2, DP, TM):
    """
    Implementing the traceback part of the smith-waterman algorithm

    Returns the best substrings and the total cost
    """
    sw_scoring(s1,s2, DP, TM) #fill the matrices
    pointer = np.unravel_index(np.nanargmax(DP, axis=None), DP.shape) #find the max value
    best = DP[pointer] #create pointer to max value
    #initialize final strings
    subs1 = ""
    subs2 = ""
    subs1 += s1[pointer[0]-1]
    subs2 += s2[pointer[1]-1]
    #while the end of an input string isn't reached
    while np.isnan(TM[pointer]) != True or TM[pointer] != 0:
    #check which direction it came from

        #diag
        if TM[pointer] == 1:
            pointer = (pointer[0]-1, pointer[1]-1)
            if np.isnan(TM[pointer]) == True or TM[pointer] == 0:
                break
            a1 = s1[pointer[0]-1]
            a2 = s2[pointer[1]-1]

        #left
        elif TM[pointer] == 2:
            pointer = (pointer[0], pointer[1]-1)
            if np.isnan(TM[pointer]) == True or TM[pointer] == 0:
                break
            a1 = "-"
            a2 = s2[pointer[1]-1]
        #top
        else:
            pointer = (pointer[0], pointer[1]-1)
            if np.isnan(TM[pointer]) == True or TM[pointer] == 0:
                break
            a1 = "-"
            a2 = s2[pointer[1]-1]
        #append new values to final strings
        subs1 += a1
        subs2 += a2

    #return final substrings reversed
    subs1 = subs1[::-1]
    subs2 = subs2[::-1]
    return subs1, subs2, best


def blast(input_seq, data_filename, dict_filename):
    words = create_list_of_words(input_seq)
    positions = create_positions_list(words, data_filename)
    sequences = find_possible_sequences(data_filename, positions, 2*len(input_seq))
    output_list = sequence_alignment(input_seq, sequences)

    return output_list

# Test Functions

### Test Functions for createListofWords

### Test Functions for createPositionsList



if __name__ == "__main__":
    # print(find_possible_sequences("Utils/Data/yeast.txt", [1000, 4000], 20))
    # print(find_possible_sequences("Utils/Data/yeast.txt", create_positions_list(create_list_of_words("ttactgttaatggtttgttcaataccg"), "Utils/Data/yeast_dictionary.p"), 40))
    #print(smith_waterman("hello", "hell o"))
    #print(blast(input_seq = "gttggtgcacgtggagcctcaac", "Utils/Data/yeast.txt", "Utils/Data/yeast_dictionary.p"))
