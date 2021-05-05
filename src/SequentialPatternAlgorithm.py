from abc import ABC, abstractmethod

class SequentialPatternAlgorithm(ABC) :

    def __init__(self, data):
        self._data = data
        self._final_sequence = None
    
    def set_data(self,data):
        self._data = data
    
    def printFinalSequence(self):
        print(self._final_sequence)
    
    def exportFinalSequence(self):
        pass

    @abstractmethod
    def run(self):
        pass