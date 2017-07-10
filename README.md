# company-lookup
code assessment 



NOTE:
Code requires scrapy and python version 3 or higher to be installed on the machine prior to use.

There were many features I would have further liked to implement such as accepting separate csv files as arguments.

Currently in order to upload a csv file, you have to manually change line 20 of url_scrape.py. I optimized it to support multiple search engines (hence the odd base url, and the addition parsing for google results) if the need ever came up. Rather than using a specific google crawler, I used scrapy and routed searches through google's NoScript site, seeing as results normally appear due to java script. As I was preparing the files, the second parsing started to fail however I didn't want to miss the deadline.

to run, cd into the directory and run url_scrape.py
