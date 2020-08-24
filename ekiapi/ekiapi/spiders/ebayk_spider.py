import scrapy 

class QuotesSpider(scrapy.Spider):
    name = "ebayk"

    @staticmethod
    def clean(sValue):

        temp = sValue.replace(' ', '')
        temp = temp.replace('<br>', '')
        temp = temp.replace('\n', '')

        return temp


    def start_requests(self):
        
        base_url = 'https://www.ebay-kleinanzeigen.de'
        sorting_url = '/s-sortierung:preis/lego-'
        append_url = '/k0'

        setId = [ 420009, 42029, 42055, 42078, 42094, 42100, 42107, 42108, 42109, 42110, 42111, 42112, 42114, 42115]
        urls = []
        for id in setId:
            new_url = base_url + sorting_url + str(id) + append_url
            urls.append(new_url)
        
     
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