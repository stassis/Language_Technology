#from nltk.stem.porter import PorterStemmer
import pandas as pd
from collections import Counter
import json
import time
from nltk.stem import WordNetLemmatizer

# Get start time to calculate execution time.
start_time = time.time()

# Import html cleared csv
# Use converter because ['Content'] column is inserted as string and we want a list as it originally is. PorterSremmer will not work if we don't convert to list.
df = pd.read_csv('postagged.csv', converters={'Content': eval})

# Insert to 'words' variable just the words without the POS tag.
words = df['Content'].apply(lambda x: [y[0] for y in x])
# Stem words using PorterStemmer.
#words = words.apply(lambda x: [PorterStemmer().stem(y) for y in x])
# Lemmatize words using WordNetLemmatizer.
words = words.apply(lambda x: [WordNetLemmatizer().lemmatize(y) for y in x])

# Store stemmed words to csv for later use.
words.to_csv("words.csv", index=False)


# 'words' is an object, so we create an empty list 'word_list' and insert all stemmed words from each article to apply 'Counter' function. 'Counter' function is applied to lists, not objects.
word_list = []

for i in words:
    for j in i:
        word_list.append(j)


# Count each word appearance.
# We use dict to convert 'collections.Counter' type to 'dict' type. We do this to have a clear JSON File.
word_count = dict(Counter(word_list))

# store the file with extension .json
filename = 'word_count.json'
#open the file in write mode       
with open(filename, 'w') as file_object:
    json.dump(word_count, file_object)


# *** Read JSON File ***
# f = open('counts.json')
 
# #returns JSON object as a dictionary
# data = json.load(f)

# *** Read JSON File - END***

# Calculate and print total execution time (seconds).
print("--- %s seconds ---" % (time.time() - start_time))