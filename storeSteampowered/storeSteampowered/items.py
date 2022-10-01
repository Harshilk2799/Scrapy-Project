import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
from scrapy.selector import Selector


def get_original_price(html_markup):
    original_price = ""
    selector_obj = Selector(text=html_markup)
    div_with_discount = selector_obj.xpath(
        ".//div[contains(@class, 'search_price discounted')]"
    )
    if len(div_with_discount) > 0:
        original_price = div_with_discount.xpath(".//span/strike/text()").get()
    else:
        original_price = selector_obj.xpath(
            ".//div[contains(@class, 'search_price')]/text()"
        ).get()

    return original_price


def get_platforms(one_classes):
    platforms = []
    platform = one_classes.split(" ")[-1]
    if platform == "win":
        platforms.append(platform)
    if platform == "linux":
        platforms.append(platform)
    if platform == "music":
        platforms.append(platform)
    if platform == "mac":
        platforms.append(platform)
    if platform == "vr_supported":
        platforms.append(platform)

    return platforms


def remove_html(review_summary):
    cleaned_review_summary = ""
    try:
        cleaned_review_summary = remove_tags(review_summary)
    except TypeError:
        cleaned_review_summary = "No Review"
    return cleaned_review_summary


def clean_discount_rate(discount_rate):
    if discount_rate:
        return discount_rate.lstrip("-")

    return discount_rate


def clean_discount_price(discount_price):
    if discount_price:
        return discount_price.strip()
    return discount_price


class SteampoweredItem(scrapy.Item):
    game_url = scrapy.Field(output_processor=TakeFirst())
    img_url = scrapy.Field(output_processor=TakeFirst())
    game_name = scrapy.Field(output_processor=TakeFirst())
    release_date = scrapy.Field(output_processor=TakeFirst())
    platforms = scrapy.Field(input_processor=MapCompose(get_platforms))
    reviews_summary = scrapy.Field(
        input_processor=MapCompose(remove_html), output_processor=TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor=MapCompose(get_original_price, str.strip),
        output_processor=Join(""),
    )
    discount_price = scrapy.Field(
        input_processor=MapCompose(clean_discount_price), output_processor=TakeFirst()
    )
    discount_rate = scrapy.Field(
        input_processor=MapCompose(clean_discount_rate), output_processor=TakeFirst()
    )
