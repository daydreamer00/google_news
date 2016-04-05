from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy

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
        item['tgt_html'] = response.body
        yield item

    def parse_follow_next_page(self, response):
        sel = Selector(response)
        search_res_tr_sellist = sel.xpath('//*[@id="ires"]/ol/div/table/tr')

        for tr_sel in search_res_tr_sellist:

            item = GoogleNews()
            item['raw_html_tr'] = tr_sel.xpath('.').extract()
            item['title'] = tr_sel.xpath('td/h3/a/node()').extract()
            item['press_time'] = tr_sel.xpath('td/div/span/text()').extract()
            item['url'] = tr_sel.xpath('td/h3/a/@href').extract()
            item['img_url'] = tr_sel.xpath('td[2]/a/img/@src').extract()
            request = scrapy.Request(
                response.urljoin(item['url'][0]),
                callback=self.parse_tgt_html)
            request.meta['item'] = item
            yield request

        next_page = sel.xpath(
            '//a[@class="fl" and ./*[contains(text(),"Next")]]')
        if next_page:
            next_url = response.urljoin(
                next_page[0].xpath('./@href').extract()[0])
            yield scrapy.Request(next_url, callback=self.parse_follow_next_page)
