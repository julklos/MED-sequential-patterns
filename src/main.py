from PrefixSpan import PrefixSpan
from DataProcessor import DataProcessor

if __name__ == "__main__":
    # TODO: pętla - wpisywanie nazwy pliku,  sprawdzenie czy spfm i txt
    dp = DataProcessor(newline="\n", splitter=" ")
    try :
        data = dp.load("data/simple.txt")
    except OSError:
        print("Nie można otworzyć pliku")

    for seq in data:
        print(seq)

    al1 = PrefixSpan(data)
    print( al1.run() )