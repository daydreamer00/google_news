import os
import json
import time
import datetime
from run_spider import run_spider

def daily_crawl(outjsonpath="./json/", depth=5):
    base_keyword = "Election 2016"
    sub_keywords = ["", "republican", "democratic"]
    ret_codes = [
        run_spider(
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
    meta['time'] = time.time()
    meta['datetime'] = datetime.datetime.fromtimestamp(
        meta['time']).strftime('%Y-%m-%d %H:%M:%S')
    meta['descrip'] = "google news crawl for U.S Elect 2016"
    with open(os.path.join(outjsonpath, 'meta.json'), 'w') as f:
        f.write(json.dumps(meta))

    print "Returen codes: " + str(ret_codes)
    return ret_codes

if __name__ == '__main__':
    daily_crawl()
