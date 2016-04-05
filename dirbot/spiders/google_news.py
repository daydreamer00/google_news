from scrapy.spiders import Spider
from scrapy.selector import Selector
import scrapy

from dirbot.items import GoogleNews


class GoogleNewsSpider(Spider):

    name = "google_news"
    allowed_domains = ["www.google.com.hk"]
    start_urls = ["https://www.google.com.hk/search?hl=en&gl=us&tbm=nws&auth"
                  "user=0&q=election+2016&oq=elect&gs_l=news-cc.3.1.43j0l10j43"
                  "i53.4845.5526.0.7711.5.5.0.0.0.0.325.491.2j3-1.3.0...0.0..."
                  "1ac.1.g9cTsl9PXkE&gws_rd=cr"]
    page_num = 1
    max_page_num = 3
    item_num = 1

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
