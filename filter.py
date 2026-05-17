import sys

chromDict = {str(i): i for i in range(1,23)}
chromDict["X"] = 23
chromDict["Y"] = 24

for line in sys.stdin:
    l_items = line.split("\t")
    if l_items[4] in chromDict:
        print(line,end="")