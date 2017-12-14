import json
from pprint import pprint
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords

def cleanString(my_string):
    ## removing all punctuation marks as well as non alphabetic character
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(my_string.lower())

    ## defining portuguese stopwords
    stopWords = set(stopwords.words('portuguese'))
    stopWords.add('r')
    stopWords.add('R')
    vocabulary = ' '.join([word for word in words if word not in stopWords])

    return vocabulary


# ### Reading dataset stored in json file

# In[3]:

json_data = json.load(open('Dataset-Treino-Anonimizado-3.json', 'r'))
# filez = open('ConjuntoTeste.json', 'r', encoding="utf-8")
# print("Pelo menos abriu")
# json_data = json.load(filez)

json_to_write = []
with open('DatasetTratado.json', 'w') as outFile:
    for document in json_data:
        document['id'] = document['id']
        document['title'] = cleanString(document['title'])
        document['description'] = cleanString(document['description'])
        json_to_write.append(document)
    json.dump(json_to_write, outFile)
    print("Dataset Cleaned successfully")
