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
    vocabulary = ' '.join([word for word in words if word not in stopWords]).encode('utf-8')

    return vocabulary


# ### Reading dataset stored in json file

# In[3]:

json_data = json.load(open('data/Dataset-Treino-Anonimizado-3_orig.json', 'r'))

with open('data/dataset.text.txt', 'wb') as outFile:
    for num, document in enumerate(json_data):
        docid = str(document['id'])
        title = cleanString(document['title'])
        description = cleanString(document['description'])

        outFile.write(('{}\t{} {}\n'.format(docid, title, description)).encode('utf-8'))

        print(docid, title, description)
