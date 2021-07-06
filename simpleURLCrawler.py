#!/usr/bin/python3
# coding: utf-8

# simpleURLCrawler, Author @sikumy

import requests
import signal
import validators
import sys
from colorama import init, Fore
import time
import re
import tldextract
import threading


# Ctrl C

def handler(sig, frame):
    print(Fore.RED + "\n\t--> You stopped the script! Wait until script finishes by itself\n")
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

# Filter

def filtered(r):

    filtering = re.findall('href="(.*?)"', r.text)
    
    for i in filtering:
        
        if i not in list_urls and validators.url(str(i)):

            list_urls.append(i)

            if tldextract.extract(i).domain == main_domain:

                print(Fore.BLUE + 'Internal Link: ' + i)

            else:

                print(Fore.YELLOW + 'External Link: ' + i)


# Crawler

def crawler():

    print(Fore.GREEN + '[+] Crawling ' + website)
    print("\n")
    
    try:

        filtered(requests.get(website, headers=headers))

    except:

        print(Fore.RED + 'Something wrong with URL???')
        sys.exit(1)

    for url in list_urls:

        if tldextract.extract(url).domain == main_domain and url.endswith(extensions) == False:

            try:
                
                r = requests.get(url, headers=headers)

                threading.Thread(target=filtered, args=(r,)).start()
        
            except:
                
                print(Fore.RED + 'Error Here! --> ' + url)


# Help Panel

def helpPanel():

    print(Fore.RED + "\n\tUsage: python3 simpleURLCrawler.py http(s)://<website>")
    sys.exit(0)

if (len(sys.argv) == 1):
    helpPanel()


# Global Variables

website = sys.argv[1]
main_domain =  tldextract.extract(website).domain
list_urls = []
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'} 
extensions = ('aac', 'iso', 'x-abiword', 'x-freearc', 'x-msvideo', 'vnd.amazon.ebook', 'octet-stream', 'bmp', 'x-bzip', 'x-bzip2', 'x-csh', 'css', 'csv', 'msword', 'vnd.openxmlformats-officedocument.wordprocessingml.document', 'vnd.ms-fontobject', 'epub+zip', 'gzip', 'gif', 'html', 'vnd.microsoft.icon', 'calendar', 'java-archive', 'jpeg', 'json', 'ld+json', 'x-midi', 'javascript', 'mpeg', 'mpeg', 'vnd.apple.installer+xml', 'vnd.oasis.opendocument.presentation', 'vnd.oasis.opendocument.spreadsheet', 'vnd.oasis.opendocument.text', 'ogg', 'ogg', 'ogg', 'opus', 'otf', 'png', 'pdf', 'x-httpd-php', 'vnd.ms-powerpoint', 'vnd.openxmlformats-officedocument.presentationml.presentation', 'vnd.rar', 'rtf', 'x-sh', 'svg+xml', 'x-shockwave-flash', 'x-tar', 'tiff', 'mp2t', 'ttf', 'plain', 'vnd.visio', 'wav', 'avi', 'mp4', 'webm', 'webm', 'webp', 'woff', 'woff2', 'xhtml+xml', 'vnd.ms-excel', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'vnd.mozilla.xul+xml', 'zip', '3gpp', '3gpp2', 'x-7z-compressed')



if __name__ == '__main__':


    banner = ''
    banner += "\n   _____            __    __  _____  __   _____                __       "
    banner += "\n  / __(_)_ _  ___  / /__ / / / / _ \/ /  / ___/______ __    __/ /__ ____"
    banner += "\n _\ \/ /  ' \/ _ \/ / -_) /_/ / , _/ /__/ /__/ __/ _ `/ |/|/ / / -_) __/          [By Juan Antonio González (aka Sikumy)]"
    banner += "\n/___/_/_/_/_/ .__/_/\__/\____/_/|_/____/\___/_/  \_,_/|__,__/_/\__/_/   "
    banner += "\n           /_/                                                          "
    banner += "\n\n"

    print(Fore.RED + banner)

    start_time = time.time()

    crawler()

    print(Fore.GREEN + '\n\n[+]Time of Execution: ' + str(round(time.time() - start_time, 2)) + ' seconds')
    print(Fore.GREEN + '[+] ' + str(len(list_urls)) + ' URLs found')

