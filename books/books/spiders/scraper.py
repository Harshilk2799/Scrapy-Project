from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


def product_info(response, value):
    return response.xpath(
        '//th[text()="' + value + '"]/following-sibling::td/text()'
    ).get()


class ScraperSpider(CrawlSpider):
    name = "scraper"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    rule_book_details = Rule(
        LinkExtractor(restrict_css="h3 > a"), callback="parse_item", follow=False
    )
    rule_next_page = Rule(LinkExtractor(restrict_css="li.next a"), follow=True)

    rules = (rule_book_details, rule_next_page)

    def parse_item(self, response):
        title = response.css("h1::text").get()
        price = response.xpath("//*[@class='price_color']/text()").get()

        rating = response.xpath("//*[contains(@class, 'star-rating')]/@class").get()
        rating = rating.replace("star-rating", "")

        description = response.xpath(
            "//*[@id='product_description']/following-sibling::p/text()"
        ).get()

        # Product information data points

        upc = product_info(response, "UPC")
        product_type = product_info(response, "Product Type")
        price_without_tax = product_info(response, "Price (excl. tax)")
        price_with_tax = product_info(response, "Price (incl. tax)")
        tax = product_info(response, "Tax")
        availability = product_info(response, "Availability")
        number_of_reviews = product_info(response, "Number of reviews")

        yield {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Description": description,
            "UPC": upc,
            "Product_Type": product_type,
            "Price_Without_Tax": price_without_tax,
            "Price_With_Tax": price_with_tax,
            "Tax": tax,
            "Availability": availability,
            "Number_of_Reviews": number_of_reviews,
        }
