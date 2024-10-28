import scrapy

class MobileSpecsSpider(scrapy.Spider):
    name = "mobile_specs"
    
    start_urls = [
        "https://www.gsmarena.com/" 
    ]
    
    def parse(self, response):

        for link in response.css("a.mobile-link::attr(href)").getall():
            yield response.follow(link, callback=self.parse_mobile)

  
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_mobile(self, response):

        self.logger.info('Parsing mobile page: %s', response.url)


        model = response.css("h1.mobile-title::text").get()
        price = response.css("span.price::text").get()
        processor = response.css("div.specs .processor::text").get()
        ram = response.css("div.specs .ram::text").get()
        storage = response.css("div.specs .storage::text").get()
        battery = response.css("div.specs .battery::text").get()


        if model is None:
            self.logger.warning('No model found for URL: %s', response.url)

        if model and price:
            yield {
                "model": model,
                "price": price,
                "processor": processor,
                "ram": ram,
                "storage": storage,
                "battery": battery,
            }
