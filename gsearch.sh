#!/usr/bin/bash

outputdir="output"
if [[ ! -e $outputdir ]]; then
    mkdir $outputdir
fi

performquery () {
    query="$1"
    output="$outputdir/$query-$epoch.html"
    echo "Searching $query > $output"
    curl "https://www.google.com/search?q=$query" -H 'referer: https://www.google.com/' \
      -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
      --compressed --output $output --silent --max-time 10
    ./gparse.py $output
}

for (( ; ; ))
do
    date

    epoch=`date +%s`

    performquery '7zip+download'
    performquery 'adobe+reader'
    performquery 'anydesk'
    performquery 'brave+browser'
    performquery 'discord'
    performquery 'filezilla'
    performquery 'notepad%2b%2b+download'
    performquery 'rufus+download'
    performquery 'teamviewer'
    performquery 'thunderbird'
    performquery 'vlc+download'
    performquery 'winrar+download'

    sleep 60
done
