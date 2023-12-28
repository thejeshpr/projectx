import json
import urllib
from urllib.parse import urlparse, urljoin
from uuid import uuid4

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for article in soup.find_all('article', {"class": "Box-row"}):
        a = article.find('a', {'class': "Link"})
        p = article.find('p')
        data = p.text.strip() if p else ""


        obj.create_task(
            unique_key=str(uuid4()),
            name=a.text.strip(),
            url=f"{extras.get('artcile_base_url')}{a.get('href')}",
            data=data
        )
