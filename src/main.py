
from PrefixSpan import PrefixSpan
from GSP import GSP 
from DataProcessor import DataProcessor
#from prefixspan import PrefixSpan
import configparser
import json
import logging 

def check_if_spmf(file_name):
    extention = file_name.split('.')[-1]
    return "spmf" == extention


if __name__ == "__main__":
    ## reading config file
    config = configparser.ConfigParser()
    config_path = r"/home/patrycja/Desktop/Repositories/MED-sequential-patterns/src/setup.cfg"
    try:
        config.read(config_path)
    except Exception as e :
        print(str(e))
    config.read(config_path)
    algorithm = config.get('configuration', 'algorithm', raw=False)
    limit = config.getint('configuration', 'limit')
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

    # for seq in data:
    #      print(seq)

    al1 = PrefixSpan(data, min_support)

    output_data = al1.run()

    try :
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=4)
        logging.info('Output saved to file')
    except Exception as e:
        print(e)
    #al1.printFinalSequence()
    
    print('Time: ' + str(output_data['time']))
    print('Found sequences: ' + str(output_data['found_seq']))


    