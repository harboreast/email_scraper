import urllib.error
import os
import requests
from header_asci import headr_asci

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    'Accept': 'application/json',
    'Connection': 'keep-alive',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br'
}


def las():
    with open('scraped_emails.txt', 'w') as f:
        f.write('test@test.com')

    # used to resize everything in terminal to fit neatly
    cmd = 'mode 101,40'
    os.system(cmd)

    headr_asci()

    email_addys = []
    scraped_emails = []


def get_urls():
    urls = []
    cleaned_urls = []
    f = open('input_urls.txt', 'r+')
    f1 = f.readlines()
    for i in f1:
        urls.append(i.rstrip())

    return urls


def del_ttl_pages_counterfile():
    if os.path.exists("ttl_pages_counter.txt"):
        os.remove("ttl_pages_counter.txt")
