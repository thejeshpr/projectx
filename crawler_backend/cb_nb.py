import json
import logging
import time
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    extras = json.loads(obj.site_conf.extra_data_json)
    base_url = base_url.format(searchParam=extras["searchParam"])

    res = WebClient.get(base_url)

    if res.status_code == 200:
        data = res.json()["data"]
        for item in data:
            logging.debug("processing item: {}".format(item))
            availableFrom = int(str(item["availableFrom"])[:-3])
            availableFrom = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(availableFrom))
            data = (f"plotArea: {item.get('plotArea')}\n"
                    f"pricePerUnit: {item.get('pricePerUnit')}\n"
                    f"completeStreetName: {item.get('completeStreetName')}\n"
                    f"address: {item.get('address')}\n"
                    f"location: {item.get('location')}\n"
                    f"availableFrom: {availableFrom}\n")
            obj.create_task(
                unique_key=item["id"],
                name=f'{item["propertyTitle"]}-{item["formattedPrice"]}',
                url=item["shortUrl"],
                data=data
            )
    else:
        logging.error(f"failed to scrape item: cb_nb: {res.content}")
