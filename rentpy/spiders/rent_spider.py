import scrapy
from ..utils import green_dorsal


class RentSpider(scrapy.Spider):
    name = "listprice"

    base_url = green_dorsal()
    city_url = "/city/1387/WA/Bellevue"
    start_urls = [
        f"{base_url}{city_url}",
    ]

    def parse(self, response):
        base_url = green_dorsal()
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

            yield response.follow(home_url, callback=self.parse_home)

        page_locator = response.css("div.viewingPage span.pageText::text").re(
            "Viewing page (\d+) of (\d+)"
        )
        current_page = int(page_locator[0])
        next_page = current_page + 1
        last_page = int(page_locator[1])

        if current_page < last_page:
            next_page = f"{base_url}{city_url}/page-{str(next_page)}"
            yield response.follow(next_page, callback=self.parse)

    def parse_home(self, response):
        street_address = response.css("h1.full-address div.street-address::text").get()
        city, _, state, _, zipcode = response.css(
            "h1.full-address div.bp-cityStateZip::text"
        ).getall()
        home_stats = response.css("div.home-main-stats-variant")
        listprice = (
            home_stats.css("div.stat-block")[0]
            .css("div.stat-block div.statsValue::text")
            .get()
        )
        num_beds = (
            home_stats.css("div.stat-block")[1]
            .css("div.stat-block div.statsValue::text")
            .get()
        )
        num_baths = (
            home_stats.css("div.stat-block")[2]
            .css("div.stat-block div.statsValue::text")
            .get()
        )
        area = (
            home_stats.css("div.stat-block")[3]
            .css("div.stat-block span.statsValue::text")
            .get()
        )
        listing_text = response.css("div.remarks p span::text").get()
        home_stats_dict = {
            "url": response.url,
            "street_address": street_address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "listprice": listprice,
            "num_beds": num_beds,
            "baths": num_baths,
            "sq_ft": area,
            "listing_text": listing_text,
        }
        yield home_stats_dict
