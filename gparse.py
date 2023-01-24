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

ignore=r"/(www.adobe.com|www.atera.com|brave.com|try.bravesoftware.com|goto.com|buy.goto.com|www.goto.com|www.teamviewer.com|service.teamviewer.com|www.zoho.com|aclk)/"

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
        ig = re.search(ignore, data_pcu)
        if not ig:
            print(f'Found {data_pcu} {filename}')
    elif data_rw:
#        print(f'data_rw={data_rw} : href={href}')
#        print(link)
        
        #print(f'Got {href}')
        ig = re.search(ignore, href)
        #print(f'ig={ig}')
        if not ig:
            aclk=href.find("/aclk?")
            #print(f'aclk={aclk}')
            if aclk == -1:
                print(f'Found {href} {filename}')

