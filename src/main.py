
from PrefixSpan import PrefixSpan
from GSP import GSP 
from DataProcessor import DataProcessor
import configparser
import json
import logging 
import sys
import math
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.ERROR)

def check_if_spmf(file_name):
    extention = file_name.split('.')[-1]
    return "spmf" == extention

def check_if_number(min, max, value):
    try :
        value = float(value)
        if value >= min and value <= max :
            return True
        else:
            print(value, value>= min, min)
            raise Exception("Parametr should be in range {} - {}".format(min,max))
    except Exception as e:
        logging.error(e)
        return False

def check_parameters(limit, min_support, max_length, min_length):
    if check_if_number(0, math.inf, limit) and check_if_number(0, 1, min_support) and check_if_number(1,math.inf, max_length) and check_if_number(0, math.inf, min_length):
        return True
    else: return False


if __name__ == "__main__":
    print("MAIN")
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
    max_length = config.get('configuration', 'max_length')
    min_length = config.getint('configuration', 'min_length')
    splitter = config.get('configuration', 'splitter')
    if limit == "None":
        limit = math.inf
    else:
        limit = int(limit)
    if max_length == "None":
        max_length = math.inf
    else:
        max_length = int(max_length)
    # TODO: pętla - wpisywanie nazwy pliku,  sprawdzenie czy spfm i txt- txt, chyba trzeba dodac parsowanie per nr indexu oraz czas (?)
    # .txt newline = "\n" splitter= " "
    # .spmf newline= "-2" splitter = "-1"
    if check_if_spmf(input_path):
        newline = "-2"
        splitter = "-1"
    else:
        newline = "\n"
        splitter = splitter
    
    if check_parameters(limit, min_support, max_length, min_length) == False :
        raise Exception("Parameteres not valid")

    dp = DataProcessor(newline=newline,  splitter=splitter, limit=limit)
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
    print("Time: " + str(output_data['time']))
    print("Found sequences: " + str(output_data['found_seq']))
    try :
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=4)
        logging.info('Output saved to file')
    except Exception as e:
        print(e)




    