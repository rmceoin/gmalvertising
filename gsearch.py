#!/usr/bin/env python3

#
# gsearch.py
#
# Monitor Google malvertising
#

import re
import os
import time
import sys
from urllib.parse import quote_plus, urlencode, urlparse
import requests

from bs4 import BeautifulSoup
from googlesearch import search

from util import Util

class GSearch:
    """
    Monitor Google malvertising
    """

    CONFIG_QUERIES = "queries.txt"

    ALLOWED_FILENAME = "allowed.txt"
    ALLOWED_CUSTOM_FILENAME = "allowed-custom.txt"
    MALICIOUS_FILENAME = "malicious.txt"
    MALICIOUS_CUSTOM_FILENAME = "malicious-custom.txt"

    def __init__(self, verbose=False):

        self.verbose = verbose
        self.queries = Util.read_list(self.CONFIG_QUERIES)
        self.re_ignore = ''
        if not os.path.exists(Util.RESULTS_DIR):
            print(f'Error: directory does not exist: {Util.RESULTS_DIR}')
            sys.exit(1)
        self.ads_found = 0
        self.google_abuse = ''

    def build_ignore_list(self):
        ignore = []
        ignore += Util.read_list(self.ALLOWED_FILENAME)
        ignore += Util.read_list(self.ALLOWED_CUSTOM_FILENAME)
        ignore += Util.read_list(self.MALICIOUS_FILENAME)
        ignore += Util.read_list(self.MALICIOUS_CUSTOM_FILENAME)

        ignore_list="|".join(ignore)

        ignore_subdomains=[]
        for domain in ignore:
            ignore_subdomains.append(r"[-\w\.]+\." + domain)
        ignore_list+="|"
        ignore_list+="|".join(ignore_subdomains)

        self.re_ignore=r"/("+ignore_list+"|aclk)/"

    def parse_google(self, data: str, filename: str):
        soup = BeautifulSoup(data, 'html.parser')

        for link in soup.find_all('a'):
            data_rw = link.get('data-rw')
            data_pcu = link.get('data-pcu')
            href=link.get('href')
            if data_pcu:
        #        print(f'data_pcu={data_pcu} : href={href}')
                ig = re.search(self.re_ignore, data_pcu)
                if not ig:
                    print(f'Found {data_pcu} {filename}')
                    self.ads_found += 1
            elif data_rw:
        #        print(f'data_rw={data_rw} : href={href}')
        #        print(link)

                #print(f'Got {href}')
                ig = re.search(self.re_ignore, href)
                #print(f'ig={ig}')
                if not ig:
                    aclk=href.find("/aclk?")
                    #print(f'aclk={aclk}')
                    if aclk == -1:
                        print(f'Found {href} {filename}')
                        self.ads_found += 1

    def emit_captcha(self, data: str):
        #
        # need to generate a URL like this:
        #
        # https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3D1password%26num%3D12%26hl%3Den%26start%3D0&hl=en&q=EhAmBVnIQYS0EAAAAAAAAAUlGIbT5rAGIjA4pwkSaCvmFf54it0-_ptcGj2PPubjOH0W4erszQLoSBLj9ixmFT-kSqEQAnji3rcyAXJaAUM
        #
        # From these:
        #
        # <input type='hidden' name='q' value='EhAmBVnIQYS0EAAAAAAAAAUlGObT5rAGIjBzK44_N6LxMtEJ4tDTyvBC1DRhHf1-jUYrPngnGJoNP5ZZLgOmEaUZz6dfvlSFwrsyAXJaAUM'>
        # <input type="hidden" name="continue" value="https://www.google.com/search?q=1password&amp;start=1">

        soup = BeautifulSoup(data, 'html.parser')

        captcha_q = ''
        captcha_continue = ''
        for input_tag in soup.find_all('input'):
            #input_type = input_tag.get('type')
            input_name = input_tag.get('name')
            input_value = str(input_tag.get('value'))
            if input_name == 'q':
                captcha_q = input_value
            if input_name == 'continue':
                captcha_continue = quote_plus(input_value)

        if captcha_q and captcha_continue:
            url = f'https://www.google.com/sorry/index?continue={captcha_continue}&q={captcha_q}'
            print(f'{url}')
            response_url = input("Response url:")
            #print(f'{response_url}')
            # https://www.google.com/search?q=1password&start=1&google_abuse=GOOGLE_ABUSE_EXEMPTION%3DID%3D3430d96886fb1bfa:TM%3D1713042750:C%3Dr:IP%3D2605:59c8:4184:b410::525-:S%3DUFjqHsAr7tfRcaQkVnJZ1-g%3B+path%3D/%3B+domain%3Dgoogle.com%3B+expires%3DSun,+14-Apr-2024+00:12:30+GMT
            p = re.compile(r".*google_abuse=(.*)")
            m = p.match(response_url)
            if m:
                self.google_abuse = m.group(1)
                print(f'google_abuse={self.google_abuse}')
            else:
                print('Unable to find google_abuse parameter')
        else:
            print('Unable to find q and continue')

    def perform_poll(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            'referer': 'https://www.google.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'Sec-Ch-Ua-Arch': '"x86"',
            'Sec-Ch-Ua-Bitness': '"64"',
            'Sec-Ch-Ua-Full-Version': '"123.0.6312.105"',
            'Sec-Ch-Ua-Full-Version-List': '"Google Chrome";v="123.0.6312.105", "Not:A-Brand";v="8.0.0.0", "Chromium";v="123.0.6312.105"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Model':'""',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Sec-Ch-Ua-Platform-Version': '"6.6.9"',
            'Sec-Ch-Ua-Wow64': '?0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        for query in self.queries:
            print(f'query: {query}')
            cookies = {
                'DV': 'o7j7TaTFv_Ug0DMXzUabLUp-kViV7Vih9o6BwpVJrgIAAAA',
                'OTZ': '7477323_76_80_104160_76_446820',
                'UULE': 'a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNzEzMDQyNjc2NzgwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDMyNTM3MjAwOAogIGxvbmdpdHVkZV9lNzogLTk2NzQ5Mzk5Mwp9CnJhZGl1czogNzYxMjQ0NDkuNDYxNTY0MDUKcHJvdmVuYW5jZTogNgo=',

            }
            for start in ['1', '11', '21']:
                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    sys.exit('Aborted')

                params = {
                    'q': query,
                    'start': start
                }
                if self.google_abuse:
                    params['google_abuse'] = self.google_abuse

                encoded_params = urlencode(params)
                url = f'https://www.google.com/search?{encoded_params}'
                print(f'url={url}')

                #results = search(query, advanced=True)
                #print(f'results={results}')
                #for result in results:
                #    print(f'result={result}')
                #continue
                try:
                    #print(f'Getting {url}')
                    r = requests.get(url, verify=True, timeout=15, headers=headers, cookies=cookies)
                except requests.exceptions.ConnectionError as exception:
                    print(f'Error requesting: {url}: {exception}')
                    return
                except KeyboardInterrupt:
                    sys.exit('Aborted')

                if r.status_code == 200:
                    filename = Util.save(f'{query}-{start}', r.text, 'html')
                    self.parse_google(r.text, filename)
                elif r.status_code == 429:
                    print('Too many requests:')

                    filename = Util.save('captcha', r.text, 'html')
                    print(f'Open this: {filename}')
                    self.emit_captcha(r.text)
                    #self.do_sleep(120)
                    return
                else:
                    print(f'Error: {r.status_code}: {url}')

    def do_sleep(self, seconds: int):
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            sys.exit('Aborted')

    def monitor(self):
        self.build_ignore_list()
        while True:
            self.perform_poll()
            sleep_time = 10
            print(f'Sleeping {sleep_time} - {self.ads_found} ads found')
            self.do_sleep(sleep_time)

if __name__ == '__main__':
    GSearch().monitor()
