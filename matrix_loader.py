"""
Loads associations into memory. Can be used to create both weighted and
unweighted matrices without and with unnormed targets.

WARNING: When generating matrices with large sets of data, be aware that the pickled
files saved will be quite large (n=70000 correlates to ~1GB). This also means that when
loaded, these matrices will occupy a considerable portion of RAM.
"""

import sys
import numpy as np

def load(fileName, out=sys.stdout):
    """
    Loads an input file for cue-target pairs
    The input file must be of the format used by Nelson et al.--
    a CSV (.txt or .csv) where every line follows the following format:
        CUE, TARGET, NORMED?, #G, #P, ...
    (more beyond the ellipsis is allowed but will not be used)
    Returns the data of the cue-target pairs in a tuple: see below
    for details
    :param fileName: a string directory of the data file; see http://w3.usf.edu/FreeAssociation/AppendixA/
    :param out: the print stream to write status messages to; defaults to sys.stdout: set to os.devnull to suppress
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

    print("Loading cue-target pairs from file: '{0}'".format(fileName), file=out)
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
        # Status messages for milestones
        if i % 10000 == 0:
            print("...{0} cue-target lines parsed...".format(i), file=out)
        i += 1
    unnormed_list.sort()
    print("Load complete: {0} cue-target lines parsed, yielding {1} total cues".format(i, len(assocs)), file=out)
    
    return assocs, normed_list, unnormed_list

def createNormedUnweightedMatrix(dict, normed_list, fileName="lib/normedUnweightedMatrix.pickle", out=sys.stdout):
    """
    Creates an nxn matrix where n is the number of cues and writes it to the given location
    The i,jth entry is 1./out-links iff people produced target j when given cue i
    Only considers normed targets (targets that were tested as cues)
    Pickles the matrix and writes it to the given file, or a default
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param fileName: the name of the file to write the pickled matrix to; has default
    :param out: the print stream to write status messages to; defaults to sys.stdout: set to os.devnull to suppress
    :returns: the name of the file holding the pickle (see param fileName)
    """
    print("Generating closed unweighted association matrix", file=out)
    matrix = np.zeros((len(normed_list), len(normed_list)), dtype=float)
    print("...Creating out-links for normed items...")
    for i in range(len(normed_list)):
        for target in dict[normed_list[i]]:
            if target[2]:  # the target was normed
                matrix[i][normed_list.index(target[0])] = 1.
    print("...Re-weighting out-links for all items...", file=out)
    makeStochastic(matrix)
    print("Matrix generated: compressing to '{0}'".format(fileName), file=out)
    matrix.dump(fileName)
    # return name of pickle file; mostly for if default was used
    return fileName
    
def createNormedWeightedMatrix(dict, normed_list, fileName="lib/normedWeightedMatrix.pickle", out=sys.stdout):
    """
    Creates an nxn matrix where n is the number of cues and writes it to the given location
    The i,jth entry is the fraction of the time people produced target j when given cue i
    Only considers normed targets (targets that were tested as cues)
    Pickles the matrix and writes it to the given file, or a default
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param fileName: the name of the file to write the pickled matrix to; has default
    :param out: the print stream to write status messages to; defaults to sys.stdout: set to os.devnull to suppress
    :returns: the name of the file holding the pickle (see param fileName)
    """
    print("Generating closed weighted association matrix", file=out)
    matrix = np.zeros((len(normed_list), len(normed_list)), dtype=float)
    print("...Creating out-links for normed items...")
    for i in range(len(normed_list)):
        for target in dict[normed_list[i]]:
            if target[2]:  # the target was normed
                matrix[i][normed_list.index(target[0])] = target[1]
    print("...Re-weighting out-links for all items...", file=out)
    makeStochastic(matrix)
    print("Matrix generated: compressing to '{0}'".format(fileName), file=out)
    matrix.dump(fileName)
    # return name of pickle file; mostly for if default was used
    return fileName

def createFullUnweightedMatrix(dict, normed_list, unnormed_list, fileName="lib/fullUnweightedMatrix.pickle", out=sys.stdout):
    """
    Creates an n+m square matrix where n and m are the length of the normed and unnormed lists
    The i,jth entry is 1./out-links iff people produced target j when given cue i
    Pickles the matrix and writes it to the given file, or a default
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param unnormed_list: a list of the responses produced that were never given as cues
    :param fileName: the name of the file to write the pickled matrix to; has default
    :param out: the print stream to write status messages to; defaults to sys.stdout: set to os.devnull to suppress
    :returns: the name of the file holding the pickle (see param fileName)
    """
    print("Generating full unweighted association matrix", file=out)
    matrix = np.zeros((len(normed_list) + len(unnormed_list), len(normed_list) + len(unnormed_list)), dtype=float)
    print("...Creating out-links for normed items...", file=out)
    for i in range(len(normed_list)):
        for target in dict[normed_list[i]]:
            if target[2]:  # target is normed
                matrix[i][normed_list.index(target[0])] = 1.
            else:  # target not normed
                matrix[i][len(normed_list) + unnormed_list.index(target[0])] = 1.
    print("...Re-weighting out-links for all items...", file=out)
    makeStochastic(matrix)
    print("Matrix generated: compressing to '{0}'".format(fileName), file=out)
    matrix.dump(fileName)
    # return name of pickle file; mostly for if default was used
    return fileName

def createFullWeightedMatrix(dict, normed_list, unnormed_list, fileName="lib/fullWeightedMatrix.pickle", out=sys.stdout):
    """
    Creates an n+m square matrix where n and m are the length of the normed and unnormed lists
    The i,jth entry is the fraction of the time people produced target j when given cue i
    Pickles the matrix and writes it to the given file, or a default
    :param dict: a dictionary mapping cues to 3-d tuples: the target word, the association strength, and whether the target is normed
    :param normed_list: a list of the cues
    :param unnormed_list: a list of the responses produced that were never given as cues
    :param fileName: the name of the file to write the pickled matrix to; has default
    :param out: the print stream to write status messages to; defaults to sys.stdout: set to os.devnull to suppress
    :returns: the name of the file holding the pickle (see param fileName)
    """
    print("Generating full weighted association matrix", file=out)
    matrix = np.zeros((len(normed_list) + len(unnormed_list), len(normed_list) + len(unnormed_list)), dtype=float)
    print("...Creating out-links for normed items...", file=out)
    for i in range(len(normed_list)):
        for target in dict[normed_list[i]]:
            if target[2]:  # target is normed
                matrix[i][normed_list.index(target[0])] = target[1]
            else:  # target not normed
                matrix[i][len(normed_list) + unnormed_list.index(target[0])] = target[1]
    print("...Re-weighting out-links for all items...", file=out)
    makeStochastic(matrix)
    print("Matrix generated: compressing to '{0}'".format(fileName), file=out)
    matrix.dump(fileName)
    # return name of pickle file; mostly for if default was used
    return fileName

def makeStochastic(matrix):
    """
    Given an ndarray matrix, re-weights all items in the matrix so that each row
    sums to 1.
    """
    # normalizes the entries of each row to sum to 1 to make it a stochastic matrix
    for i in range(len(matrix)):
        total = sum(matrix[i])
        for j in range(len(matrix)):
            if total == 0.: # no out-links: make fully regular out-links
                if i != j: # node shouldn't have an out-edge to itself
                    matrix[i][j] = 1. / (len(matrix) - 1)
            else:
                matrix[i][j] = matrix[i][j] / total
