import csv
import time
from datasketch import MinHash, MinHashLSH

start_time = time.time()
filetoread = open("smallDataset.csv", "r", newline = '')
reader = csv.reader(filetoread)

minHashs = []
for line in reader:
    minHash = MinHash(num_perm=128)
    for word in line:
        minHash.update(word.encode('utf-8'))
    minHashs.append(minHash)

t = 0.5
# threshold 0.7 ainda pode ser melhor, testar como ele perfoma com sinônimos
lsh = MinHashLSH(threshold=t, num_perm=128)

counter = 0
for m in minHashs:
    lsh.insert( "m" + str(counter)  , m)
    counter += 1
print("Time que passou ate a query = ", time.time() - start_time)
result = lsh.query(minHashs[1])
print("Approximate neighbours with Jaccard similarity > ", t, result)
print("Number of minHashs ", len(minHashs))
print("Time que passou = ", time.time() - start_time)
