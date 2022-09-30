import scrapy
from scrapy.http import FormRequest
from ..items import QuotesItem


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    # First Approach

    # Login With Credential
    # def parse(self, response):
    #     csrf_token = response.css("input").xpath("@value").get()
    #     yield FormRequest.from_response(
    #         response,
    #         formdata={
    #             "csrf_token": csrf_token,
    #             "username": "admin",
    #             "password": "password",
    #         },
    #         callback=self.parse_after_login,
    #     )

    # Second Approach
    def parse(self, response):
        csrf_token = response.css("input").xpath("@value").get()
        yield FormRequest(
            "https://quotes.toscrape.com/login",
            formdata={
                "csrf_token": csrf_token,
                "username": "admin",
                "password": "password",
            },
            callback=self.parse_after_login,
        )

    def parse_after_login(self, response):
        for data in response.css(".quote"):
            text = "".join(data.css(".text::text").get().split(";")).replace("'", "")
            author = data.css(".author::text").get()
            tags = data.css(".tag::text").getall()

            # Item Object
            item = QuotesItem()
            item["text"] = text
            item["author"] = author
            item["tags"] = tags
            yield item

        # Pagination
        next_page_url = response.css(".next a::attr(href)").get()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url, callback=self.parse_after_login)
