""" Creates a dictionary of all possible words in a dataset and their positions """

import pickle
import sys

def load_file(filename):
    """ Loads a compressed file and returns its contents"""
    data = pickle.load( open( filename, "rb" ) )
    return data


def compress(data, filename):
    pickle.dump( data, open( filename, "wb" ))


def create_dict(filename, out_file):
    data = load_file(filename)
    sequence = data[1][0]
    names = data[0]
    length = data[2]
    word_length = 11; # The length of a word

    dictionary = {}
    for i in range(len(sequence)-10):
        if i%100000 == 0:
            sys.stdout.write("\r" + str(i) + " of " + str(length) + "    " + str(i/length*100) + "%")
            sys.stdout.flush()

        word = sequence[i:i+11]
        
        if word in dictionary:
            dictionary[word].append(i)
        else:
            dictionary[word] = [i]

    compress((names, dictionary), out_file)
    return (names, dictionary)


if __name__ == "__main__":
    create_dict("Data/alpaca.p", "Data/alpaca_dictionary.p")




