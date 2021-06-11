
class Pattern():

    def __init__(self, pattern, value) :
        self.pattern = pattern
        self.value = value
    
    def __str__ (self):
        return "Wzorzec:" + str(self.pattern) + " Liczba: " + str(self.value)