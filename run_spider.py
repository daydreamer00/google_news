#!/usr/local/opt/python/bin/python2.7

import argparse
import os
import sys
import time
import json


def run_google_news_spider(keywords, depth=5, outfilename='res.json'):
    outfilename = outfilename.replace(" ", "_")
    os.system('rm {0}'.format(outfilename))
    url = "https://www.google.com.hk/search?hl=en&gl=us&tbm=nws&authuser=0&q={0}&oq=elect&gs_l=news-cc.3.1.43j0l10j43i53.4845.5526.0.7711.5.5.0.0.0.0.325.491.2j3-1.3.0...0.0...1ac.1.g9cTsl9PXkE&gws_rd=cr".format(
        keywords.replace(
            " ",
         "+"))
    print "Google news Searh URL: " + url
    cmd = 'cd /home/kaiming/git/google_news/ && proxychains /home/kaiming/local/bin/scrapy crawl google_news -a start_url="{0}" -o {1} -t json -s DEPTH_LIMIT={2} '.format( url, outfilename, depth)
    #cmd = 'proxychains scrapy crawl google_news -a start_url="{0}" -o {1} -t json -s DEPTH_LIMIT={2} '.format(url, outfilename, depth)
    print "Scrapy Cmd: " + cmd
    ret_code = os.system(cmd)
    if ret_code != 0:
        print "Error: Scrapy Google News Failed!"
        exit(-1)
    res_dict = {}
    res_dict['timestamp'] = int(time.time())
    with open(outfilename,'rb') as f:
        json_str = f.read()

    res_dict['content'] = json.loads(json_str)
    with open(outfilename, 'w') as f:
        f.write(json.dumps(res_dict))

    return ret_code

def run_google_search_spider(depth=5, outfilename='res.json'):
    os.system('rm {0}'.format(outfilename))
    os.system('rm {0}'.format(outfilename+'.tmp'))
    cmd  = 'proxychains /home/kaiming/local/bin/scrapy crawl google_search -a start_url="https://www.google.com/async/usprimaries_party?async=party:2,exp:0,month:2016-04,cs:0,ecm:,location:,_id:eob-pcb,_pms:s&vet=10ahUKEwiOg8qMvojMAhUBW2MKHY2zCIAQjpgBCCEwAA..i&ei=bJcMV46dO4G2jQON56KACA&hl=en&yv=2;https://www.google.com/async/usprimaries_party?async=party:1,exp:0,month:2016-04,cs:0,ecm:,location:,_id:eob-pcb,_pms:s&vet=10ahUKEwiOg8qMvojMAhUBW2MKHY2zCIAQjpgBCCEwAA..i&ei=bJcMV46dO4G2jQON56KACA&hl=en&yv=2" -o {0} -t json -s DEPTH_LIMIT={1}'.format(outfilename+'.tmp',depth)
    print "Scrapy Cmd: " + cmd

    ret_code =  os.system(cmd)
    if ret_code != 0:
        print "Error: Scrapy Google Search Failed!"
        exit(-1)
    with open(outfilename+'.tmp', 'rb') as f:
        json_str = f.read()

    json_dict = json.loads(json_str)
    res_dict = {}
    res_dict['timestamp'] = int(time.time())
    res_dict['content'] = {'democratic':[],'republican':[]}
    democratic_candidates = ["Clinton","Sanders"]

    for candidate in json_dict:
        if candidate["name"] in democratic_candidates:
            res_dict['content']['democratic'].append(candidate)
        else:
            res_dict['content']['republican'].append(candidate)

    with open(outfilename,'w') as f:
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
