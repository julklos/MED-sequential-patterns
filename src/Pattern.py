
class Pattern():

    def __init__(self, pattern, value = None) :
        self.pattern = pattern
        self.value = value
    
    def __str__ (self):
        return "Wzorzec:" + str(self.pattern) + " Liczba: " + str(self.value)
    
    def get_pattern(self):
        return self.pattern
    
    def get_value(self):
        return self.value

    def get_pattern_size(self):
        return len(self.pattern)