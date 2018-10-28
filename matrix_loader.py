"""
Loads associations into memory. Can be used to create both weighted and
unweighted matrices without and with unnormed targets.
"""

import numpy as np

class AssociationMatrix:
    def __init__(self):
        '''
        '''
        self.assocs = dict() # dict mapping string cues to lists of tuples: (string target, float strengths, bool normed)
        self.normed_items = [] # enumerating list of string normed words
        self.unnormed_items = [] # enumerating list of string unnormed words
        self.matrix = None # matrix of relations, indices match from items
        
    def load(filename):
        '''
        '''
        self.assocs.clear()
        self.items.clear()
        assoc_file = open(filename)
        
        printf("Loading cue-target pairs from file: '{0}'", filename)
        int i = 1
        for line in assoc_file:
            line_data = line.split(',')
            if len(line_data) < 5:
                printf("EXCEPTION: Line {0} failed to load", i)
            # Load data fields 1, 2, 3, 4 and 5 (see USF free association norms: appendix A)
            cue, target = line_data[0].strip(), line_data[1].strip(), line_data[2].strip()
            normed = true if normed == "YES" else false
            fsg = float(line_data[4].strip()) / float(line_data[3].strip())
            # Add the data into self.assocs and the lists self.normed_items and self.unnormed_items
            self.normed_items.add(cue)
            if not normed:
                self.unnormed_items.add(target)
            target_list = self.assocs.setdefault(cue, [])
            self.assocs[cue] = target_list.add(tuple(target, fsg, normed))
            # Status messages; comment out if undesired
            if i % 10000 == 0:
                printf("...{0} cue-target lines parsed...", i)
            i += 1
        np.sort(self.unnormed_items)
        printf("Load complete: {0} cue-target lines parsed, yielding {1} total cues", i, len(self.assocs))
    
    def init_matrix(self):
        '''
        '''
        self.matrix = np.zeros(tuple())
        
