import http
import re
import socket
import requests.exceptions
import urllib3
import urllib.error
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import os
from header_asci import headr_asci
from bs4.builder import XMLParsedAsHTMLWarning
import warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

with open('scraped_emails.txt', 'w') as f:
    f.write('test@test.com')

# used to resize everything in terminal to fit neatly
cmd = 'mode 101,40'
os.system(cmd)

#include leet header asci
headr_asci()

# starting url. replace google with your own url.
with open(r"input_urls.txt", 'r') as fp:
    total_lines = len(fp.readlines())
    # print('\rTotal urls loaded:', total_lines, '\nTotal emails scraped:', end="")

num_lines = sum(1 for line in open('input_urls.txt', 'r'))

# group for the end of the script to help clean up
# and remove dupes/banned keywords.
email_addys = []
# group to contain scramed email addresses.
scraped_emails = []

# import domains to be crawled and scraped.
urls = []
f = open('input_urls.txt', 'r+')
f1 = f.readlines()
for i in f1:
    urls.append(i.rstrip())

# a set of fetched emails
emails = set()
em_cntr = 0

# track amount of total pages scraped between
# all loaded domains.
ttl_pages_scraped = 0

domain_cntr = 0

# second instance of progress bar (the second printed on the terminal screen)
pbar2 = tqdm(desc='while loop', total=333, position=1, leave=False)

for i in (pbar := tqdm(urls, total=num_lines, position=0, leave=True)):

    # starting url. replace google with your own url.
    starting_url = i

    # a queue of urls to be crawled
    unprocessed_urls = deque([starting_url])

    # set of already crawled urls for email
    processed_urls = set()

    # increment current positison of domain cntr var for tracking
    if domain_cntr is not len(urls):
        domain_cntr += 1

    # track placement in various iterations and loops to
    # maintain smooth and working functionality of tqdm integration (progress bar)
    cntr = 0

    # boolean to help maintain consistent tracking of iterations and
    # maintain working tqdm functionality with dual prograess bars
    skipped = False

    # process urls one by one from unprocessed_url queue until queue is empty
    while len(unprocessed_urls):

        # move next url from the queue to the set of processed urls
        url = unprocessed_urls.popleft()
        processed_urls.add(url)
        # print(url) # use for debugging
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        if cntr >= 333:
            cntr = 0
            pbar2.reset()
            break

        if "javascript" in url:
            continue
        if "void" in url:
            continue
        if "java" in url:
            continue
        if "WebForm" in url:
            continue
        if "PostBack" in url:
            continue
        if "tel:" in url:
            continue
        if "smartlink" in url:
            continue

        d = starting_url

        domain = re.findall('(\w+)://',
                            d)
        domain = re.findall('://www.([\w\-\.]+)',
                            d)
        domain = str(domain)
        domain = domain.replace("'", "")
        domain = domain.replace("[", "")
        domain = domain.replace("]", "")

        if domain_cntr is not len(urls):
            pbar2.set_description(f"Host: {domain}: Progress")

        if domain in url:
            
            h = requests.head(url)
            header = h.headers
            content_type = header.get('content-type')

            # print(content_type, cntr) # use for debugging

            if content_type is None:
                continue
            elif "video" in content_type:
                skipped = True
                continue
            elif "application" in content_type:
                skipped = True
                continue
            elif "image" in content_type:
                skipped = True
                continue

            try:
                response = requests.get(url, timeout=10, verify=True)
                skipped = False
            except requests.exceptions.SSLError as e:
                skipped = True
                continue
            except requests.exceptions.RequestException as e:
                skipped = True
                continue
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                # ignore pages with errors and continue with next url
                skipped = True
                continue
            except urllib.error.HTTPError as e:
                skipped = True
                # status = e.__dict__
                continue
            except urllib.error.URLError as e:
                skipped = True
                # status = e.__dict__
                continue
            except socket.error as e:
                skipped = True
                # if e.errno != errno.ECONNRESET:
                continue
            except http.client.IncompleteRead as e:
                skipped = True
                continue

            try:
                response = requests.get(url, timeout=10, verify=True)
                ttl_pages_scraped += 1
                pbar2.update(1)
                skipped = False
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                # ignore pages with errors and continue with next url
                skipped = True
                continue
            except requests.exceptions.SSLError as e:
                skipped = True
                continue

            # extract all email addresses and add them into the resulting set
            # You may edit the regular expression as per your requirement
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)

            # print(emails)
            # create a beautiful soup for the html document
            soup = BeautifulSoup(response.text, 'lxml')

            # Once this document is parsed and processed, now find and process all the anchors i.e. linked urls in
            # this ocument

            for anchor in soup.find_all("a"):
                # extract link url from the anchor
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                link_p_bar = (link[:33])

                # resolve relative links (starting with /)
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                # add the new url to the queue if it was not in unprocessed list nor in processed list yet
                if not link in unprocessed_urls and not link in processed_urls:
                    unprocessed_urls.append(link)

                with open(r'scraped_emails.txt', 'w') as fp:
                    for item in emails:
                        item = item.lower()
                        # write each item on a new line
                        fp.write("%s \n" % item)

        if not skipped:
            cntr += 1

        email_total_cnt = int(len(emails))
        em_cntr = email_total_cnt
        with open(r"scraped_emails.txt", 'r') as fe:
            fe_total_lines = len(fe.readlines())
        pbar.set_description(f"Pages Scanned: {ttl_pages_scraped}, Scraped Emails: {em_cntr}, Progress")

from footer_asci import ytc

# clean up the list

def ctl():
    keywords = ['.gov', '.png', 'jpg', 'png', 'set()', 'PNG', 'JPG', 'jpeg', 'JPEG', 'wixpress', '2x.png', '2x.jpg']
    scraped_email_addys = []
    final_email_addys = []
    with open(r"scraped_emails.txt", 'r') as emails:
        for x in emails:
            x = x.replace(" ", "")
            scraped_email_addys.append("%s" % x)

    for x in scraped_email_addys:
        save_or_not = False
        if len(x) > 7:
            if len(x):
                for kw in keywords:
                    if kw not in x:
                        save_or_not = True
                    else:
                        save_or_not = False
                        # print("found", kw, "in", x)
                        break
        else:
            save_or_not = False
            break

        if save_or_not:
            final_email_addys.append(x)

    with open(r'final_scraped_emails.txt', 'w') as fp:
        for item in final_email_addys:
            # write each item on a new line
            fp.write("%s" % item)


ctl()
