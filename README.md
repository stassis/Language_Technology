# Language_Technology
This project is about creating a search engine that works in real life articles, like other well-known search engines.

First of all, we scrape articles using scrapy. Then we preprocess them and create an index that can be searched in a time-efficient way using python.

Finally, we may search the articles using a command line interface.

## Download scrapy
- [Download scrapy here](https://scrapy.org/)
- [Installation Guide here](https://docs.scrapy.org/en/latest/intro/install.html)

### Download the articles
Initialize your scrapy spider and then copy/paste the spiders provided. Then, run each spider and collect as many atricles as you want.

You may enable or disable sleep() function in each spider, in order to avoid getting blocked. Sleep seconds may vary from page to page in general.

### Contents of csv files
- Title
- Content
- URL
- URL-Hash

## Create Inverted Index

### Make sure you have the following packages installed
- pandas
- nltk

### Run files in the following order
- html_clean.py
- token_postag.py
- stemcount.py
- create_inverted_index.py
- read_n_query.py

## Open CSV's
To display correctly the contents of a csv in excel click [here](https://techcommunity.microsoft.com/t5/excel/open-and-edit-a-csv-file-in-utf8/m-p/1035653/highlight/true#M45222)

Alternatively download [Libre Office](https://www.libreoffice.org/)

## Terminal
You may use cmd or any terminal of your choice.

This has been tested on [Anaconda Prompt terminal](https://www.anaconda.com/products/individual)

Python 3.7 is recommended