import csv
import itertools

def jaccard(set_a, set_b):
    """Jaccard similarity of two sets.

    The Jaccard similarity is defined as the size of the intersection divided by
    the size of the union of the two sets.

    Parameters
    ---------
    set_a: set
        Set of arbitrary objects.

    set_b: set
        Set of arbitrary objects.
    """

    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


# start_time = time.time()
filetoread = open("jaccardDist.csv", "r", newline = '', encoding="utf-8")
filetoread1 = open("jaccardDist.csv", "r", newline = '', encoding="utf-8")
reader1 = csv.reader(filetoread)
reader2 = csv.reader(filetoread1)

filetowrite = open("gabarito.csv", "w", newline = '')
writer = csv.writer(filetowrite)

printer = []
counter1 = 0
readerzao = list(reader1)
outerloop, innerloop = itertools.tee(reader1,2)
for line in readerzao:
    document1 = set()
    for word in line:
        document1.add(word)
    counter2 = 0
    for line2 in readerzao:
        if counter1 < counter2:
            document2 = set()
            for word2 in line2:
                document2.add(word2)
            if jaccard(document1, document2) >= 0.7:
                printer.append([counter1, counter2])
        counter2 += 1
    counter1 += 1
    print(counter1, "out of 10000")

writer.writerows(printer)
filetowrite.close()
filetoread.close()
