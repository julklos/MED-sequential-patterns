
class Pattern():

    def __init__(self, pattern, sup = None) :
        self._pattern = pattern
        self._sup = sup
    
    def __str__ (self):
        return "Wzorzec:" + str(self.pattern) + " Liczba: " + str(self.value)
    
    def get_pattern(self):
        return self._pattern
    
    def get_value(self):
        return self._sup

    def get_pattern_size(self):
        return len(self.pattern)