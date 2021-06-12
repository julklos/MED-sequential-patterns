from PrefixSpan import PrefixSpanAlgorithm
from GSP import GSP 
from DataProcessor import DataProcessor
#from Prefixspan import PrefixSpan


def check_if_spmf(file_name):
    [_, extention] = file_name.split('.')
    return extention == "spmf"


if __name__ == "__main__":
    path = "../data/"
    file_name = "short.spmf"
    # TODO: pętla - wpisywanie nazwy pliku,  sprawdzenie czy spfm i txt- txt, chyba trzeba dodac parsowanie per nr indexu oraz czas (?)
    # .txt newline = "\n" splitter= " "
    # .spmf newline= "-2" splitter = "-1"
    if check_if_spmf(file_name):
        newline = "-2"
        splitter = "-1"
    else:
        # TODO: pobranie z pliku
        newline = "-2"
        splitter = "-1"
    dp = DataProcessor(newline=newline,  splitter=splitter)
    try :
        data = dp.load(path+file_name)
    except OSError:
        print("Nie można otworzyć pliku")

    # for seq in data:
    #     print(seq)

    al1 = GSP(data, 0.4)
    al1.run()
    al1.printFinalSequence()
    # al1 = GSP(data,2)
    # min_support = 2 # TODO parametr z pliku- czy z zakresu 0-1?
    # print( "here", al1.run() )

    db = [
            ['C', 'A', 'G', 'A', 'A', 'G','T' ],
            ['T', 'G','A','C','A','G'],
            ['G','A','A','G','T']
        ]

    # print(PrefixSpan(db).frequent(3))


    