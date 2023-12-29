from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)
    print(res.json())

    for item in res.json().get('data').get('news_list'):
        news_obj = item.get('news_obj')
        print(news_obj)
        if news_obj:
            name = f"[{news_obj.get('source_name')}] - {news_obj.get('title')}"
            url = news_obj.get('source_url') or news_obj.get('bottom_panel_link')
            # url = url.replace("?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts", "")
            data = news_obj.get('content')

            obj.create_task(
                unique_key=item.get("hash_id"),
                name=name,
                url=url,
                data=data
            )

