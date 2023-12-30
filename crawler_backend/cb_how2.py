import json
from urllib.parse import urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for div in soup.find_all('div', {'class': "responsive_thumb"}):
        obj.create_task(
            unique_key=div.find('a').get('href'),
            name=div.find('a').text.strip(),
            url=div.find('a').get('href')
            # data=div.find('p').text.strip()
        )
