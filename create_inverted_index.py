import pandas as pd
import numpy as np
from collections import Counter
import xml.etree.ElementTree as ET
import time
import xml.dom.minidom


# Get start time to calculate execution time.
start_time = time.time()

# Use converter because ['Content'] column is inserted as string and we want a list as it originally is. 
# We will not be able to extract words if we don't convert to list.
df = pd.read_csv('words.csv', converters={'Content': eval})
psg = pd.read_csv('postagged.csv')


# *** WHAT TO EXPECT: words_in_docs ***
#             {'william': {0,
#             4,
#             5,
#             7,
#             ...},
#             'championship': {0,
#              1,
#              2,
#             ...},
#             ...
# *** END OF WHAT TO EXPECT: words_in_docs ***

# Create words_in_docs emty set and then polupate with unique words as keys and another set 
# of corresponding documents(documents in wich the word appears) to each word as value.
words_in_docs = {}
for i in range(len(df['Content'])):
    tokens = df['Content'][i]
    for w in tokens:
        try:
            words_in_docs[w].add(i)
        except:
            words_in_docs[w] = {i}



# Create a copy of words_in_docs. '.copy()' is a 'must',
# otherwise words_in_docs_num will work as a pointer to words_in_docs and original values in words_in_docs will change.

# words_in_docs_num is the same as words_in_docs and the only difference are the values. 
# Values here are not a set of documents but an integer that represents the count of documents in wich the word appears.

# *** WHAT TO EXPECT: words_in_docs_num ***
# {'william': 355,
#  'driver': 789,
#  'nichola': 90,
#  'latifi': 56,
#  'reveal': 800,
#  'receiv': 1243,
#  'death': 345,
#  'threat': 525,
#  'wake': 363,
#  'formula': 616,
#   ...}
# *** END OF WHAT TO EXPECT: words_in_docs_num ***

words_in_docs_num = words_in_docs.copy()
for i in words_in_docs_num:
    words_in_docs_num[i] = len(words_in_docs_num[i])
words_in_docs_num


# Create an empty set 'tf_idf' to insert tfidf values. tf_idf set has two indexes. First Index is Document line in our csv (an Integer). Second Index is the token(word) in the document.
tf_idf = {}
N = len(df)
for i in range(0, N):
    tokens = df['Content'][i]
    doc_length = len(tokens) # Total words in current document.
    counter = Counter(tokens) # How many times each word appears in current document.
    for token in np.unique(tokens): # np.unique is a numpy library that gives an !!array!! that contains words of a document without duplicates. It is also sorted in alphabetical order.
        tf = counter[token]/doc_length # Term Frequency
        dfreq = words_in_docs_num[token] # Document Frequency
        idf = np.log(N/(dfreq)) # Inverse Document Frequency. In this case we are sure we do not divide by 0, because all values in "words_in_docs_num" set are greater than 0. | a.k.a.: (dfreq>0). If not sure, use the code line below.
        #idf = np.log(N/(dfreq+1)) #As we cannot divide by 0, we smoothen the value by adding 1 to the denominator.
        tf_idf[i, token] = tf*idf  # i for document, token for word in document.

# *** WHAT TO EXPECT: xml file ***
#          <inverted_index>
#          <lemma name=”orange”>
#          <document id=”…” weight=”0.4”/>
#          <document id=”…” weight=”0.34”/>
#          </lemma>
#          <lemma name=”apple”>
#          <document id=”…” weight=”0.65”/>
#          <document =”…” weight=”0.87”/>
#          <document =”…” weight=”0.45”/>
#          </>
#          </>
# *** END OF WHAT TO EXPECT: xml file ***


# Create root element of our xml file called "inverted_index"
root = ET.Element("inverted_index")

# Append lemma and document subelements.
for word in words_in_docs:
    lemma = ET.SubElement(root, "lemma", {"name": word})
    docs_to_list = list(words_in_docs[word]) # words_in_docs[word] is a 'set' of documents, each document represented by an Integer. We convert the SET to a LIST to iterate though.

    for doc_id in docs_to_list:
        ET.SubElement(lemma, "document", {"id": str(psg['Hash'][doc_id]), "weight": str("%.4f" % tf_idf[doc_id, word])})
        # Assign 'hash' as the 'document id' and 'tfidf value' as the 'document weight' of our xml file.

# *** WAY 1 ***
# ElementTree is a wrapper class that corresponds to the "entire element hierarchy" providing serialization functionality - dumping and loading the tree. 
# Element, on the other hand, is a much "bigger" class that defines the Element interface.

# The ElementTree wrapper class is used to read and write XML files. Most ElementTree apis are simple wrappers around the root Element. 
# Simply put, ElementTree wraps the root Element (for convenience) and provides methods to serialize/deserialize the entire tree.

# Parse and create XML data (ElementTree). Then write XML data to output file named "inverted_index.xml" (write()).
#ET.ElementTree(root).write("inverted_index.xml")

# *OR*
# tree = ET.ElementTree(root)
# tree.write("inverted_index.xml")
# *** END OF WAY 1 ***

# *** WAY 2 ***

# Prettify xml and store to "inverted_index.xml" file.
pretty_xml = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
with open("inverted_index.xml", "w") as f:
    f.write(pretty_xml)

# *** END OF WAY 2 ***

# Calculate and print total execution time (seconds).
print("--- %s seconds ---" % (time.time() - start_time))