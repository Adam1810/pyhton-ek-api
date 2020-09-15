import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "brickmerge"

    @staticmethod
    def clean(sValue):

        temp = sValue.replace(' €', '')

        return temp

    @staticmethod
    def getUrls ():
            
        with open('config.json', 'r') as f:
            config = json.load(f)

        baseUrl = config['DEFAULT']['brickmergeUrl']


        setId = config['SETS']
        urls = []

        for l in setId:

            temp = str(l['setId'])

            new_url = baseUrl + temp  
            urls.append(new_url)

        return urls

    def start_requests(self):
        
        urls = self.getUrls()
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        r = response.css("div.medium-4")
        price = r.css("span.theprice::text").get()

        strong = r.css("strong::text").getall()

        yield {
            'set-id': strong[3],
            'description': strong[2],
            'UVP': strong[8],
            'price': self.clean(price),
            'POV': self.clean(strong[11])
        }