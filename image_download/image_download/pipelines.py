from scrapy.pipelines.images import ImagesPipeline
from slugify import slugify

# class ImageDownloadPipeline:
#     def process_item(self, item, spider):
#         return item


class CustomImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = slugify(item["title"])
        return f"full/{file_name}.jpg"
