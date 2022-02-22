import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import time
# import re
# import string

# Get start time to calculate execution time.
start_time = time.time()

# Import html cleared dataframe.
df = pd.read_csv('html_cleared.csv')

# Remove punctuations.
df['Content'] = df['Content'].str.replace('[^\w\s]',' ')

# Convert to lower so that all stopwords are removed.
df['Content'] = df['Content'].str.lower()

# Remove non word characters a.k.a. Numbers, Symbols.
df['Content'] = df['Content'].str.replace('[^a-zA-Z]',' ')

# Create word vector (tokenize) | Another way to tokenize: regexp_tokenize(z, pattern=r"(?:(?!\d)\w)+|\S+")
df['Content'] = df.apply(lambda row: word_tokenize(str(row['Content'])), axis=1)

# Remove common words (stopwords) - (closed class categories)
stop_words = set(stopwords.words('english'))
df['Content'] = df['Content'].apply(lambda x: [ y for y in x if y not in stop_words])

# POS tag each token(word)
df['Content'] = df['Content'].apply(lambda row: pos_tag(row))

# Define closed class categories POS tags.
CLOSED_TAGS = {'CD', 'CC', 'DT', 'EX', 'IN',
				   'LS', 'MD', 'PDT', 'POS', 'PRP',
				   'PRP$', 'RP', 'TO', 'UH', 'WDT',
				   'WP', 'WP$', 'WRB'}


# Remove tuples (word,POStag) that have closedclasscategorytag assigned
# x represents a row in our csv file
# y represents a tuple in a row: (word,POStag)
# y[1] represents the POStag
df['Content'] = df['Content'].apply(lambda x: [ y for y in x if y[1] not in CLOSED_TAGS])

# Export Dataframe to CSV.
df.to_csv( "postagged.csv", index=False, encoding='utf-8-sig')

# Calculate and print total execution time (seconds).
print("--- %s seconds ---" % (time.time() - start_time))