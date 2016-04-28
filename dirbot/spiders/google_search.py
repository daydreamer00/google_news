from scrapy.spiders import Spider
from scrapy.selector import Selector
import re

from dirbot.items import GoogleSearch


class GoogleSearchSpider(Spider):

    name = "google_search"
    allowed_domains = ["www.google.com.hk"]
    start_urls = []
    page_num = 1
    max_page_num = 3
    item_num = 1

    def __init__(self, *args, **kwargs):
        super(GoogleSearchSpider,self).__init__(*args, **kwargs)
        start_urls = []
        urls = kwargs.get('start_url').split(';')
        for url in urls:
            start_urls.append(url)
        self.start_urls = start_urls

    def parse(self, response):
        sel = Selector(response)
        pattern = re.compile('Candidate \d of \d. (\w+). (\d+) delegates.')
        body_text = sel.xpath('//body').extract()[0]
        name_del_pairs = pattern.findall(body_text)

        for kv in name_del_pairs:
            item = GoogleSearch()
            item['name'] = kv[0]
            item['votes'] = int(float(kv[1]))
            yield item



