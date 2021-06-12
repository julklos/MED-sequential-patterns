from PrefixSpan import PrefixSpanAlgorithm
from GSP import GSP 
from DataProcessor import DataProcessor
#from Prefixspan import PrefixSpan
import configparser



def check_if_spmf(file_name):
    extention = file_name.split('.')[-1]
    return "spmf" == extention


if __name__ == "__main__":
    ## reading config file
    config = configparser.ConfigParser()
    config.read('./setup.cfg')
    algorithm = config.get('configuration', 'algorithm', raw=False)
    limit = config.getint('configuration', 'limit')
    input_path = config.get('configuration', 'input', raw=False)
    output = config.get('configuration', 'output', raw=False)
    min_support = config.getfloat('configuration', 'min_support')
    max_length = config.getint('configuration', 'max_length')
    min_length = config.getint('configuration', 'min_length')
    splitter = config.get('configuration', 'splitter')

    # TODO: pętla - wpisywanie nazwy pliku,  sprawdzenie czy spfm i txt- txt, chyba trzeba dodac parsowanie per nr indexu oraz czas (?)
    # .txt newline = "\n" splitter= " "
    # .spmf newline= "-2" splitter = "-1"
    if check_if_spmf(input_path):
        newline = "-2"
        splitter = "-1"
    else:
        # TODO: pobranie z pliku
        newline = "\n"
        splitter = splitter
    
    dp = DataProcessor(newline=newline,  splitter=splitter)
    try :
        data = dp.load(input_path)
    except OSError:
        print("Nie można otworzyć pliku")

    al1 = GSP(data, min_support)
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


    