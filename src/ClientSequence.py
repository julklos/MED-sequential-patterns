class ClientSequence():
    def __init__(self,  items, freq=-1):
        self._items = items
        self._freq = freq
        
    def __len__(self):
        return len(self._items)
    def  __str__(self):
        return str(self._items) + " #SUP: "+ str(self._freq)
    
    def get_pattern(self):
        return self._items
    
    def get_value(self):
        return self._freq

    def get_pattern_size(self):
        return len(self._items)
        
    def generate_candidates(self,_transaction):
        if self._items[:-1] == _transaction._items[:-1]:
            cand_1 = ClientSequence(self._items + [_transaction._items[-1]])
            cand_2 = ClientSequence(_transaction._items + [ self._items[-1]])
            cand_3 = ClientSequence(self._items[:-1] + [sorted(set(_transaction._items[-1] + self._items[-1]))])
            return [cand_1, cand_2, cand_3]
        else :
            return []
        
    def generate_candidate(self):
        return [ClientSequence(self._items + [self._items[-1]])]
    
    def support(self, sequences):
        if self._freq < 0:
            self.single_candidate_freq(sequences)
        return self._freq
            
            
    def single_candidate_freq (self, sequences):
        #   """
        # 	Return support
        # 	"""
        hits = 0
        for t in sequences:
            if self.search_sequence (t):
                hits += 1
        self._freq = hits
        
    def search_sequence (self,sequence):
        #   """
        # 	Return true if a candidate is found in the transactions.
        # 	"""
        seq_ = sequence.get_itemsets()
        for item in self._items:
            idx_ = [i for i,e in enumerate(seq_) if all(elem in e  for elem in item) ]
            if len(idx_):
                seq_ = seq_[idx_[0]+1:]
            else:
                return False
        return True

