import json
from urllib.parse import urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for a in soup.find_all('a', {'class': "c-storiesLatest_story xl:u-col-2 lg:u-col-2 md:u-col-3 sm:u-col-2 u-flexbox-column"}):
        url = urljoin(base_url, a.get('href'))
        obj.create_task(
            unique_key=url,
            name=a.text.strip(),
            url=url
            # data=div.find('p').text.strip()
        )
