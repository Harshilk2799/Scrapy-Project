import scrapy
from scrapy.http import Request


class ImdbSpiderSpider(scrapy.Spider):
    name = "imdb_spider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def parse(self, response):
        movies = response.css(".titleColumn>a::attr(href)").getall()
        for movie in movies:
            url = response.urljoin(movie)
            yield Request(url, callback=self.parse_movie, meta={"URL": url})

    def parse_movie(self, response):
        url = response.meta["URL"]
        movie_name = response.css("section.ipc-page-section h1::text").get()

        rating = response.css(
            "div[class='sc-7ab21ed2-2 kYEdvH'] span[class='sc-7ab21ed2-1 jGRxWM']::text"
        ).get()

        image_links = response.urljoin(
            response.css(
                "div[class='ipc-photo ipc-photo--base ipc-photo--dynamic-width photos-image ipc-sub-grid-item ipc-sub-grid-item--span-2'] a[class='ipc-lockup-overlay ipc-focusable']::attr(href)"
            ).get()
        )

        movie_description = response.css(
            "span[role='presentation']:nth-child(3)::text"
        ).get()

        cast_name = response.css(
            "div[data-testid='title-cast-item'] a[data-testid='title-cast-item__actor']::text"
        ).getall()

        director_name = response.css(
            "div[data-testid='title-pc-wide-screen'] li:nth-child(1) li a::text"
        ).getall()

        writer_name = response.css(
            "div[data-testid='title-pc-wide-screen'] li:nth-child(2) li a::text"
        ).getall()

        stars = response.css(
            "div[data-testid='title-pc-wide-screen'] li:nth-child(3) li a::text"
        ).getall()

        yield {
            "URL": url,
            "Movie_name": movie_name,
            "Rating": rating,
            "Movie_Description": movie_description,
            "Cast_name": cast_name,
            "Director_name": director_name,
            "Writer_name": writer_name,
            "Stars": stars,
            "Image_link": image_links,
        }
