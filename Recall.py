import csv

gabaritoFile = open("gabarito.csv", "r", newline = '', encoding="utf-8")
readerGabarito = csv.reader(gabaritoFile)

final_csv = open("final_output.csv", "r", newline = '', encoding="utf-8")
readerFinalCSV = csv.reader(final_csv)

dirtyResult = list(readerFinalCSV)
result = [item[0] for item in dirtyResult]

dirtyGabarito = list(readerGabarito)


truePositive = 0
falseNegative = 0

for item in dirtyGabarito:
    document1 = item[0]
    document2 = item[1]
    if result[int(document1)] == result[int(document2)]:
        truePositive += 1
    else:
        falseNegative += 1

print("Recall was ", truePositive/(truePositive + falseNegative))

truePositive = 0
trueNegative = 0
counter1 = 1
for doc1cluster in result:
    counter2 = 2
    for doc2cluster in result:
        if counter1 < counter2:
             if doc1cluster == doc2cluster:
                 foundit = None
                 for item in dirtyGabarito:
                     if item[0] == str(counter1) and item[1] == str(counter2):
                         foundit = True
                         break
                 if foundit:
                     truePositive += 1
                 else:
                     trueNegative += 1
        counter2 += 1
    counter1 += 1

print("true positive ", truePositive)
print("true negative ", trueNegative)
print("Precision was ", truePositive/(truePositive+trueNegative))
