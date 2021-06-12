from abc import ABC, abstractmethod
import math

class SequentialPatternAlgorithm(ABC) :

    def __init__(self, data, min_support = 0.01, max_seq_length = math.inf, min_seq_length = 1):
        self._data = data
        self._final_sequences = {}
        self._min_support = int(min_support * len(self._data))
        if self._min_support <= 0:
            raise ValueError("Min support cannot be 0")
        self._max_seq_length = max_seq_length
        self._min_seq_length = min_seq_length
        
    
    def set_data(self,data):
        self._data = data
    
    def printFinalSequence(self):
        print("Znalezione wzorce sekwencyjne:")
        for sequence in self._final_sequences :
            print(sequence)
    
    def exportFinalSequence(self):
        pass

    @abstractmethod
    def run(self):
        pass