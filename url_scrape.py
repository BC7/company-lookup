import scrapy
import result_item
import csvmanager
import sys

from csvmanager import CsvManager
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from result_item import StackItem
class CompanySearchSpider(scrapy.Spider):
    #spider process

    # Base URL for a google search
    BASE_GOOGLE_URL="https://www.google.com/search?sclient=psy-ab&hl=en&site=webhp&source=hp&btnG=Search&q="
    name = 'companysearch'

    start_urls = []
    download_delay = 2

    manager = CsvManager(sys.argv[1])
    orgData = manager.getOrgs()
    csvdata = [len(orgData)]

    def start_requests(self):
        i = 1
        for key in self.orgData.keys():
            self.start_urls.append(self.BASE_GOOGLE_URL + key.replace(' ', '+'))
            i += 1

        i = 0
        for url in self.start_urls:
            # for data in self.orgData[self.start_urls.index(url)]:
            # self.csvdata[self.start_urls.index(url)] = self.orgData[self.start_urls.index(url)]
                # i += 1
            yield scrapy.Request(url=url, dont_filter=True, callback=self.results_parse)


    def results_parse(self, response):
        # Selector and xpaths based on google search results
        # Will need to modify to support crawling multiple search engines (If that is required later during development)
        searchedOrg = {}
        searchedOrg[0] = response.url[len(self.BASE_GOOGLE_URL):].replace("+", " ")
        potentialresources = Selector(response).xpath('//div[@class="g"]')
        for i in range (0, 6):
            link = potentialresources[i]
            linkextract = link.xpath('//h3[@class="r"]/a/@href').extract()[i]
            item = StackItem()
            item['title'] = link.xpath('//h3[@class="r"]/a/text()').extract()[i]
            item['url'] = linkextract[7:linkextract.find("&sa=U&ved")]


            yield scrapy.Request(url=item['url'], callback=self.scanLinks, meta=searchedOrg, dont_filter=True)

    def scanLinks(self, response):
        # # print("\n\n\nTEST: " + str(response.meta[0]))
        print("\n\nWorking on url: "+ response.url+"\nWith given meta for org: " + str(response.meta[0]))


        # check if url is owned by the company (minimal check since vartions can happen in a domain)
        if str(response.meta[0]).replace(" ", "") in str(response.url):
            print("LINK IS USEFULLL\n\n\n")
            self.addlink(str(response.meta[0]), str(response.url))


        # check if page mentions a company email
        if str(response.meta[0]).replace(" ", "") in str(response.body):
            print("LINK IS USEFULLL\n\n\n")
            self.addlink(str(response.meta[0]), str(response.url))

        # checks if page mentions company in any way
        if "Ltd" in response.meta[0]:
            if str(response.meta[0]) in str(response.body):
                print("LINK IS USEFULLL\n\n\n")
                self.addlink(str(response.meta[0]), str(response.url))
        elif "Limited" in response.meta[0]:
            if str(response.meta[0].replace("Limited", "Ltd")) in str(response.body):
                print("LINK IS USEFULLL\n\n\n")
                self.addlink(str(response.meta[0]), str(response.url))
        elif response.meta[0] in str(response.body):
            print("LINK USEFULL\n\n\n")
            self.addlink(str(response.meta[0]), str(response.url))

        # checks if page mentions company address from adreess columns or city
        if self.orgData[response.meta[0]][0] in str(response.body):
            print("Link USEFULLLL\n\n")
            self.addlink(str(response.meta[0]), str(response.url))
        elif self.orgData[response.meta[0]][1] in str(response.body):
            print("Link USEFULLLL\n\n")
            self.addlink(str(response.meta[0]), str(response.url))
        elif self.orgData[response.meta[0]][3] in str(response.body):
            print("Link USEFULLLL\n\n")
            self.addlink(str(response.meta[0]), str(response.url))

        self.manager.updateCSV(self.orgData)

    def addlink(self, key, url):
        # check if cell isn't populated with a link already
        # if it is, check the next available cell
        if self.orgData[key][4] == "":
            self.orgData[key][4] = str(url)
        elif self.orgData[key][5] == "":
            self.orgData[key][5] = str(url)
        elif self.orgData[key][6] == "":
            self.orgData[key][6] = str(url)
        # elif self.orgData[key][7] == "":
        #     self.orgData[key][7] = str(url)

        print("Url added\n" + str(self.orgData[key]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Error: Please specify path to csv file..')
        sys.exit()
    else:
        # Webcrawler process
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(CompanySearchSpider)
        process.start() # the script will block here until the crawling is finished