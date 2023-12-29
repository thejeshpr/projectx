from urllib.parse import urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for div in soup.find_all('div', {'class': "w-display-card-content"}):
        a = div.find('a')
        if a:
            p = div.find('p')
            data = p.text.strip() if p else ""
            obj.create_task(
                unique_key=a.get('href'),
                name=a.text.strip(),
                url=urljoin(base_url, a.get('href')),
                data=data
            )
