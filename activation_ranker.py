"""

"""

import numpy as np
import sys

def pageRank(matrixFile, alpha=.85, epsilon=np.exp(-8), out=sys.stdout):
    """
    Evaluates all entries of a square, stochastic nparray using Google's PageRank
    Uses a random surfer paradigm
    Returns an array of PageRank importance rankings (floats) in the preserved order
    :param matrixFile: name of .pickle file storing the nparray
    :param alpha: probability that surfer will follow link, not hyperlink; default is .85, last given value by Google
    :param weighted: whether the entries of the nparray are weighted or even; defaults to even
    :param out: the print stream to write status messages to; defaults to sys.stdout: set to os.devnull to suppress
    :returns: 1-dimensional array of PageRank importance rankings
    """
    print("Loading matrix from '{0}'...".format(matrixFile), file=out)
    matrix = np.load(matrixFile) # currently in stochastic matrix (S) form
    print("Executing Google matrix transform with alpha value {0:f}...".format(alpha), file=out)
    n = len(matrix) # length of side of square matrix; stored for computational intelligibility
    # introduce random surfer to make dense Google matrix: afterward, in Google matrix (G) form
    ERatio = (1. - alpha) * (1. / n) # chance that any surfer will teleport to any page, randomly
    for i in range(n): # through columns of S
        for j in range(n): # through rows of S
            matrix[i][j] = (alpha * matrix[i][j]) + ERatio # introduce hyperlink chance
    
    print("Iterating using power rule on Google matrix...", file=out)
    pi = (1. / n) * np.ones((1, n), dtype=float) # initialize iterating ranking row vector pi
    residual = 1. # change in pi after iteration; iteration will finish when residual < epsilon
    k = 0 # number of iterations, used for status message
    while (residual >= epsilon):
        prevpi = pi
        k += 1
        pi = np.matmul(pi, matrix) # apply one iteration of power rule
        residual = np.linalg.norm(np.subtract(prevpi, pi)) # residual is norm of difference of vectors
    
    print("PageRank ranking complete; {0:d} iterations applied.".format(k), file=out)
    return pi[0] # pi has a 1-layer outer array for matrix multiplication; relevant array is pi[0]

def hypertextInducedTopicSearch(matrixFile, xi=.85, epsilon=np.exp(-8), out=sys.stdout):
    print("Loading matrix from '{0}'...".format(matrixFile), file=out)
    matrix = np.load(matrixFile) # currently in stochastic matrix form
    n = len(matrix) # length of side of square matrix; stored for computational intelligibility
    print("Generating authority and hub matrices...", file=out)
    L = matrix.astype(int) # binary form of matrix, labeled L mathematically
    transL = np.matrix.transpose(L) # transpose form of L, labeled L^T mathematically
    authMatrix = (transL @ L).astype(float)
    hubMatrix = (L @ transL).astype(float)
    print("Executing Google matrix transform to authority and hub matrices with xi value {0:f}...".format(xi), file=out)
    # introduce random surfer to simulate dense matrix, as in Google matrix
    ERatio = (1. - xi) * (1. / n) # chance that any surfer will teleport to any page, randomly; will be used in iteration
    for i in range(n): # through columns of L^T L
        for j in range(n): # through rows of L L^T
            authMatrix[i][j] = xi * authMatrix[i][j] # reduce by hyperlink chance in authority matrix
            hubMatrix[i][j] = xi * hubMatrix[i][j] # reduce by hyperlink chance in hub matrix
    print("Iterating using power rule on authority and hub matrices...", file=out)
    x = (1. / n) * np.ones((1, n), dtype=float) # initialize iterating authority ranking row vector x
    y = (1. / n) * np.ones((1, n), dtype=float) # initialize iterating hub ranking row vector y
    residual = 1. # change in pi after iteration; iteration will finish when residual < epsilon
    k = 0 # number of iterations, used for status message
    while (residual >= epsilon):
        prevx = x
        prevy = y
        k += 1
        x = np.matmul(authMatrix, x) + ERatio # apply one iteration of power rule to authority matrix
        y = np.matmul(hubMatrix, y) + ERatio # apply one iteration of power rule to hub matrix
        # residual is average norm of difference of vectors
        residual = (np.linalg.norm(np.subtract(prevx, x)) + np.linalg.norm(np.subtract(prevy, y))) * .5
    
    print("HITS ranking complete; {0:d} iterations applied.".format(k), file=out)
    return x[0], y[0] # x and y have a 1-layer outer array for matrix multiplication
    
    