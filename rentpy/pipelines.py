# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RentpyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Remove Leading & Trailing Whitespace
        field_names = adapter.field_names()
        for fn in field_names:
            if fn not in ["listing_text", "description"]:
                value = adapter.get(fn)
                if value is not None:
                    adapter[fn] = value.strip()

        # Process State
        state = adapter.get("state")
        state = state.upper()
        adapter["state"] = state

        # Zipcodes should be 5 digit leftpadded strings
        zipcode = adapter.get("zipcode")
        zipcode = zipcode.zfill(5)
        adapter["zipcode"] = zipcode

        # Listprice
        price_keys = ["listprice"]
        listprice = adapter.get("listprice")
        listprice = listprice.strip()
        listprice = value.replace("$", "")
        listprice = value.replace(",", "")
        adapter["listprice"] = float(listprice)

        # Bedrooms
        num_beds = adapter.get("num_beds")
        if num_beds is not None:
            adapter["num_beds"] = int(num_beds.strip())

        # Bathrooms
        num_baths = adapter.get("num_baths")
        if num_baths is not None:
            adapter["num_baths"] = float(num_baths.strip())

        # Area
        # TODO: handle case when sq_ft field contains acres
        sq_ft = adapter.get("sq_ft")
        if "-" in sq_ft:
            adapter["sq_ft"] = None
        else:
            sq_ft = sq_ft.replace(",", "")
            adapter["sq_ft"] = float(sq_ft)

        return item
