#!/usr/bin/bash

outputdir="output"
if [[ ! -e $outputdir ]]; then
    mkdir $outputdir
fi

performquery () {
    query="$1"
    today=$(date +%Y%m%d)
    output_today="$outputdir/$today"
    if [[ ! -e $output_today ]]; then
        mkdir -p $output_today
    fi

    output="$output_today/$query-$epoch.html"
    #echo "Searching $query > $output"
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

for (( ; ; ))
do
    date

    epoch=`date +%s`

    performquery '1password'
    performquery '7zip+download'
    performquery 'adobe+reader'
    performquery 'anydesk'
    performquery 'brave+browser'
    performquery 'ccleaner'
    performquery 'discord'
    performquery 'filezilla'
    performquery 'gimp'
    performquery 'notepad%2b%2b+download'
    performquery 'rufus+download'
    performquery 'slack'
    performquery 'teamviewer'
    performquery 'thunderbird'
    performquery 'virtualbox'
    performquery 'vlc+download'
    performquery 'winrar+download'

    sleep 60
done
