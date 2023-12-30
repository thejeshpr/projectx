import json

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    divs = soup.find_all('div', {'class': 'sc-3kpz0l-7 ezIqDt'})

    for div in divs:
        a = div.find('a')
        if a:
            p = div.find_next('div').find('p')
            data = p.text.strip() if p else ""
            obj.create_task(
                unique_key=a.get('href'),
                name=a.text.strip(),
                url=a.get('href'),
                data=data
            )
