class Sequence() :

    def __init__(self, id, itemsets):
        self._id = id
        self._itemsets = itemsets
    def  __str__(self):
        return "Id: "+str(self._id)+" items: "+ str(self._itemsets)
    
    def get_unique_values(self):
        flatten = sum(self._itemsets, [])
        return set(flatten)
    
    def get_itemsets(self):
        return self._itemsets