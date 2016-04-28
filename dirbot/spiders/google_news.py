from scrapy.spiders import Spider
from scrapy.selector import Selector
import uuid
import scrapy
import re

from dirbot.items import GoogleNews


class GoogleNewsSpider(Spider):

    name = "google_news"
    allowed_domains = ["www.google.com.hk"]
    start_urls = []
    page_num = 1
    max_page_num = 3
    item_num = 1

    def __init__(self, *args, **kwargs):
        super(GoogleNewsSpider,self).__init__(*args, **kwargs)
        start_urls = []
        start_urls.append(kwargs.get('start_url'))
        self.start_urls = start_urls

    def parse(self, response):
        return self.parse_follow_next_page(response)

    def parse_tgt_html(self, response):
        item = response.meta['item']
        item['tgt_url'] = response.url
        item['news_id'] = str(uuid.uuid3(uuid.NAMESPACE_URL,response.url))
        yield item

    def parse_follow_next_page(self, response):
        sel = Selector(response)
        search_res_tr_sellist = sel.xpath('//*[@id="ires"]/ol/div/table/tr')

        for tr_sel in search_res_tr_sellist:

            item = GoogleNews()
            item['title'] = tr_sel.xpath('string(td/h3/a)').extract()[0]
            press_time= tr_sel.xpath('td/div/span/text()').extract()[0]
            press_time_list = press_time.split('-')
            item['press']  = '-'.join(press_time_list[:-1]).strip()
            item['time']  = press_time_list[-1].strip()
            item['url'] = tr_sel.xpath('td/h3/a/@href').extract()[0]
            print("pageurl: "+response.url)
            pat = re.compile("q=(.*?)&")
            matches = re.findall(pat,response.url)
            if len(matches) > 0:
                item['keywords'] = matches[0].replace('+',' ')
            else:
                item['keywords'] = ""

            item['img_url'] = tr_sel.xpath('td[2]/a/img/@src').extract()
            if (len(item['img_url'])!=1):
                yield
            item['abstract'] = tr_sel.xpath('string(td[1]/div[@class="st"])').extract()[0].replace(u'\xa0','')
            request = scrapy.Request(
                response.urljoin(item['url']),
                callback=self.parse_tgt_html)
            request.meta['item'] = item
            if (len(item['img_url'])!=1):
                yield
            else:
                yield request

        next_page = sel.xpath(
            '//a[@class="fl" and ./*[contains(text(),"Next")]]')
        if next_page:
            next_url = response.urljoin(
                next_page[0].xpath('./@href').extract()[0])
            yield scrapy.Request(next_url, callback=self.parse_follow_next_page)
