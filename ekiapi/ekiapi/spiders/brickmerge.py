import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "brickmerge"

    @staticmethod
    def clean(sValue):

        temp = sValue.replace('\xa0€', '')

        return temp

    @staticmethod
    def getUrls ():
            
        with open('configN.json', 'r') as f:
            config = json.load(f)

        baseUrl = config['DEFAULT']['baseUrl']


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
        strong = r.css("strong::text").getall()

        yield {
            'set-id': strong[3],
            'description': strong[2],
            'price': self.clean(strong[9]),
            'POV': self.clean(strong[11]),
            'Rate': strong[13]
        }