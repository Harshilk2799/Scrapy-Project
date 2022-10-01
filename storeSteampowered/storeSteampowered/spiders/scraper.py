import scrapy
from ..items import SteampoweredItem
from w3lib.html import remove_tags
from scrapy.loader import ItemLoader


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?filter=topsellers"]

    def parse(self, response):
        games = response.css("div#search_resultsRows a")

        for game in games:
            loader = ItemLoader(
                item=SteampoweredItem(), selector=game, response=response
            )
            loader.add_css("game_url", "a::attr(href)")
            loader.add_css("img_url", "a div.col.search_capsule img::attr(src)")
            loader.add_css(
                "game_name", "a .responsive_search_name_combined span.title::text"
            )
            loader.add_css(
                "release_date",
                "a .responsive_search_name_combined div.search_released::text",
            )
            loader.add_xpath(
                "platforms",
                ".//span[contains(@class, 'platform_img') or @class='vr_supported' or @class='music']/@class",
            )
            loader.add_xpath(
                "reviews_summary",
                ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html",
            )
            loader.add_css("discount_rate", ".search_discount span::text")
            loader.add_xpath(
                "original_price",
                ".//div[contains(@class, 'search_price_discount_combined')]",
            )
            loader.add_css(
                "discount_price",
                "div.search_price_discount_combined div.search_price.discounted::text",
            )

            yield loader.load_item()

        for i in range(2, 10):
            page_url = f"https://store.steampowered.com/search/?sort_by=&sort_order=0&filter=topsellers&page={str(i)}"
            yield scrapy.Request(url=page_url, callback=self.parse)
