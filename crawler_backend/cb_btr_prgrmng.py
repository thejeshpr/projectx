import urllib

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for div in soup.find_all('div', {
        'class': "col u-xs-marginBottom10 u-paddingLeft0 u-paddingRight0 u-paddingTop15 u-marginBottom30"}):
        a = div.find('a')
        if a:
            obj.create_task(
                unique_key=a.get('href'),
                name=a.text.strip(),
                url=a.get('href')
            )
