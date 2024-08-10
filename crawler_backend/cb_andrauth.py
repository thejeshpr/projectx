import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    extras = json.loads(obj.site_conf.extra_data_json)
    res = WebClient.get(base_url)

    if res.status_code == 200:
        jdata = res.json()

        for item in jdata["data"]["posts"]:
            data = (f"desc: {item['excerpt']}"
                    f"data: {item['date']}")
            obj.create_task(
                unique_key=item["ID"],
                name=f'[{item["topic"]}] - {item["title"]}',
                url=urllib.parse.urljoin(extras["artcile_base_url"], item["slug"]),
                data=data
            )
    else:
        logging.error(f"Error while fetching andrauth data: {res}")

