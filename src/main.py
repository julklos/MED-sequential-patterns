from PrefixSpan import PrefixSpan
from DataProcessor import DataProcessor

if __name__ == "__main__":
    dp = DataProcessor()
    data = dp.load("../data/short_d.spmf", True)
    for seq in data:
        print(seq)

    # al1 = PrefixSpan("costam")
    # print( al1.run() )