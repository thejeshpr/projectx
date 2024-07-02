import json
from urllib.parse import urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    # c-storiesNeonLatest_story xl:u-col-2 lg:u-col-2 md:u-col-2 sm:u-col-2 u-flexbox-column
    # c-storiesLatest_story xl:u-col-2 lg:u-col-2 md:u-col-3 sm:u-col-2 u-flexbox-column

    for a in soup.find_all('a', {'class': "c-storiesNeonLatest_story md:u-col-2 sm:u-col-2 u-flexbox-column lg:u-col-2"}):
        url = urljoin(base_url, a.get('href'))
        obj.create_task(
            unique_key=url,
            name=a.text.strip(),
            url=url
            # data=div.find('p').text.strip()
        )
