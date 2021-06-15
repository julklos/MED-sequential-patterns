from Sequence import Sequence
import math
class DataProcessor():
    '''
    Class responsibile for loadind and preprocessing spmf and text file
    '''

    def __init__(self, newline = "-2", splitter = "-1", limit = math.inf):
        self.newline = newline
        self.splitter = splitter
        self.limit = int(limit)

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
        if self.splitter == "-1":
            sequences_obj = [ Sequence(self.preprocess_spmf_itemset(val, self.splitter), idx) for idx, val in enumerate(sequences) ]
        else:
            sequences = self.preprocess_file(sequences)
            sequences_obj =  [ Sequence(val, idx) for idx, val in enumerate(sequences) ]
        return sequences_obj
    def preprocess_file(self, sequences):
        result = {}
        final_ = []
        for seq in sequences:
            if seq[0] not in result.keys():
                result[seq[0]] = []
            val = result[seq[0]]
            val.append(seq[1:].strip())
            result[seq[0]] = val
        for key, value in result.items():
            transactions = []
            for el in value:
                ## maybe sort by digits..?
                res  = ''.join(i for i in el if not i.isdigit()).strip()
                if self.splitter:
                    res = res.split(self.splitter)
                    res = [ i.strip() for i in res]
                else:
                    res = self.split_into_char(res)
                transactions.append(res)
            final_.append(transactions)
        print(transactions)
        return final_
            
    
    def preprocess_spmf_itemset(self, itemset, splitter):
        # split itemsets
        itemset = itemset.split(splitter)
        # delete whitespaces
        itemset = [i.strip() for i in itemset]
        if splitter == "-1":
            itemset = [self.preprocess_spmf_itemset(i, " ") for i in itemset if i]
        return itemset

    def split_into_char(self, word):
        return [char for char in word]
        
