from abc import ABC, abstractmethod

class SequentialPatternAlgorithm(ABC) :

    def __init__(self, data, min_support):
        self._data = data
        self._final_sequences = []
        self._min_support = min_support
    
    def set_data(self,data):
        self._data = data
    
    def printFinalSequence(self):
        print(self._final_sequences)
    
    def exportFinalSequence(self):
        pass

    @abstractmethod
    def run(self):
        pass