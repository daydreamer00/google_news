import sys
import json
import argparse

if __name__ =="__main__":
    pa = argparse.ArgumentParser()
    pa.add_argument('--click_path')
    pa.add_argument('--view_path')
    args = pa.parse_args()
    click_f = open(args.click_path,'w')
    view_f = open(args.view_path,'w')
    for line in sys.stdin:
        json_dict = json.loads(line)
        res_dict = {}
    # user_id not same with uid?
        res_dict['uid'] = str(json_dict.get('user_id',None))
        res_dict['ip'] = json_dict.get('ip',None)
        req = json_dict.get('request',None);
        if req :
            data = req.get('data',None)
            for item in data:
                if item.get('path',None)=="/WEBPAGE/ONLINE_SHOP/TRENDS":
                    val = item.get('value',None)
                    val_dict = json.loads(val)
                    res_dict['timestamp'] = val_dict.get('timestamp',None)
                    try:
                        skey = json.loads(val_dict.get('single_key',None))
                    except ValueError, e:
                        sys.stderr.write(str(e))
                    if skey.get('eventId',None) == "click":
                        res_dict['titleName'] = skey.get('titleName',None)
                        res_dict['newsID'] = skey.get('newsID',None)
                        click_f.write(json.dumps(res_dict)+"\n")
                    if skey.get('eventId',None) == "pageview":
                        view_f.write(json.dumps(res_dict)+"\n")
    click_f.close()
    view_f.close()
