#!/usr/bin/env python3

#
# bparse.py
#
# Parse an HTML file returned by Bing search
# Report on any ads
#

import json
import requests
from bs4 import BeautifulSoup
from os import path
import re
import sys

ALLOWED_FILENAME = "allowed.txt"
ALLOWED_CUSTOM_FILENAME = "allowed-custom.txt"
MALICIOUS_FILENAME = "malicious.txt"
MALICIOUS_CUSTOM_FILENAME = "malicious-custom.txt"

ignore = []

def read_list(filename: str) -> list:
    data_list = []
    if path.exists(filename):
        file = open(filename, 'r')
        data = file.read()
        for line in data.split('\n'):
            if line:
                data_list.append(line)
    return data_list

ignore += read_list(ALLOWED_FILENAME)
ignore += read_list(ALLOWED_CUSTOM_FILENAME)
ignore += read_list(MALICIOUS_FILENAME)
ignore += read_list(MALICIOUS_CUSTOM_FILENAME)

ignore_list="|".join(ignore)
ignore_subdomains=[]
for domain in ignore:
    ignore_subdomains.append("\w+\." + domain)
ignore_list+="|"
ignore_list+="|".join(ignore_subdomains)
re_ignore=r"\/("+ignore_list+")"
#print(f're_ignore={re_ignore}')

try:
    filename = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <filename>")

if path.exists(filename):
    file = open(filename,mode='r')
    html_text = file.read()
    file.close()
else:
    print(f'Error: {filename} does not exist')
    sys.exit(1)

soup = BeautifulSoup(html_text, 'html.parser')

regex = re.compile('.*sb_adTA.*')
for div_ad in soup.find_all('div', {"class": "sb_adTA"}):
#for div_ad in soup.find_all('div', {"class": regex}):
#for sb_addesc in soup.find_all('div[class="sb_addesc"]'):
#for sb_addesc in soup.find_all('p'):
    #print(f'div_ad={div_ad}')
    for atag in div_ad.find_all('a', {"class": "b_restorableLink"}):
        #print(f'atag={atag}')
        data_restore = atag.get('data-restore')
        #print(f'data_restore={data_restore}')
        data = json.loads(data_restore)
        #print(f'data={data}')
        displayUrl = data.get('displayUrl', None)
        displayUrl = displayUrl.replace("<strong>","")
        displayUrl = displayUrl.replace("</strong>","")
        #print(f'displayUrl={displayUrl}')

        ig = re.search(re_ignore, displayUrl)
        #print(f'ig={ig}')
        if not ig:
            print(f'Found {displayUrl} {filename}')
