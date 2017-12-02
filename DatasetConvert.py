import json
import csv
from pprint import pprint

fulldataset = json.load(open("D:/code/datascience/DatasetTratado.json"))

# Getting n first entrys
n = 50
smallDataset = []
for a in fulldataset:
    smallDataset.append(a["description"].split())
    if (fulldataset.index(a) == n - 1):
        break

print(smallDataset[0])

filetowrite = open("smallDataset.csv", "w", newline ='')
writer = csv.writer(filetowrite)
writer.writerows(smallDataset)
filetowrite.close()
