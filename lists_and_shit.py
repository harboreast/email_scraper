import urllib.error
import os
import requests
from header_asci import headr_asci


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
