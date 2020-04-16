""" Processor for .fa files to remove unwanted characters
 and then combine files while maintaining naming """

import pickle

def load_file(filename):
    """ Loads a file by name and returns its contents and length """
    file = open(filename, 'r')
    contents = file.read()
    length = len(contents)
    return (contents, length)


def compress(data, filename):
    pickle.dump( data, open( filename, "wb" ))


def strip_file(filename):
    """ Strips the first line and newline characters from a file """
    data = load_file(filename)
    contents = data[0]
    second_line = contents.find("\n")
    contents = contents[second_line:]
    contents = contents.replace("\n", "")
    return (contents, data[1])


def combine_files(filenames, output_file):
    full_data = []
    names = []
    counter = 0
    for filename in filenames:
        data = strip_file(filename)
        contents = data[0]
        length = data[1]
        full_data.append(contents)
        names.append((filename[5:-3], (counter, counter + length)))
        counter += length
    compress((names, full_data, counter), output_file)
    return (names, full_data, counter)


if __name__ == "__main__":
    combine_files(["Data/alpaca.fa"], "Data/alpaca.p")