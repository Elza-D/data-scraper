# data-scraper
This repository contains a Scrapy spider that scrapes data from metacritic.com. The spider extracts information on video games, including title, release data, critic & user ratings, platform, genre, nr of user & critic review. The data is stored in a csv format and can be used for data analysis, visualization, and other research purposes.

To obtain the data, run the code, then open the termin and copy in the following: scrapy runspider scrapy_spider.py -o output.csv

You do need to install the scrapy libarary to run the code and get the data. 