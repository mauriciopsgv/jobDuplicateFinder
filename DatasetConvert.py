import json
import csv
from pprint import pprint

fulldataset = json.load(open("C:/code/jobDuplicateFinder/DatasetTratado.json"))

# Getting n first entrys
n = 200
print(fulldataset[0])
smallDataset = []
for a in fulldataset:
    smallDataset.append((a["description"].split()).append(a["title"]))
#    if (fulldataset.index(a) == n - 1):
#        break

print(smallDataset[0])

filetowrite = open("smallDataset.csv", "w", newline ='')
writer = csv.writer(filetowrite)
writer.writerows(smallDataset)
filetowrite.close()
