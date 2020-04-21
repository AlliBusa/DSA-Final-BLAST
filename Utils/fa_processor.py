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
    """ Compresses arbitrary data structure into binary file """
    pickle.dump(data, open(filename, "wb"))

def save_text(data, filename):
    """ Compresses arbitrary data structure into binary file """
    f = open(filename, 'w')
    for i in data:
        f.write(i)
    f.close()


def strip_file(filename):
    """ Strips the first line and newline characters from a file """
    data = load_file(filename)
    contents = data[0]
    second_line = contents.find("\n")
    contents = contents[second_line:]
    contents = contents.replace("\n", "")
    return (contents, data[1])


def combine_files(filenames, output_file, output_text_file):
    """ Concatenates files and creates a list of names of the creatures they came from """
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
    save_text(full_data, output_text_file)
    return (names, full_data, counter)


if __name__ == "__main__":
    combine_files(["Data/yeast.fa"], "Data/yeast.p", "Data/yeast.txt")