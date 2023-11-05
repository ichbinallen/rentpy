# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentpyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HomeItem(scrapy.Item):
    url = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    listprice = scrapy.Field()
    num_beds = scrapy.Field()
    num_baths = scrapy.Field()
    sq_ft = scrapy.Field()
    listing_text = scrapy.Field()
