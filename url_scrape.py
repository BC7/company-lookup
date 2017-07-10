import scrapy
import result_item
import csvmanager

from csvmanager import CsvManager
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from result_item import StackItem
class CompanySearchSpider(scrapy.Spider):
    #spider process

    # Base URL for a google search
    BASE_URL="https://www.google.com/search?sclient=psy-ab&hl=en&site=webhp&source=hp&btnG=Search&q="
    name = 'companysearch'
    allowed_domains = ["google.com"]
    start_urls = []
    download_delay = 2

    def start_requests(self):
        self.manager = CsvManager("smaller_dataset.csv")
        self.orgData = self.manager.getOrgs()
        i = 1
        for i in range(1, len(self.orgData)):
            self.start_urls.append(self.BASE_URL + self.orgData[i][0].replace(' ', '+'))
            i += 1

        for url in self.start_urls:
            meta = {}
            meta['data'] = self.orgData[self.start_urls.index(url)]
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)


    def parse(self, response):
        # Selector and xpath based on google search results
        # Will need to modify to support crawling multiple search engines (If that is required later during development)
        scanMarker = 0
        potentialresources = Selector(response).xpath('//div[@class="g"]')
        for i in range (0, 6):
            meta = {}
            link = potentialresources[i]
            linkextract = link.xpath('//h3[@class="r"]/a/@href').extract()[i]
            item = StackItem()
            item['title'] = link.xpath('//h3[@class="r"]/a/text()').extract()[i]
            item['url'] = linkextract[7:linkextract.find("&sa=U&ved")]

            # daisy chaining meta information to scan for on the found links
            meta['data'] = response.meta['data']
            yield scrapy.Request(url=item['url'], callback=self.scanLinks, meta=meta)

    def scanLinks(self, response):
        print(response.meta['data'][0][0]+"\n\n\n"+"wtffff")

# Webcrawler process
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


process.crawl(CompanySearchSpider)
process.start() # the script will block here until the crawling is finished