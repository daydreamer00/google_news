from pymongo import MongoClient
import argparse
import json

if __name__=="__main__":

    pa = argparse.ArgumentParser()
    pa.add_argument('--click_path',type=str)
    pa.add_argument('--view_path',type=str)
    args = pa.parse_args()
    click_path = args.click_path
    view_path = args.view_path

    click_data_db = MongoClient().elect2016.google_news_click_data
    with open(click_path,'r') as f:
        for l in f:
            json_dict = json.loads(l)
            click_data_db.insert_one(json_dict)
    view_data_db = MongoClient().elect2016.google_news_view_data
    with open(view_path,'r') as f:
        for l in f:
            json_dict = json.loads(l)
            view_data_db.insert_one(json_dict)
