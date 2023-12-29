from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    spans = soup.find_all('span', {'class': 'titleline'})

    for span in spans:
        a = span.find('a')
        site_info = span.find('span', {'class': "sitebit comhead"})
        if site_info:
            title = f"{a.text.strip()} - {site_info.text.strip()}"
        else:
            title = a.text.strip()

        obj.create_task(
            unique_key=a.get('href'),
            name=title,
            url=a.get('href')
        )
