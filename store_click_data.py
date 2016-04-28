from pymongo import MongoClient
import argparse
import json

if __name__=="__main__":

    pa = argparse.ArgumentParser()
    pa.add_argument('-i',dest='inputjson',nargs=1,type=str)
    args = pa.parse_args()
    inputjson = args.inputjson[0]

    click_data_db = MongoClient().elect2016.google_news_click_data
    with open(inputjson,'r') as f:
        for l in f:
            json_dict = json.loads(l)
            click_data_db.insert_one(json_dict)
