import scrapy


class QuotesSpider(scrapy.Spider):
    name = "listprice"
    part1 = "htt" + "ps://w" + "ww.re"
    part2 = "dfi" + "n.com"
    base_url = part1 + part2
    start_urls = [
        f"{part1}{part2}/city/1387/WA/Bellevue",
    ]

    def parse(self, response):

        homes = response.css('div.HomeCardContainer div.bottomV2')
        for home in homes:

            price = home.css("div.bottomV2 span.homecardV2Price::text").get()
            stats = home.css('div.HomeStatsV2 div.stats::text').getall()
            beds = stats[0]
            baths = stats[1]
            area = stats[2]
            address = home.css('a div.link-and-anchor::text').get()

            yield {
                "price": price,
                "beds": beds,
                "baths": baths,
                "area": area,
                "address": address,
            }
