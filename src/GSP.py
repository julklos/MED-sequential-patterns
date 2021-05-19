from SequentialPatternAlgorithm import SequentialPatternAlgorithm

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
       # output_candidates = [key for key, value in candidates.items() if value > self._min_sup]
        output_candidates = [{"item": [key], "supp": value} for key, value in candidates.items() if value > self._min_sup]

        #output_candidates.sort()
        output_candidates.sort(key=lambda x: x.get("item"))
        return output_candidates
    def generate_new_candidates (self, freq_pat):
        """
		Given existing patterns, generate a set of new patterns, one longer.
		"""
        old_cnt = len (freq_pat)    
        old_len = len (freq_pat[0])
        print ("Generating new candidates from %s %s-mers ..." % (old_cnt, old_len))
        new_candidates = []
        for c in freq_pat:
            for d in freq_pat:
                merged_candidate = self.merge_candidates (c, d)
                if merged_candidate and (merged_candidate not in new_candidates):
                    new_candidates.append (merged_candidate)
        ## Postconditions & return:
        return new_candidates
    def merge_candidates (self, a, b):
        if a[1:] == b[:-1]:
            return a + b[-1:]
        else:
            return None

    # def filter_candidates(self,candidates):
    #     filtered_candidates = []
    #     for c in candidates:
    #         curr_cand_hits = self.single_candidate_freq (c)
    #         if self._min_sup <= curr_cand_hits:
    #             filtered_candidates.append ((c, curr_cand_hits))
    #     return filtered_candidates

    # def single_candidate_freq (self, c):
    #     """
	# 	Return true if a candidate is found in the transactions.
	# 	"""
    #     hits = 0
    #     for t in self.transactions:
    #         if self.search_transaction (t, c):
    #             hits += 1
    #     return hits

    def search_transaction (self, t, c):
        """
		Does this candidate appear in this transaction?
		"""
        return (t.find (c) != -1)

    def run(self, min_support):
        self._min_sup = min_support
        
        print('run')
        cand = self.generate_initial_candidates()
        new_patterns  = cand
        self.freq_items = cand
        k_items = 1
        ## create this weird loop
        print(cand)
        while new_patterns and k_items < 3:
            candidates = self.generate_new_candidates ([x.get("item") for x in new_patterns])
            print ("There are %s new candidates." % len (candidates))
            print(candidates)
            new_patterns = candidates
            #new_patterns = self.filter_candidates (candidates) ///finish
            #print(new_patterns)
            k_items+=1
            
        return self._data