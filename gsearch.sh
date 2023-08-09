#!/usr/bin/bash

outputdir="output"
if [[ ! -e $outputdir ]]; then
    mkdir $outputdir
fi

# https://stackoverflow.com/questions/296536/how-to-urlencode-data-for-curl-command
rawurlencode() {
  local string="${1}"
  local strlen=${#string}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${string:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        " " ) o="+" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
  REPLY="${encoded}"
}

performquery () {
    query="$1"
    today=$(date +%Y%m%d)
    output_today="$outputdir/$today"
    if [[ ! -e $output_today ]]; then
        mkdir -p $output_today
    fi

    output="$output_today/$query-$epoch.html"
    echo "Searching $query > $output"
    http_code=$(curl "https://www.google.com/search?q=$query" -H 'referer: https://www.google.com/' \
      -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
      --compressed --output $output --silent --max-time 10 -w '%{http_code}')
    exit_status="$?"
    if [[ $http_code == "200" ]]; then
        ./gparse.py $output
    else
        echo "curl error:$http_code:$exit_status:$query:$output"
    fi
    sleep 1
}

performbingquery () {
    query="$1"
    today=$(date +%Y%m%d)
    output_today="$outputdir/$today"
    if [[ ! -e $output_today ]]; then
        mkdir -p $output_today
    fi

    output="$output_today/bing-$query-$epoch.html"
    echo "Searching $query > $output"
    # https://www.bing.com/search?q=looksrare&qs=n&form=QBRE&sp=-1&lq=0&pq=looksrare&sc=15-9&sk=&cvid=F4468886830C498B9CB2B17F18956F22&ghsh=0&ghacc=0&ghpl=
    http_code=$(curl "https://www.bing.com/search?q=$query" -H 'referer: https://www.bing.com/' \
      -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
      --compressed --output $output --silent --max-time 10 -w '%{http_code}')
    exit_status="$?"
    if [[ $http_code == "200" ]]; then
        ./bparse.py $output
    else
        echo "curl error:$http_code:$exit_status:$query:$output"
    fi
    sleep 1
}

for (( ; ; ))
do
    date

    epoch=`date +%s`

    IFS=$'\n'
    for t in `cat queries.txt`; do
        rawurlencode "$t"
        performquery "$REPLY"
        performbingquery "$REPLY"
    done

    if [[ -e "queries-custom.txt" ]]; then
        for t in `cat queries-custom.txt`; do
            rawurlencode "$t"
            performquery "$REPLY"
            performbingquery "$REPLY"
        done
    fi
    sleep 60
done
