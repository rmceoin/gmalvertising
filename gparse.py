#!/usr/bin/env python3

#
# gparse.py
#
# Parse an HTML file returned by Google search
# Report on any ads
#

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

re_ignore=r"/("+ignore_list+"|aclk)/"

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

for link in soup.find_all('a'):
    data_rw = link.get('data-rw')
    data_pcu = link.get('data-pcu')
    href=link.get('href')
    if data_pcu:
#        print(f'data_pcu={data_pcu} : href={href}')
        ig = re.search(re_ignore, data_pcu)
        if not ig:
            print(f'Found {data_pcu} {filename}')
    elif data_rw:
#        print(f'data_rw={data_rw} : href={href}')
#        print(link)
        
        #print(f'Got {href}')
        ig = re.search(re_ignore, href)
        #print(f'ig={ig}')
        if not ig:
            aclk=href.find("/aclk?")
            #print(f'aclk={aclk}')
            if aclk == -1:
                print(f'Found {href} {filename}')

