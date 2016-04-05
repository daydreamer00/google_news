#!/usr/local/opt/python/bin/python2.7

import argparse
import os
import sys

parser = argparse.ArgumentParser(description='process args')
parser.add_argument('keywords')
parser.add_argument('--Depth', type=int, default=5)
parser.add_argument('--OutFileName', default="res.json")
#parse_res =  parser.parse_args(['elect 2016','--Depth','5'])
parse_res = parser.parse_args(sys.argv[1:])
os.system('rm {0}'.format(parse_res.OutFileName))
url = "https://www.google.com.hk/search?hl=en&gl=us&tbm=nws&authuser=0&q={0}&oq=elect&gs_l=news-cc.3.1.43j0l10j43i53.4845.5526.0.7711.5.5.0.0.0.0.325.491.2j3-1.3.0...0.0...1ac.1.g9cTsl9PXkE&gws_rd=cr".format(parse_res.keywords.replace(" ", "+"))
print url
cmd = 'proxychains scrapy crawl google_news -a start_url="{0}" -o {1} -t json -s DEPTH_LIMIT={2}'.format(
    url, parse_res.OutFileName, parse_res.Depth)
print cmd
os.system(cmd)
