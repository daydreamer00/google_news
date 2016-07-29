import os
import json
import datetime
from run_spider import run_google_news_spider,run_google_search_spider
from google_news_json2html import google_news_json2html

def daily_crawl(outjsonpath="./json/", depth=5):
    base_keyword = "United States Presidential Election 2016 "
    sub_keywords = ["republican", "democratic"]
    ret_codes = [
        run_google_news_spider(
            base_keyword +
            sub_keyword,
            depth,
            os.path.join(
                outjsonpath,
                base_keyword +
                sub_keyword +
                ".json")) for sub_keyword in sub_keywords]
    #keywords ="United States Presidential Election 2016"
    #ret_codes.append(run_google_news_spider( keywords, depth, os.path.join( outjsonpath, keywords+".json")) )
    meta = {}
    meta['description'] = "Election"
    with open(os.path.join(outjsonpath, 'meta.json'), 'w') as f:
        f.write(json.dumps(meta))

    print "Returen codes: " + str(ret_codes)

    votes_file_name = os.path.join(outjsonpath,'votes.json')
    ret_code = run_google_search_spider(depth,votes_file_name)

    ret_codes.append(ret_code)

    if sum(ret_codes)==0:
       os.system('rm html/latest/*')

       res_dict = {}
       res_dict['content'] = []
       for sub_keyword in sub_keywords:
           file_name = base_keyword + sub_keyword + ".json"
           with open(os.path.join(outjsonpath,file_name.replace(" ","_")),"r") as f:
                json_str = f.read()
                json_dict = json.loads(json_str)
                res_dict['timestamp'] = json_dict['timestamp']
                res_dict['content'].extend(json_dict['content'])

       import random
       # remove dumplicat items with sam title
       res_dict['content'] = { d["title"] : d for d in res_dict['content'] }.values()
       random.shuffle(res_dict['content'])
       res_dict['content'].sort(cmp = lambda x,y: 1 if ("hour" in x and "hour" not in y) else
                                1 if ("day" in x and "day" not in y and "hour" not in y) else
                                -1 ,reverse = True,key = lambda x:x["time"])
       with open(os.path.join(outjsonpath,"Election_2016_.json"),"w") as f:
           f.write(json.dumps(res_dict))

       os.system('cp '+ os.path.join(outjsonpath,"*.json")+' html/latest/')

       datestr = datetime.datetime.now().strftime('%Y%m%d%H')
       os.system('mkdir -p html/history/google_news_{0}'.format(datestr))
       os.system('cp '+ os.path.join(outjsonpath,"*.json") + ' html/history/google_news_{0}/'.format(datestr))
       google_news_json2html()
       os.system('cp html/*.html html/history/google_news_{0}/'.format(datestr))
    return
if __name__ == '__main__':
    daily_crawl()
