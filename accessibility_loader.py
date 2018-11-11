import sys

def loadDicts(file_name ='data/Accessiblity-Rankings.txt'):
    '''
    Loads two dictionaries, each mapping words to one type of retrievability metric
    KF_frequency is the number of occurances in a text sample and was created by Kucera & Francis (1967).
    Accessibility index is the number of times of cues for which the target was produced at least once
    :param file: The location of the file containing the data
    :return: two dictionaries: the first mapping words to their kf_frequencies and
     the second mapping words to their accessibility_indices
    '''

    kf_frequencies = {}
    accessibility_indices = {}
    file = open(file_name, 'r')
    file.readline() # get rid of the header line

    for line in file:
        line_data = line.split(',')
        line_data[0] = line_data[0].lower()
        line_data[1] = int(line_data[1])
        line_data[2] = int(line_data[2])

        if not line_data[1] == 0:
            kf_frequencies[line_data[0]] = line_data[1]
        accessibility_indices[line_data[0]] = line_data[2]

    return kf_frequencies, accessibility_indices

if __name__ == "__main__":
    ks_freq, accessibilty = loadDicts()
    pickle.dump(ks_freq, )