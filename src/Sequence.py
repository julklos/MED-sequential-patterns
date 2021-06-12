class Sequence() :

    def __init__(self,  itemsets, id = -1):
        self._id = id
        self._itemsets = itemsets
    def  __str__(self):
        return "Id: "+str(self._id)+" items: "+ str(self._itemsets)
    
    def get_unique_values(self):
        flatten = sum(self._itemsets, [])
        return set(flatten)
    
    def get_itemsets(self):
        return self._itemsets
    
    def get_id(self):
        return self._id
    
    def frequent_item_from_itemset(self, freq):
        new_itemsets = []
        for itemset in self._itemsets :
            new_itemset = []
            for item in itemset :
                if item in freq :
                    new_itemset.append(item)
            if len(new_itemset) != 0 :
                new_itemsets.append(new_itemset)
        return new_itemsets