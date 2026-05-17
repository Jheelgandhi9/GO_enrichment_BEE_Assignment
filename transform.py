import sys

for line in sys.stdin:
    l_items = line.strip().split("\t")

    ted = int(l_items[7])+1
    col4 = "chr"+l_items[4]+"@"+str(l_items[7])+"-"+str(ted)+"|"+l_items[6]
    
    col6 = ""
    if l_items[5][0]=='1':
        col6 = "+"
    else:
        col6 = "-"

    transformed_items = ["chr"+l_items[4],l_items[7],str(ted),col4,".",col6]
    
    for i in transformed_items:
        print(i,end="\t")
    print("")

# cat filtered.tsv | python transform.py > genes.bed 
# runs in about 1-2 s 