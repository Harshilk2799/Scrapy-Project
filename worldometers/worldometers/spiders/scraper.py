import scrapy


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country/"
    ]

    def parse(self, response):
        countries = response.css("tbody tr")
        for country in countries:
            countryName = country.css("a::text").get()
            link = country.css("a::attr(href)").get()

            # absolute_url = f"https://www.worldometers.info{link}"  # Method 1
            # absolute_url = response.urljoin(link)                  # Method 2
            # yield scrapy.Request(url=absolute_url, callback=self.getCountryPopulation)

            # Method 3
            yield response.follow(
                url=link,
                callback=self.getCountryPopulation,
                meta={"CountryName": countryName},
            )

    def getCountryPopulation(self, response):
        countryName = response.meta["CountryName"]
        rows = response.xpath(
            "(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr"
        )
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()

            yield {"CountryName": countryName, "Year": year, "Population": population}
