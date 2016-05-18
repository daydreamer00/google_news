cd $HOME/git/google_news
date=`date +%Y%m%d -d '-2 days'`
predate=`date +%Y%m%d -d '-2 days'`
postdate=`date +%Y%m%d -d '-2 days'`

while getopts "b:e:" opt; do
    case $opt in
        b)
            echo "rerun predate is set as: $OPTARG" >&2
            predate=$OPTARG
            ;;
        e)
            echo "rerun postdate is set as: $OPTARG" >&2
            postdate=$OPTARG
            ;;
        \?)
            echo "Invalid option: $OPTARG" >&2 
            exit
            ;;
    esac
done

d_count_pre=`echo $(( ($(date --date=$predate +%s) - $(date +%s) )/(60*60*24) ))`
d_count_post=`echo $(( ($(date --date=$postdate +%s) - $(date +%s) )/(60*60*24) ))`

function rundate {
    date_run=$1
    >&2 echo "Running Date of Data is $date_run"
    log_data_path=$HOME/git/google_news/data/news_click/log_data/$date_run
    click_data_path=$HOME/git/google_news/data/news_click/click_data/$date_run
    view_data_path=$HOME/git/google_news/data/news_click/view_data/$date_run
    mkdir -p $log_data_path
    mkdir -p $click_data_path
    mkdir -p $view_data_path
    aws s3 cp --region us-east-1  --recursive  "s3://ime.data/$date_run/""$date_run""_usage_ime_international_slice/webpage__/" $log_data_path
    lzop -dc $log_data_path/*.lzo | python extract_click.py --click_path $click_data_path/click_data.json --view_path $view_data_path/view_data.json
    python store_click_data.py --click_path $click_data_path/click_data.json --view_path $view_data_path/view_data.json
}


for index in $(seq $d_count_pre 1 $d_count_post); do
    date_i=$(date +%Y%m%d -d "${index} days");
    rundate $date_i
done

