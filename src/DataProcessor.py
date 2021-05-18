from Sequence import Sequence
class DataProcessor():

    def __init__(self, newline = "-2", splitter = "-1"):
        self.newline = newline
        self.splitter = splitter

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
        # create array
        sequences_obj = [ Sequence(idx, self.preprocess_spmf_itemset(val, self.splitter) ) for idx, val in enumerate(sequences) ]
        return sequences_obj

    def preprocess_spmf_itemset(self, itemset, splitter):
        # split itemsets
        itemset = itemset.split(splitter)
        # delete whitespaces
        itemset = [i.strip() for i in itemset if i.strip()]
        if splitter == "-1":
            itemset = [self.preprocess_spmf_itemset(i, " ") for i in itemset ]
        return itemset
        
