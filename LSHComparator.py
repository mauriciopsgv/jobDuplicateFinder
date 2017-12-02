import csv
from datasketch import MinHash, MinHashLSH

filetoread = open("smallDataset.csv", "r", newline = '')
reader = csv.reader(filetoread)

minHashs = []
for line in reader:
    minHash = MinHash(num_perm=128)
    for word in line:
        minHash.update(word.encode('utf-8'))
    minHashs.append(minHash)

lsh = MinHashLSH(threshold=0.99, num_perm=128)

counter = 0
for m in minHashs:
    lsh.insert( "m" + str(counter)  , m)
    counter += 1

result = lsh.query(minHashs[1])
print("Approximate neighbours with Jaccard similarity > 0.5", result)
print("Number of minHashs ", len(minHashs))
print("Number of lines", len(list(reader)))
print("Minhashes bitches")
print(minHashs)
