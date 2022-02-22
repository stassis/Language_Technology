import pandas as pd
import re
import glob
import os
from time import sleep
import time

# ------------------ WAY 1 to combine all csv's to one ------------------

# Get start time to calculate execution time.
start_time = time.time()

os.chdir("Your path to articles here")

extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))] |||| alternatively: 
all_filenames = [i for i in glob.glob('*.csv'.format(extension))] #if we have multiple files in directory other than csv's

# Combine all files in the list.
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# Export to csv.
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
sleep(2)
# ------------------ END OF WAY 1  ------------------



# ------------------ WAY 2 to combine all csv's to one ------------------

# path = "C:\\Users\\Stefanos\\Desktop\\scrapy\\gl_tech" # path to all csv's
# all_csvs = glob.glob(path + "\\*.csv")

# li = []

# for csv_file in all_csvs:
#     df = pd.read_csv(csv_file, index_col=None, header=0) #header=0: after reading csv, first row can be assigned as the column names
#     li.append(df)

# csvs_concatenated = pd.concat(li, axis=0, ignore_index=True)
# csvs_concatenated.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')

# ------------------ END OF WAY 2  ------------------



# Get latest csv file, which is going to be the concatenated csv that we created above.
combined_csv_file = max(glob.iglob('*.csv'),key=os.path.getctime)
os.rename(combined_csv_file,'combined.csv')


# Remove HTML tags of Contents.
combined = pd.read_csv('combined.csv')
html_tags = re.compile('<.*?>')
combined['Content'] = combined['Content'].astype(str).apply(lambda row: re.sub(html_tags,'',row))
combined.to_csv( "html_cleared.csv", index=False, encoding='utf-8-sig')

# Calculate and print total execution time (seconds).
print("--- %s seconds ---" % (time.time() - start_time))