import scrapy


class RentSpider(scrapy.Spider):
    name = "listprice"
    part1 = "htt" + "ps://w" + "ww.re"
    part2 = "dfi" + "n.com"
    base_url = part1 + part2
    city_url = "/city/1387/WA/Bellevue"
    start_urls = [
        f"{part1}{part2}{city_url}",
    ]

    def parse(self, response):
        part1 = "htt" + "ps://w" + "ww.re"
        part2 = "dfi" + "n.com"
        base_url = part1 + part2
        city_url = "/city/1387/WA/Bellevue"

        homes = response.css("div.HomeCardContainer div.bottomV2")
        for home in homes:
            price = home.css("div.bottomV2 span.homecardV2Price::text").get()
            stats = home.css("div.HomeStatsV2 div.stats::text").getall()
            beds = stats[0]
            baths = stats[1]
            area = stats[2]
            address = home.css("a div.link-and-anchor::text").get()
            home_url = home.css("a").attrib.get("href")
            home_url = base_url + home_url

            yield {
                "price": price,
                "beds": beds,
                "baths": baths,
                "area": area,
                "address": address,
                "url": home_url,
            }

        page_locator = response.css("div.viewingPage span.pageText::text").re(
            "Viewing page (\d+) of (\d+)"
        )
        current_page = int(page_locator[0])
        next_page = current_page + 1
        last_page = int(page_locator[1])

        if current_page < last_page:
            next_page = f"{base_url}{city_url}/page-{str(next_page)}"
            print(next_page)
            yield response.follow(next_page, callback=self.parse)
