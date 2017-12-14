
# coding: utf-8

# In[1]:

import json
from pprint import pprint
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords


# In[2]:

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
pprint(json_data[0])


# ###  Preprocess dataset to be contained in a single file 

# In[4]:

with open('data/dataset.text.txt', 'wb') as outFile:
    for num, document in enumerate(json_data):
        docid = str(document['id'])
        title = cleanString(document['title'])
        description = cleanString(document['description'])
        
        outFile.write(('{}\t{} {}\n'.format(docid, title, description)).encode('utf-8'))

        print(docid, title, description)


# ### Testing the LSH module

# In[5]:

get_ipython().magic('matplotlib inline')

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

ix = pd.IndexSlice


# In[26]:

df = pd.DataFrame(data=[(2, 50), (50, 2), (10, 10), (5, 20), (20, 5)], columns=['pieces', 'size'])
df['hashes'] = df['pieces'] * df['size']
for pr in np.linspace(0, 1, 200):
    df[pr] = 1 - (1 - pr**df['size']) ** df['pieces']

df = pd.pivot_table(df, index=['hashes', 'pieces', 'size'])

ax = df.T.plot(figsize=(10, 7), title='Probability of LSH finding a candidate pair', fontsize=15);
plt.ylabel('Probability of being chosen as candidate', fontsize=15);
plt.xlabel('Jaccard similarity', fontsize=15);
plt.legend(list(df.loc[ix[100]].index),
           bbox_to_anchor=(1., 1, 1., 0), loc='upper left', fontsize=14, 
           ncol=1, borderaxespad=0., title='Each line shows the\nfingerprint chopped\ninto (pieces, size)\n');
plt.savefig("fig1")


# ### Utility functions

# In[13]:

import itertools

from lsh import cache, minhash

# a pure python shingling function that will be used in comparing
# LSH to true Jaccard similarities
def get_shingles(text, char_ngram=5):
    """Create a set of overlapping character n-grams.
    
    Only full length character n-grams are created, that is the first character
    n-gram is the first `char_ngram` characters from text, no padding is applied.

    Each n-gram is spaced exactly one character apart.

    Parameters
    ----------

    text: str
        The string from which the character n-grams are created.

    char_ngram: int (default 5)
        Length of each character n-gram.
    """
    
    return set(text[head:head + char_ngram] for head in range(0, len(text) - char_ngram))


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


def candidate_duplicates(document_feed, char_ngram=5, seeds=100, bands=5, hashbytes=4):
    #char_ngram = 5
    sims = []
    hasher = minhash.MinHasher(seeds=seeds, char_ngram=char_ngram, hashbytes=hashbytes)
    if seeds % bands != 0:
        raise ValueError('Seeds has to be a multiple of bands. {} % {} != 0'.format(seeds, bands))
    
    lshcache = cache.Cache(num_bands=bands, hasher=hasher)
    for i_line, line in enumerate(document_feed):
        line = line.decode('utf8')
        docid, headline_text = line.split('\t', 1)
        fingerprint = hasher.fingerprint(headline_text.encode('utf8'))
        
        # in addition to storing the fingerpring store the line
        # number and document ID to help analysis later on
        lshcache.add_fingerprint(fingerprint, doc_id=(i_line, docid))

    candidate_pairs = set()
    for b in lshcache.bins:
        for bucket_id in b:
            if len(b[bucket_id]) > 1:
                pairs_ = set(itertools.combinations(b[bucket_id], r=2))
                candidate_pairs.update(pairs_)
    
    return candidate_pairs


# In[9]:

hasher = minhash.MinHasher(seeds=100, char_ngram=5, hashbytes=4)
lshcache = cache.Cache(bands=10, hasher=hasher)

# read in the data file and add the first 100 documents to the LSH cache
with open('data/dataset.text.txt', 'rb') as fh:
    feed = itertools.islice(fh, 100)
    for line in feed:
        docid, articletext = line.decode('utf8').split('\t', 1)
        lshcache.add_fingerprint(hasher.fingerprint(line), docid)

# for every bucket in the LSH cache get the candidate duplicates
candidate_pairs = set()
for b in lshcache.bins:
    for bucket_id in b:
        if len(b[bucket_id]) > 1: # if the bucket contains more than a single document
            pairs_ = set(itertools.combinations(b[bucket_id], r=2))
            candidate_pairs.update(pairs_)



# In[10]:

candidate_pairs


# In[11]:

num_candidates = []
bands = [2, 5, 10, 20]
for num_bands in bands:
    with open('data/dataset.text.txt', 'rb') as fh:
        feed = itertools.islice(fh, 1000)
        candidates = candidate_duplicates(feed, char_ngram=5, seeds=100, bands=num_bands, hashbytes=4)
        num_candidates.append(len(candidates))


# In[28]:

fig, ax = plt.subplots(figsize=(8, 6))
plt.bar(bands, num_candidates, align='center');
plt.title('Number of candidate duplicate pairs found\n by LSH using 100 minhash fingerprint.', fontsize=15);
plt.xlabel('Number of bands', fontsize=15);
plt.ylabel('Number of candidate duplicates', fontsize=15);
plt.xticks(bands, bands);
plt.savefig("fig2")


# In[14]:

lines = []
with open('data/dataset.text.txt', 'rb') as fh:
    # read the first 1000 lines into memory so we can compare them
    for line in itertools.islice(fh, 1000):
        lines.append(line.decode('utf8'))
    
    # reset file pointer and do LSH
    fh.seek(0)
    feed = itertools.islice(fh, 1000)
    candidates = candidate_duplicates(feed, char_ngram=5, seeds=100, bands=20, hashbytes=4)

# go over all the generated candidates comparing their similarities
similarities = []
for ((line_a, docid_a), (line_b, docid_b)) in candidates:
    doc_a, doc_b = lines[line_a], lines[line_b]
    shingles_a = get_shingles(lines[line_a])
    shingles_b = get_shingles(lines[line_b])
    
    jaccard_sim = jaccard(shingles_a, shingles_b)
    fingerprint_a = set(hasher.fingerprint(doc_a.encode('utf8')))
    fingerprint_b = set(hasher.fingerprint(doc_b.encode('utf8')))
    minhash_sim = len(fingerprint_a & fingerprint_b) / len(fingerprint_a | fingerprint_b)
    similarities.append((docid_a, docid_b, jaccard_sim, minhash_sim))


# In[15]:

import random

print('There are {} candidate duplicates in total'.format(len(candidates)))
random.sample(similarities, k=15)


# In[16]:

sims_all = np.zeros((1000, 1000), dtype=np.float64)
for i, line in enumerate(lines):
    for j in range(i+1, len(lines)):
        shingles_a = shingles(lines[i])
        shingles_b = shingles(lines[j])
        jaccard_sim = jaccard(shingles_a, shingles_b)
        
        # similarities are symmetric so we only care about the
        # upper diagonal here and leave (j, i) to be 0
        sims_all[i, j] = jaccard_sim


# In[19]:

# turn the candidates into a dictionary so we have easy access to
# candidates pairs that were found
candidates_dict = {(line_a, line_b): (docid_a, docid_b) for ((line_a, docid_a), (line_b, docid_b)) in candidates}
found = 0
for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        if sims_all[i, j] >= .9:
            # documents i and j have an actual Jaccard similarity >= 90%
            found += ((i, j) in candidates_dict or (j, i) in candidates_dict)

print('Out of {} pairs with similarity >= 90% {} were found, that\'s {:.1%}'.format((sims_all >= .9).sum(), found, found / (sims_all >= .9).sum()))


# In[ ]:



