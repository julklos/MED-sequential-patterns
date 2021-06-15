from SequentialPatternAlgorithm import SequentialPatternAlgorithm
import numpy as np
import itertools
from Transaction import Transaction
from ClientSequence import ClientSequence
from timeit import default_timer as timer
import logging

class GSP(SequentialPatternAlgorithm):

    def generate_initial_candidates(self):
        candidates = {}
        for sequence in self._data:
            seq_unique= sequence.get_unique_values()
            for unique in seq_unique:
                if unique in candidates.keys():
                    candidates[unique] += 1
                else:
                    candidates[unique] = 1
        output_candidates = [ClientSequence([[key]], value) for key, value in candidates.items() if value >= self._min_support]
        return output_candidates
    
    def generate_new_candidates (self, freq_pat):
        """
		Given existing patterns, generate a set of new patterns, one longer.
		"""
        # print ("Generating new candidates...")
        pairs = list(itertools.combinations(freq_pat, 2))
        new_candidates = []
        for pair in pairs:
            candidates_ = pair[0].generate_candidates(pair[1])
            for can_ in candidates_:
                if not self.already_created(can_, new_candidates):
                    new_candidates.append(can_)
        for pat in freq_pat:
            candidate_ = pat.generate_candidate()
            for can_ in candidate_:
                if not self.already_created(can_, new_candidates):
                    new_candidates.append(can_)
        new_candidates = [can_ for can_ in new_candidates if not self.already_created(can_, freq_pat)]
        return new_candidates

    def already_created(self, can, freq_pat):
        return any (self.are_equal(pat._items, can._items) for pat in freq_pat)
    def are_equal(self,el1, el2):
        return len(el1) == len(el2) and el1 == el2

    def filter_candidates(self,candidates):
        return [cand for cand in candidates if cand.support(self._data)>= self._min_support]
        
   
    def print_candidates(self,new_candidates):
        for cand_ in new_candidates:
            print(cand_)
    def write_candidates(self, new_candidates):
        output = ""
        for cand_ in new_candidates:
            output += str(cand_)+'\n'
        return output
    
    def run(self):
        logging.info("Algorithm parameters:")
        logging.info("Min support: " +str(self._min_support))
        logging.info("Max length pattern: " + str(self._max_seq_length))
        logging.info("Min length pattern: " + str(self._min_seq_length))
        logging.info("Rows: " + str(len(self._data)))
        logging.info("Start GSP Algorithm...")

        start = timer()

        cand = self.generate_initial_candidates()
        new_patterns  = cand
        self.freq_items = []

        #self.print_candidates(new_patterns)
        ## create this weird loop
        while len(new_patterns):
            self.freq_items += new_patterns
            #print( len(self.freq_items[-1]._items), self._max_seq_length)
            if len(self.freq_items[-1]._items) >= self._max_seq_length:
                break
            candidates = self.generate_new_candidates(self.freq_items)
            new_patterns = self.filter_candidates (candidates)
        if self._min_seq_length:
            self.freq_items = [freq_item for freq_item in self.freq_items if len(freq_item._items) >= self._min_seq_length]
        self._final_sequences = self.freq_items

        stop = timer()
        self._time = stop - start
        logging.info("Stop GSP Algorithm...")
        logging.info("Time:" + str(self._time ))
        output = self._createOutputDicrionary()
        return output
    
    def _createOutputDicrionary(self):  
        output = {}
        parameters = {}
        sequences = {}

        parameters['algorithm'] = 'GSP'
        parameters['min_support'] = self._min_support
        parameters['max_seq_length'] = self._max_seq_length
        parameters['min_seq_length'] = self._min_seq_length

        for i,seq in enumerate(self._final_sequences) :
            s = {}
            s['pattern'] = seq.get_pattern()
            s['support'] = seq.get_value()
            sequences[i] = s

        output['parameters'] = parameters
        output['rows'] = len(self._data)
        output['found_seq'] = len(self._final_sequences)
        output['time'] = self._time
        output['sequences'] = sequences
    
        return output