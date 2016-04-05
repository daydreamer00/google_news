from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class GoogleNews(Item):

    raw_html_tr = Field()
    title = Field()
    press = Field()
    time = Field()
    url = Field()
    img_url = Field()
    tgt_html = Field()
    tgt_url = Field()
    abstract = Field()
