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
    

def sequence_allignment(input_seq, sequences):
    """
    Run smith-waterman on input_seq and each of the sequences 
    """

    output = []
    for sequence in sequences:
        output.append(smith_waterman(input_seq, sequence))

def smith_waterman(input_seq, seq):
    """
        Determine the substitution matrix and the gap penalty scheme.
        s ( a , b )  - Similarity score of the elements that constituted the two sequences
        W k- The penalty of a gap that has length k {\displaystyle k} k
        Construct a scoring matrix H  H and initialize its first row and first column. The size of the scoring matrix is ( n + 1 ) ∗ ( m + 1 ). The matrix uses 0-based indexing.

        H k 0 = H 0 l = 0 f o r 0 ≤ k ≤ n a n d 0 ≤ l ≤ m 

    Fill the scoring matrix using the equation below.

        H i j = max { H i − 1 , j − 1 + s ( a i , b j ) , max k ≥ 1 , max l ≥ 1  , 0 ( 1 ≤ i ≤ n , 1 ≤ j ≤ m )
        where
        H i − 1 , j − 1 + s ( a i , b j ) is the score of aligning a i  and b j {\displaystyle b_{j}} b_{j},
        H i − k , j − W k  is the score if a i  is at the end of a gap of length k  k,
        H i , j − l − W l  is the score if b j  is at the end of a gap of length l {\displaystyle l} l,
        0 {\displaystyle 0} {\displaystyle 0} means there is no similarity up to a i {\displaystyle a_{i}} a_{i} and b j {\displaystyle b_{j}} b_{j}.

    Traceback. Starting at the highest score in the scoring matrix H {\displaystyle H} H and ending at a matrix cell that has a score of 0, traceback based on the source of each score recursively to generate the best local alignment.
    """

    gap_penalty = 3

    if len(input_seq) == 0 or len(seq) == 0:
        return 0

    return max(smith_waterman(input_seq[:-1], seq[:-1]) + (1 if input_seq[-1]==seq[-1] else -1), \
        smith_waterman(input_seq[:-1], seq)-gap_penalty, \
        smith_waterman(input_seq, seq[:-1])-gap_penalty, \
        0)


def blast(input_seq, data_filename, dict_filename):
    words = create_list_of_words(input_seq)
    positions = create_positions_list(words, data_filename)
    sequences = find_possible_sequences(data_filename, positions, 2*len(input_seq))
    sequence_allignment(input_seq, sequences)

# Test Functions

### Test Functions for createListofWords

### Test Functions for createPositionsList



if __name__ == "__main__":
    # print(find_possible_sequences("Utils/Data/yeast.txt", [1000, 4000], 20))
    # print(find_possible_sequences("Utils/Data/yeast.txt", create_positions_list(create_list_of_words("ttactgttaatggtttgttcaataccg"), "Utils/Data/yeast_dictionary.p"), 40))
    print(smith_waterman("hello", "hell o"))