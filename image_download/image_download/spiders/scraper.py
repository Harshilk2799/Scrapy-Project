import scrapy
from ..items import ImageDownloadItem
from itemloaders import ItemLoader


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css("h3 a::attr(href)").getall()
        for book in books:
            absolute_url = response.urljoin(book)
            yield scrapy.Request(absolute_url, callback=self.parse_book)

        # Paginations

        # next_page_url = response.css("li[class='next'] a::attr(href)").get()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield scrapy.Request(absolute_next_page_url)

    def parse_book(self, response):
        l = ItemLoader(item=ImageDownloadItem(), selector=response)
        title = response.css("h1::text").get()
        price = response.css("p[class='price_color']::text").get()

        image_urls = response.css("img::attr(src)").get()
        image_urls = image_urls.replace("../../", "https://books.toscrape.com/")

        l.add_value("title", title)
        l.add_value("price", price)
        l.add_value("image_urls", image_urls)

        yield l.load_item()
