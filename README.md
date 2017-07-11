# company-lookup
code assessment 



NOTE:
Code requires scrapy and python version 3 or higher to be installed on the machine prior to use.

I optimized it to support multiple search engines (hence the odd base url, and the addition parsing for google results) if the need ever came up, I'll just have to add another BASE_URL to match whichever search engine you wish to implement. Rather than using a specific google crawler, I used scrapy and routed searches through google's NoScript site, seeing as results normally appear due to javascript.

to run, cd into the directory and run the command:
"python url_scrape.py "path/to/csv/file.csv"
