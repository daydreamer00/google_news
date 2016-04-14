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
        #item['tgt_html'] = response.body.decode('utf8', 'ignore')
        yield item

    def parse_follow_next_page(self, response):
        sel = Selector(response)
        search_res_tr_sellist = sel.xpath('//*[@id="ires"]/ol/div/table/tr')

        for tr_sel in search_res_tr_sellist:

            item = GoogleNews()
            #`item['raw_html_tr'] = tr_sel.xpath('.').extract()[0]
            item['title'] = tr_sel.xpath('string(td/h3/a)').extract()[0]
            press_time= tr_sel.xpath('td/div/span/text()').extract()[0]
            item['press']  = press_time.split('-')[0].strip()
            item['time']  = press_time.split('-')[1].strip()
            item['url'] = tr_sel.xpath('td/h3/a/@href').extract()[0]
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
