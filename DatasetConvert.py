import json
import csv
from pprint import pprint

fulldataset = json.load(open("DatasetTratado.json", encoding="utf-8"))
#fulldataset = json.load(open("DatasetTestezaoPlease.json"))


# Getting n first entrys
n = 20
smallDataset = []
for a in fulldataset:
    smallDataset.append(a["description"].split() + a["title"].split())
    # if (fulldataset.index(a) == n - 1):
    #     break


filetowrite = open("smallDataset.csv", "w", newline ='', encoding="utf-8")
writer = csv.writer(filetowrite)
writer.writerows(smallDataset)
filetowrite.close()
print("Dataset Converted successfully")
