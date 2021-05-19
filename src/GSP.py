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
        output_candidates = []
        for key, value in candidates.items():
            if( value > self._min_sup):
                output_candidates.append({"item": key, "support": value})
        return output_candidates
            
        

    def run(self, min_support):
        self._min_sup = min_support
        print('run')
        cand = self.generate_initial_candidates()
        ## create this weird loop
        print(cand)
        return self._data