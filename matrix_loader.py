"""
Loads associations into memory. Will create an association matrix
when initialized with a file of the correct type. Directed graphs
from individual data points can then be requested.
"""

import numpy

class AssociationMatrix:
    def __init__(self, filename):
        assoc_file = open(filename)
        self.items = []
        assocs = None # TODO: decide target format
        for line in assoc_file:
            # TODO: decide target format
            pass
        self.matrix = matrix_from_???(assocs)
    
    def get_dir_graph(self, cue):
        '''
        Returns a directed graph formed around a cue in
        the items of the matrix.
        '''
        cue_index = self.items.indexof(cue)
        graph = None 
        # TODO: I need to look up how to do graphs in Python; I forgot
        
        return graph
