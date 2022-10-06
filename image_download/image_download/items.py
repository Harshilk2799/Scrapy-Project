import scrapy
from itemloaders.processors import TakeFirst, MapCompose


class ImageDownloadItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    image_urls = scrapy.Field()
    images = scrapy.Field()
