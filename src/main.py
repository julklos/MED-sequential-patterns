
from PrefixSpan import PrefixSpan
from GSP import GSP 
from DataProcessor import DataProcessor
#from prefixspan import PrefixSpan
import configparser
import json
import logging 
import sys

def check_if_spmf(file_name):
    extention = file_name.split('.')[-1]
    return "spmf" == extention


if __name__ == "__main__":
    ## read path to config file
    config_path = sys.argv[1]
    if not config_path:
        raise Exception("Missing config file/Wrong path")
    ## reading config file
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
    except Exception as e :
        print(str(e))
    config.read(config_path)
    algorithm = config.get('configuration', 'algorithm', raw=False)
    limit = config.get('configuration', 'limit')
    input_path = str(config.get('configuration', 'input', raw=False))
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
        logging.error("Nie można otworzyć pliku")

    if algorithm == "GSP":
        al1 = GSP(data,min_support=min_support, max_seq_length=max_length, min_seq_length=min_length)
        
    elif algorithm == "PrefixSpan":
        al1 = PrefixSpan(data, min_support,max_seq_length=max_length, min_seq_length=min_length)
    else: 
        raise Exception("Unknown algorithm: choose GSP or PrefixSpan")

    output_data = al1.run()
    try :
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=4)
        logging.info('Output saved to file')
    except Exception as e:
        print(e)

    #al1.printFinalSequence()

    # min_support = 2 # TODO parametr z pliku- czy z zakresu 0-1?
    # print( "here", al1.run() )

    # db = [
    #         ['C', 'A', 'G', 'A', 'A', 'G','T' ],
    #         ['T', 'G','A','C','A','G'],
    #         ['G','A','A','G','T'],
    #         []
    #     ]

    # print(PrefixSpan(db).frequent(3))



    