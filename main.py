import re
from urllib.parse import urlparse
import requests
import urllib3
import scrape_emails
from tqdm.auto import tqdm
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
from collections import deque
import list_cleaner
import yt
import lists_and_shit
import total_scraped
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

if __name__ == '__main__':

    decider = input("Sanitize urls list? (y):")

    if decider == "y":
        urls = list_cleaner.first_url_check()
    else:
        urls = []
        f = open('input_urls.txt', 'r+')
        f1 = f.readlines()
        for xx in f1:
            urls.append(xx.rstrip())

    with open(r"input_urls.txt", 'r') as fp:
        total_lines = len(fp.readlines())
        # print('\rTotal urls loaded:', total_lines, '\nTotal emails scraped:', end="")

    num_lines = sum(1 for line in open('input_urls.txt', 'r'))

    # lists, groups, datasets etc.
    lists_and_shit.las()

    # a set of fetched emails
    emails = set()
    em_cntr = 0

    # track amount of total pages scraped between all loaded domains.
    ttl_pages_scraped = 0

    domain_cntr = 0

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    for i in (pbar := tqdm(urls, total=num_lines, position=1, leave=False)):
        # starting url. replace google with your own url.
        starting_url = i

        # a queue of urls to be crawled
        unprocessed_urls = deque([starting_url])

        # set of already crawled urls for email
        processed_urls = set()

        d = starting_url

        # domain = urlparse(d).netloc

        cntr = 0

        skipped = False

        # track amount of skipped urls, if more than 3 break loop move to next host
        skip_cntr = 0

        scrape_emails.scraper_main(unprocessed_urls,
                                   processed_urls,
                                   cntr,
                                   starting_url,
                                   urls,
                                   ttl_pages_scraped,
                                   pbar,
                                   emails,
                                   domain_cntr,
                                   skip_cntr,
                                   headers)

    list_cleaner.ctl()

    yt.cracker()
