from bs4 import BeautifulSoup as bs
from bs4 import Tag, NavigableString
from json import loads
import datetime

json_base_filename = "html/latest/Election_2016_"
json_sub_filenames = ["", "democratic", "republican"]
json_filenames = [json_base_filename+s+".json" for s in json_sub_filenames]
domain = "www.google.com.hk"

def clone(el):
    if isinstance(el, NavigableString):
        return type(el)(el)

    copy = Tag(None, el.builder, el.name, el.namespace, el.nsprefix)
    # work around bug where there is no builder set
    # https://bugs.launchpad.net/beautifulsoup/+bug/1307471
    copy.attrs = dict(el.attrs)
    for attr in ('can_be_empty_element', 'hidden'):
        setattr(copy, attr, getattr(el, attr))

    for child in el.contents:
        copy.append(clone(child))

    return copy

def google_news_json2html():

    for s in json_filenames:
        print(s)

        json_str = ""
        with open(s, "r") as f:
            json_str = f.read()

        json_dict = loads(json_str)
        timestamp = json_dict["timestamp"]
        contents = json_dict["content"]
        html = '<!DOCTYPE html> <html> <body> <style >table {table-layout: auto; border-collapse: separate; width: 100%; border: 1px solid black; } td { border: 1px solid black; }table{} .content-loader tr td { white-space: nowrap; }</style><table >'
        header = '<tr class="block"><td>Title</td><td>Image</td><td>Press</td><td>Time</td><td>Abstract</td></tr>'
        html = html + header

        for content in contents:

            #raw_html_tr = content["raw_html_tr"].encode('utf-8','ignore')
            title = content["title"].encode('utf-8','ignore')
            press = content["press"].encode('utf-8','ignore')
            time = content["time"].encode('utf-8','ignore')
            url = content["url"].encode('utf-8','ignore')
            tgt_url = content["tgt_url"].encode('utf-8','ignore')
            img_urls = content["img_url"]
            if len(img_urls):
                img_url = img_urls[0].encode('utf-8','ignore')
            else:
                img_url = ""
            #tgt_url = content["tgt_url"]
            abstract = content["abstract"].encode('utf-8','ignore')
            tr = '<tr class="block"><td><a href="{3}"> {0}</a></td><td><img src="{5}" alt="No Image"></td><td>{1}</td><td>{2}</td><td>{4}</td></tr>'.format(title,press,time,tgt_url,abstract,img_url)
            html = html + tr

        html = html + "</table> </body> </html> "

        keywords = s.split('/')[2] .split('.')[0]
        html_filename = "html/"+keywords+'.html'
        with open(html_filename, "wb") as f:
            f.write(html)

if __name__ == "__main__":
    google_news_json2html()
