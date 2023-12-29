from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    for item in res.json().get('data').get('news_list'):
        name = f"[{item.get('news_obj').get('source_name')}] - {item.get('news_obj').get('title')}"
        url = item.get('news_obj').get('source_url')
        url = url.replace("?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts", "")
        data = item.get('news_obj').get('content')

        obj.create_task(
            unique_key=item.get("hash_id"),
            name=name,
            url=url,
            data=data
        )

