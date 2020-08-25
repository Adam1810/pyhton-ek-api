import scrapy
import json


class QuotesSpider(scrapy.Spider):
    name = "ebayk"

    @staticmethod
    def clean(sValue):

        temp = sValue.replace(' ', '')
        temp = temp.replace('<br>', '')
        temp = temp.replace('\n', '')

        return temp

    @staticmethod
    def getUrls ():
            
        with open('config.json', 'r') as f:
            config = json.load(f)

        baseUrl = config['DEFAULT']['baseUrl']
        sortingUrl = config['DEFAULT']['sortingUrl']
        legoUrl = config['DEFAULT']['legoUrl']
        siteUrl = config['DEFAULT']['siteUrl']
        appendUrl = config['DEFAULT']['appendUrl']


        setId = config['SETS']
        urls = []

        for l in setId:

            temp = str(l['setId'])

            new_url = baseUrl + sortingUrl + legoUrl + temp + appendUrl  
            urls.append(new_url)

            if l['site'] > 1:
                new_url = baseUrl + sortingUrl + siteUrl + legoUrl + temp + appendUrl  
                urls.append(new_url)

        return urls

    def start_requests(self):
        
        urls = self.getUrls()
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        base_url = 'https://www.ebay-kleinanzeigen.de'
        title_list = response.css("title::text").get().split(' ')
        setid = title_list[1]

        for item in response.css("article.aditem"):
 
            uid = item.attrib['data-adid']
            description =  item.css("div.aditem-main a.ellipsis::text").get()
            price =item.css("div.aditem-details strong::text").get()
            versand = item.css("p.text-module-end span::text").get()
            link = base_url + item.css("div.aditem-main a.ellipsis::attr(href)").get()
            added = item.css("div.aditem-addon::text").get()

            loc = item.css("div.aditem-details").get()
            a = loc.split('\n')
            plz = self.clean(a[3])
            city = self.clean(a[4])

            yield {
                'id': uid,
                'set-id': setid,
                'description': description,
                'price': price,
                'versand': versand,
                'link': link,
                'added': added,
                'cityCode': plz,
                'city': city
            }