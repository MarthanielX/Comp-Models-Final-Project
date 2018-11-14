import collections

def load_data(file_name="data/ExperimentalData.csv"):
    '''
    Loads in experimental data from the file and uses it to create a dict of dicts.
    The outer dictionary maps letters to dictionaries
    Each inner dict maps words starting with that letter to the number of occurrences of the word

    :param file_name: The location  of the file to be loaded from
    :return: the outer dictionary
    '''

    frequencies_dict = {}
    file = open(file_name, 'r')

    # Make an emtpy dict for each word in the header (each word tested)
    letters = file.readline().split(",")
    for letter in letters:
        frequencies_dict[letter] = {}

    for l in file:
        line = l.rstrip()  # remove trailing \r\n
        line = line.split(",")
        for word in line:
            word = word.upper()
            # get frequency the word maps to; either increment it or initialize to 1
            frequencies_dict[word[0]][word] = frequencies_dict[word[0]].get(word, 0) + 1

    return frequencies_dict


def load_data_no_repeats(file_name="data/ExperimentalData.csv"):
    '''
    Loads in experimental data from the file and uses it to create a dict of dicts.
    The outer dictionary maps letters to dictionaries
    Each inner dict maps words starting with that letter to the number of occurrences of the word
    When a participant produces the same word twice, we only count it once

    :param file_name: The location  of the file to be loaded from
    :return: the outer dictionary
    '''

    frequencies_dict = {}
    file = open(file_name, 'r')

    # Make an emtpy dict for each word in the header (each word tested)
    letters = file.readline().split(",")
    for letter in letters:
        frequencies_dict[letter] = {}

    for l in file:
        line = l.rstrip()  # remove trailing \r\n
        line = line.split(",")
        counter = collections.Counter(line)
        for item in counter.items():
            if item[1] == 2:
                line.remove(item[0])

        for word in line:
            word = word.upper()
            # get frequency the word maps to; either increment it or initialize to 1
            frequencies_dict[word[0]][word] = frequencies_dict[word[0]].get(word, 0) + 1

    return frequencies_dict
