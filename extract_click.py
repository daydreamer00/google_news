import sys
import json

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
                    print json.dumps(res_dict)
