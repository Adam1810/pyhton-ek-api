import scrapy 

class QuotesSpider(scrapy.Spider):
    name = "ebayk"

    def start_requests(self):
        
        base_url = 'https://www.ebay-kleinanzeigen.de/s-sortierung:preis/lego-'
        append_url = '/k0'

        setId = [ 420009, 42029, 42055, 42078, 42094, 42100, 42107, 42108, 42109, 42110, 42111, 42112, 42114, 42115]
        urls = []
        for id in setId:
            new_url = base_url + str(id) + append_url
            urls.append(new_url)
        
     
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        title_list = response.css("title::text").get().split(' ')
        setid = title_list[1]

        for item in response.css("article.aditem"):
 
            uid = item.attrib['data-adid']
            details = item.css("div.aditem-details")
            description = item.css("div.aditem-main")
            description_text =  description.css("a.ellipsis::text").get()
            price = details.css("strong::text").get()
            versand = item.css("p.text-module-end")
            versand_true = versand.css("span::text").get()

            yield {
                'id': uid,
                'set-id': setid,
                'description': description_text,
                'price': price,
                'versand': versand_true,
            }