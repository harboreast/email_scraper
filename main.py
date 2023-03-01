import urllib3
import scrape_emails
from tqdm.auto import tqdm
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
from collections import deque
import list_cleaner
import total_scraped
import yt
import lists_and_shit
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

scraped = 0  # setting a default to avoid errors
if not os.path.exists('ttl_pages_counter.txt'):
    # file does not exist therefore will create a new file with a value of 0
    ttl_pages_scraped = int(total_scraped.create_the_txtfile())

first_run = True

# load domains to crawl
urls = lists_and_shit.get_urls()

# sum of total hosts/domains to scrape not sure why I did this twice.
num_lines = sum(1 for line in open('input_urls.txt', 'r'))

# lists, groups, datasets etc.
lists_and_shit.las()

# a set of fetched emails
emails = set()

ttlscrps = []

# count total hosts/domains to scrape
domain_cntr = 0

# set pbar vars here once to avoid a blank loading bar if navigation bad urls initially
ttl_pages_scraped = 0
em_cntr = 0

# total amount of maximum pages per host to crawl
max_to_crawl = 33

for i in (pbar := tqdm(urls, total=num_lines, position=0, leave=False)):

    if first_run:
        pbar.set_description(f"Pages Scanned: 0, Scraped Emails: 0, Progress")
        first_run = False

    # starting url. replace google with your own url.
    starting_url = i

    # a queue of urls to be crawled
    unprocessed_urls = deque([starting_url])

    # set of already crawled urls for email
    processed_urls = set()

    # first url to scrape/scrape etc.
    d = starting_url

    # counter used for various tracking functions
    cntr = 0

    # reset skipped variable to false with iteration to new host
    skipped = False

    # track amount of skipped urls, if more than 3 break loop move to next host
    skip_cntr = 0

    scrape_emails.scraper_main(unprocessed_urls,
                               processed_urls,
                               cntr,
                               starting_url,
                               urls,
                               pbar,
                               emails,
                               domain_cntr,
                               skip_cntr,
                               lists_and_shit.headers,
                               ttlscrps,
                               max_to_crawl)

# final sanitization of emails list to remove
# data scraped that is not an email address
list_cleaner.ctl()

# However,
# my Faith in Thee remains
# Unwavered -
# my Faith
# in the Holy Arts
# and
# the Holy Flowcharts -
# until my binary Departs
# and Your Simulation Restarts.
yt.cracker()

# print final stats
total_scraped.final_stats(num_lines)

# script is finished, delete ttl_pages_counter.txt file
lists_and_shit.del_ttl_pages_counterfile()

