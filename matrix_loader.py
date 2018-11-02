"""
Loads associations into memory. Can be used to create both weighted and
unweighted matrices without and with unnormed targets.
"""

import numpy as np

def load(fileName):
    """
    Loads an input file for cue-target pairs
    The input file must be of the format used by Nelson et al.--
    a CSV (.txt or .csv) where every line follows the following format: 
        CUE, TARGET, NORMED?, #G, #P, ...
    (more beyond the ellipsis is allowed but will not be used)
    Returns the data of the cue-target pairs in a tuple: see below
    for details
    :param fileName: a string directory of the data file;
                     see http://w3.usf.edu/FreeAssociation/AppendixA/
    :returns: tuple of len 3:
        [0] a dictionary mapping cues to targets;
            key is string, value is tuple of len 3:
                [0] target as string
                [1] forward strength as float
                [2] normed as boolean
        [1] a list enumerating all normed words in data;
            sorted alphabetically A-Z
        [2] a list enumerating all unnormed words in data;
            sorted alphabetically A-Z
    """
    assocs = dict()
    normed_list = []
    unnormed_list = []
    assoc_file = open(fileName)

    print("Loading cue-target pairs from file: '{0}'".format(fileName))
    i = 1
    for line in assoc_file:
        line_data = line.split(',')
        if len(line_data) < 5 or not line_data[3].strip().isdigit() or not line_data[4].strip().isdigit():
            print("...Line {0} failed to load...".format(i))
            continue
        # Load data fields 1, 2, 3, 4 and 5 (see above; or USF free association norms: appendix A)
        cue = line_data[0].strip()
        target = line_data[1].strip()
        normed = True if line_data[2].strip() == "YES" else False
        fsg = int(line_data[4].strip()) / int(line_data[3].strip())
        # Add the data into self.assocs and the lists self.normed_items and self.unnormed_items
        if len(normed_list) == 0 or normed_list[-1] != cue: # Data should be alphabetical by cue; identical cues should be adjacent
            normed_list.append(cue)
        if not normed and target not in unnormed_list:
            unnormed_list.append(target)
        assocs.setdefault(cue, [])
        assocs[cue].append((target, fsg, normed)) # assocs dict values are tuples of these 3
        # Status messages; comment out if undesired
        if i % 10000 == 0:
            print("...{0} cue-target lines parsed...".format(i))
        i += 1
    unnormed_list = np.sort(unnormed_list)
    print("Load complete: {0} cue-target lines parsed, yielding {1} total cues".format(i, len(assocs)))
    
    return assocs, normed_list, unnormed_list

def createNormedBooleanMatrix(dict, normed_list, fileName="lib/normedBooleanMatrix.pickle"):
    """
    Creates an nxn matrix where n is the number of cues and writes it to the given location
    The i,jth entry is 1 iff people produced target j when given cue i
    Only considers normed targets (targets that were tested as cues)
    Pickles the matrix and writes it to the given file
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param fileName: the name of the file to write the pickled matrix to
    """
    matrix = np.zeros((len(normed_list), len(normed_list)), dtype=bool)
    for i in len(normed_list):
        for target in dict[normed_list[i]]:
            if target[2]:  # the target was normed
                matrix[i][normed_list.index(target[0])] = True
    file = open(fileName,'w')
    matrix.dump(file)
    
def createNormedStochaticMatrix(dict, normed_list, fileName="lib/normedStochasticMatrix.pickle"):
    """
    Creates an nxn matrix where n is the number of cues and writes it to the given location
    The i,jth entry is the fraction of the time people produced target j when given cue i
    Only considers normed targets (targets that were tested as cues)
    Pickles the matrix and writes it to the given file
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param fileName: the name of the file to write the pickled matrix to
    """
    matrix = np.zeros((len(normed_list), len(normed_list)), dtype=float)
    for i in len(normed_list):
        for target in dict[normed_list[i]]:
            if target[2]:  # the target was normed
                matrix[i][normed_list.index(target[0])] = target[1]

    # normalizes the entries of each row to sum to 1 to make it a stochastic matrix
    for row in matrix:
        sum = 0
        for col in row:
            sum += col
        for col in row:
            col = col / sum

    file = open(fileName,'w')
    matrix.dump(file)

def createFullBooleanMatrix(dict, normed_list, unnormed_list, fileName="lib/fullBooleanMatrix.pickle"):
    """
    Creates an n+m square matrix where n and m are the length of the normed and unnormed lists
    The i,jth entry is 1 iff people produced target j when given cue i
    Pickles the matrix and writes it to the given file
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param unnormed_list: a list of the responses produced that were never given as cues
    :param fileName: the name of the file to write the pickled matrix to
    """
    matrix = np.zeros((len(normed_list) + len(unnormed_list), len(normed_list) + len(unnormed_list)), dtype=float)
    for i in len(normed_list):
        for target in dict[normed_list[i]]:
            if target[2]:  # target is normed
                matrix[i][normed_list.index(target[0])] = True
            else:  # target not normed
                matrix[i][len(normed_list) + unnormed_list.index(target[0])] = True

    # give unnormed cues edges to every target
    for i in range(len(unnormed_list)):
        for j in range(len(normed_list) + len(unnormed_list)):
            if not i == j :  # node shouldn't have an out-edge to itself
                matrix[len(normed_list)][j] = True

    file = open(fileName,'w')
    matrix.dump(file)

def createFullStochasticMatrix(dict, normed_list, unnormed_list, fileName="lib/fullStochasticMatrix.pickle"):
    """
    Creates an n+m square matrix where n and m are the length of the normed and unnormed lists
    The i,jth entry is the fraction of the time people produced target j when given cue i
    Pickles the matrix and writes it to the given file
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param unnormed_list: a list of the responses produced that were never given as cues
    :param fileName: the name of the file to write the pickled matrix to
    """
    matrix = np.zeros((len(normed_list) + len(unnormed_list), len(normed_list) + len(unnormed_list)), dtype=float)
    for i in len(normed_list):
        for target in dict[normed_list[i]]:
            if target[2]:  # target is normed
                matrix[i][normed_list.index(target[0])] = target[1]
            else:  # target not normed
                matrix[i][len(normed_list) + unnormed_list.index(target[0])] = target[1]

    # give unnormed cues edges to every target. Weights will later be normalized to sum to 1
    for i in range(len(unnormed_list)):
        for j in range(len(normed_list) + len(unnormed_list)):
            if not i == j:  # node shouldn't have an out-edge to itself
                matrix[len(normed_list)][j] = 1

    # normalizes the entries of each row to sum to 1 to make it a stochastic matrix
    for row in matrix:
        sum = 0
        for col in row:
            sum += col
        for col in row:
            col = col / sum

    file = open(fileName,'w')
    matrix.dump(file)


