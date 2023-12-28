import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for item in res.json().get('results'):
        name = f"{item.get('model')} - {item.get('price')}"
        url = urllib.parse.urljoin(extras.get("item_base_url"), item.get('permanent_url'))

        data = f"Fuel: {item.get('fuel_type')}\n" \
               f"Year: {item.get('make_year')}\n" \
               f"Variant: {item.get('variant')}\n" \
               f"KM: {item.get('mileage')}\n" \
               f"Owner: {item.get('no_of_owners')}\n" \
               f"Shortlist Count: {item.get('shortlist_count')}\n"

        obj.create_task(
            unique_key=item.get("id"),
            name=name,
            url=url,
            data=data
        )

