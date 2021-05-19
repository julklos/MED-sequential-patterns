from PrefixSpan import PrefixSpan
from GSP import GSP 
from DataProcessor import DataProcessor

if __name__ == "__main__":
    # TODO: pętla - wpisywanie nazwy pliku,  sprawdzenie czy spfm i txt- txt, chyba trzeba dodac parsowanie per nr indexu oraz czas (?)
    # .txt newline = "\n" splitter= " "
    # .spmf newline= "-2" splitter = "-1"
    dp = DataProcessor(newline="-2", splitter="-1")
    try :
        data = dp.load("data/short_d.spmf")
    except OSError:
        print("Nie można otworzyć pliku")

    for seq in data:
        print(seq)

    al1 = PrefixSpan(data, 2)
    al1.run()
    # print( al1.run() )
    #al1 = GSP(data)
    #min_support = 3 ## parametr do pliku + dodaj 
    #print( "here", al1.run(min_support) )