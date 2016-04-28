date=`date +%Y%m%d -d '-2 days'`
log_data_path=$HOME/git/google_news/data/news_click/log_data/$date
click_data_path=$HOME/git/google_news/data/news_click/click_data/$date
mkdir -p $log_data_path
mkdir -p $click_data_path
#aws s3 cp --region us-east-1  --recursive  "s3://ime.data/$date/""$date""_usage_ime_international_slice/webpage__/" $log_data_path
lzop -dc $log_data_path/*.lzo | python extract_click.py > $click_data_path/click_data.json
