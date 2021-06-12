from Sequence import Sequence
import math
class DataProcessor():

    def __init__(self, newline = "-2", splitter = "-1", limit = math.inf):
        self.newline = newline
        self.splitter = splitter
        self.limit = limit

    def load(self,path):
        return self.load_file(path)

    def load_file(self, path):
        file = open(path,mode='r')
        # read all lines at once
        content = file.read()
        # close the file
        file.close()
        if self.newline != "\n" :
            content = content.replace("\n", "")
        sequences = content.split(self.newline)
        # delete empty
        sequences = [x for x in sequences if x]
        if len(sequences) > self.limit :
            sequences = sequences[:self.limit]
        # create array
        sequences_obj = [ Sequence(self.preprocess_spmf_itemset(val, self.splitter), idx) for idx, val in enumerate(sequences) ]
        return sequences_obj

    def preprocess_spmf_itemset(self, itemset, splitter):
        # split itemsets
        itemset = itemset.split(splitter)
        # delete whitespaces
        #itemset = [self.split_into_char(i.replace(" ","")) for i in itemset if i.strip()]
        itemset = [i.strip() for i in itemset]
        if splitter == "-1":
            itemset = [self.preprocess_spmf_itemset(i, " ") for i in itemset if i]
        return itemset

    def split_into_char(self, word):
        return [char for char in word]
        
