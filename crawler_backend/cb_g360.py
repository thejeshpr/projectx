import json

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    divs = soup.find_all('div', {'class': 'caption_box'})

    for div in divs:
        a = div.find('a')
        obj.create_task(
            unique_key=a.get('href'),
            name=a.text.strip(),
            url=a.get('href')
        )
