from Sequence import Sequence
class DataProcessor():

    def load(self,path, spmf = True):
        if spmf:
            return self.load_spmf(path)
        else:
            return self.load_text(path)

    def load_spmf(self, path):
        file = open(path,mode='r')
        # read all lines at once
        content = file.read()
        # close the file
        file.close()
        content = content.replace("\n", "")
        sequences = content.split("-2")
        # delete empty
        sequences = [x for x in sequences if x]
        # create array
        sequences_obj = [ Sequence(idx, self.preprocess_spmf_itemset(val) ) for idx, val in enumerate(sequences) ]
        return sequences_obj

    def loaf_text(self, path):
        return

    def preprocess_spmf_itemset(self, itemset, splitter = "-1"):
        # split itemsets
        itemset = itemset.split(splitter)
        # delete whitespaces
        itemset = [i.strip() for i in itemset if i.strip()]
        if splitter == "-1":
            itemset = [self.preprocess_spmf_itemset(i, " ") for i in itemset ]
        return itemset
        
