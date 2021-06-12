class Transaction():
    def __init__(self,  items):
        self._items = items
        
    def __len__(self):
        return len(self._items)
    
    def  __str__(self):
        return self._items
        