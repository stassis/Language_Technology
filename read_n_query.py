import xml.etree.ElementTree as ET
import time
import pandas as pd
#from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import operator

# Get start time to calculate execution time.
start_time = time.time()

psg = pd.read_csv('postagged.csv')
df = pd.read_csv('words.csv', converters={'Content': eval})


# Read and store "inverted_index.xml" to memory.
FILE_NAME = "inverted_index.xml"
inv_index = {}
tree = ET.ElementTree()
tree.parse(FILE_NAME)

for lemma in list(tree.iter("lemma")):
        word = lemma.attrib['name']
        inv_index[word] = {}
        for doc in list(lemma.iter("document")):
            doc_id = doc.attrib['id']
            tfidf = float(doc.attrib['weight'])
            inv_index[word][doc_id] = tfidf


print("\n") 
# Calculate and print total execution time (seconds).
print("--- %s seconds to load XML index---" % (time.time() - start_time))            
print("\n") 

while True:
    print("\n") 
    exit_or_go = input('"go" to Google | "exit" to Exit:')

    if  exit_or_go=='exit':
        break


    if exit_or_go == "go":    
        print("\n") 
        USER_INPUT = list(input('Google:').split(" "))

        # Store start time since a user started a query.
        start_time = time.time()

        # Convert query to pure string in order to print it in a user-friendly way.
        input_to_string = ' '.join([str(elem) for elem in USER_INPUT])

        print("\n") 
        # Print Query String.   |->Quote string
        print(' **** Query ', '"{}"'.format(input_to_string), '**** ')
        print("\n") 

        # Stem/Lemmatize input words, in order to search the index file. Index file has stemmed/lemmatized words
        # stored. Hence, will not work if we don't stem/lemmatize input.
        for i in range(len(USER_INPUT)):
            #USER_INPUT[i] = PorterStemmer().stem(str.lower(USER_INPUT[i]))
            USER_INPUT[i] = WordNetLemmatizer().lemmatize(str.lower(USER_INPUT[i]))


        # Store all documents that contain each query word (along with their tfidf's).
        # input_docs = {}
        # for word in USER_INPUT:
        #     input_docs[word] = inv_index[word].copy()    


        # Create a 'Set' that contains each document hash only once as keys and
        # the sum of all word tfidf's that the document has as values.
        document_score = {}

        for word in USER_INPUT:
            try:
                for hash_ in inv_index[word]:
                    if hash_ in document_score:
                        document_score[hash_] += float("{:.2f}".format(inv_index[word][hash_]))
                    else:
                        document_score[hash_] = float("{:.2f}".format(inv_index[word][hash_]))
            except:
                print('No such word found! :/')            


        # Sort the set that we previously created by descending tfidf value.
        # IMPORTANT_NOTE: Now 'document_score' is a 'list' and not a 'Set' because 
        # 'sorted' function converts it to a list.
        document_score = sorted(document_score.items(), key=operator.itemgetter(1),reverse=True)


        # Print 'Hash - Title' of retrieved documents in descending tfidf order.
        # We set a threshold to obtain more relevant documents.
        # Threshold is the minimum amount of tfidf sum of words that a document can have.
        THRESHOLD = 0.01
        for hash_ in document_score:
            if hash_[1] > THRESHOLD: # hash_[1] is tfidf value. | hash_[0] is the hash value itself.
                title = psg.loc[psg['Hash'] == hash_[0]].index[0] # Obtain the row index of the Hash. | '.index' returns: "Int64Index([5952], dtype='int64')". | '.index[0]' returns 5952 a.k.a. the row integer(index).
                print(hash_[0], "--", psg['Title'][title])
            else:
                break 
                # There is no need to search further because for loop selects tuples from start index to last index
                # and 'document_score' is stored in descending order,
                # meaning the ones to come will have a tfidf below threshold.
                # Eventually we 'cut off' unnecessary for loop iterations and speed up the execution.
        
        print("\n") 
        # Calculate and print Query time (seconds).
        print("--- %s seconds to finish query ---" % (time.time() - start_time))     
