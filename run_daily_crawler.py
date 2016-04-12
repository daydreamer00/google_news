import os
import json
from run_spider import run_google_news_spider,run_google_search_spider
from google_news_json2html import google_news_json2html

def daily_crawl(outjsonpath="./json/", depth=5):
    base_keyword = "Election 2016"
    sub_keywords = ["", "republican", "democratic"]
    ret_codes = [
        run_google_news_spider(
            base_keyword +
            " " +
            sub_keyword,
            depth,
            os.path.join(
                outjsonpath,
                base_keyword +
                " " +
                sub_keyword +
                ".json")) for sub_keyword in sub_keywords]
    meta = {}
    meta['description'] = "Election"
    with open(os.path.join(outjsonpath, 'meta.json'), 'w') as f:
        f.write(json.dumps(meta))

    print "Returen codes: " + str(ret_codes)
    if sum(ret_codes)==0:
       os.system('cp json/*.json html/latest/')
       google_news_json2html()

    votes_file_name = os.path.join(outjsonpath,'votes.json')
    ret_code = run_google_search_spider(depth,votes_file_name)

    ret_codes.append(ret_code)

    if sum(ret_codes)==0:
       os.system('cp json/*.json html/latest/')
       google_news_json2html()
    return
if __name__ == '__main__':
    daily_crawl()
