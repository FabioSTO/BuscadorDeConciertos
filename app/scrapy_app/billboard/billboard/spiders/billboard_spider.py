import scrapy

class BillboardSpider(scrapy.Spider):
    name = "billboard"
    start_urls = ["https://www.billboard.com/c/music/music-news/"]

    def parse(self, response):
        titles = response.css('h3.c-title a::text').extract()
        titles = [title.strip() for title in titles if title.strip()]
        
        for title in titles[:10]:
            yield {
                'title': title
            }