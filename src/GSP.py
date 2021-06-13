from SequentialPatternAlgorithm import SequentialPatternAlgorithm
import numpy as np
import itertools
from Transaction import Transaction
from ClientSequence import ClientSequence
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
        print ("Generating new candidates...")
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
        ## add- max.sequential_length
        cand = self.generate_initial_candidates()
        new_patterns  = cand
        self.freq_items = []

        self.print_candidates(new_patterns)
        ## create this weird loop
        while len(new_patterns):
            self.freq_items += new_patterns
            candidates = self.generate_new_candidates(self.freq_items)
            new_patterns = self.filter_candidates (candidates)
            # self.print_candidates(new_patterns)
            # f = open("demofile"+str(k_items)+"+1.txt", "a")
            # content = self.write_candidates(new_patterns)
            # f.write(content)
            # f.close()
        #self.print_candidates(self.freq_items)
        self._final_sequences = self.freq_items
        return self._final_sequences