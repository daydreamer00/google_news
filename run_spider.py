#!/usr/local/opt/python/bin/python2.7

import argparse
import os
import sys
import time
import json


def run_spider(keywords, depth=5, outfilename='res.json'):
    outfilename = outfilename.replace(" ", "_")
    os.system('rm {0}'.format(outfilename))
    url = "https://www.google.com.hk/search?hl=en&gl=us&tbm=nws&authuser=0&q={0}&oq=elect&gs_l=news-cc.3.1.43j0l10j43i53.4845.5526.0.7711.5.5.0.0.0.0.325.491.2j3-1.3.0...0.0...1ac.1.g9cTsl9PXkE&gws_rd=cr".format(
        keywords.replace(
            " ",
         "+"))
    print "Google news Searh URL: " + url
    cmd = 'proxychains scrapy crawl google_news -a start_url="{0}" -o {1} -t json -s DEPTH_LIMIT={2} -s LOG_FILE=log/scrapy.log -s LOG_LEVEL="INFO"'.format(
        url, outfilename, depth)
    print "Scrapy Cmd: " + cmd
    ret_code = os.system(cmd)
    if ret_code != 0:
        print "Error: Scrapy Failed!"
    res_dict = {}
    res_dict['timestamp'] = int(time.time())
    res_dict['content'] = json.loads(open(outfilename, 'rb').read())
    with open(outfilename, 'w') as f:
        f.write(json.dumps(res_dict))

    return ret_code

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='process args')
    parser.add_argument('keywords')
    parser.add_argument('--Depth', type=int, default=5)
    parser.add_argument('--OutFileName', default="res.json")
    parse_res = parser.parse_args(sys.argv[1:])
    keywords = parse_res.keywords
    depth = parse_res.Depth
    outfilename = parse_res.OutFileName
    run_spider(keywords, depth, outfilename)
