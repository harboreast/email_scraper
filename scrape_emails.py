import http
import re
import socket
import time
import urllib

import requests.exceptions
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from tld import get_tld, get_fld
from tqdm.auto import tqdm
import urllib3
from urllib3.exceptions import ReadTimeoutError
import sys
import validators

try:
    from requests.packages.urllib3.exceptions import ReadTimeoutError
except:
    try:
        from urllib3.exceptions import ReadTimeoutError

        ReadTimeoutError
    except:
        print("Something seems wrong with the urllib3 installation.\nQuitting")
        sys.exit(const.EFatal)


def skip_checka(skip_cntr):
    if skip_cntr >= 3:
        skip_this_bitch = True
    else:
        skip_this_bitch = False
    return skip_this_bitch


def force_fill_bar(pbar2):
    for i in range(1, 100):
        pbar2.update(1)
        time.sleep(.01)


def scraper_main(unprocessed_urls,
                 processed_urls,
                 cntr,
                 starting_url,
                 urls,
                 pbar,
                 emails,
                 domain_cntr,
                 skip_cntr,
                 headers,
                 ttlscrps,
                 max_to_crawl):
    # second instance of progress bar (the second printed on the terminal screen)
    pbar2 = tqdm(desc='Loading next host...', total=max_to_crawl, position=1, leave=False)

    # process urls one by one from unprocessed_url queue until que is empty
    while len(unprocessed_urls):

        # move next url from the queue to the set of processed urls
        url = unprocessed_urls.popleft()
        processed_urls.add(url)
        # print(url) # use for debugging
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        # validate url to search for malformed urls that will break script
        if not validators.url(url):
            force_fill_bar(pbar2)
            break

        # check one final time to see if url is accessible

        try:
            # Get Url
            get = requests.get(url, verify=True, timeout=5)
            # if the request succeeds
            if get.status_code == 200:
                d = 'g'
            else:
                force_fill_bar(pbar2)
                break

        except requests.exceptions.RequestException as e:
            break

        # if 100 pages on this host have been checked break loop move to next item in list
        if cntr >= max_to_crawl:
            cntr = 0
            # # pbar2.refresh()
            break

        # check url for banned keywords
        if "javascript" in url:
            force_fill_bar(pbar2)
            break
        if "void" in url:
            force_fill_bar(pbar2)
            break
        if "java" in url:
            force_fill_bar(pbar2)
            break
        if "WebForm" in url:
            force_fill_bar(pbar2)
            break
        if "PostBack" in url:
            force_fill_bar(pbar2)
            break
        if "tel:" in url:
            force_fill_bar(pbar2)
            break
        if "smartlink" in url:
            force_fill_bar(pbar2)
            break

        try:
            # Get Url
            get = requests.get(url, verify=False, headers=headers, timeout=10)
            # if the request succeeds
            if get.status_code == 200:
                d = "g"
            else:
                force_fill_bar(pbar2)
                break

        # Exception
        except requests.exceptions.RequestException as e:
            force_fill_bar(pbar2)
            break
        except urllib.error.URLError:
            force_fill_bar(pbar2)
            break

        # strip the domain name from the url just name and tld
        d = get_fld(starting_url, fix_protocol=True)

        # # pbar2.refresh()
        pbar2.set_description(f"Host: {d}: Progress")

        if d in url:

            h = requests.head(url, verify=False, headers=headers, timeout=10)

            header = h.headers
            content_type = header.get('content-type')

            # print(content_type, cntr) # use for debugging

            if content_type is None:
                force_fill_bar(pbar2)
                skipped = True
                cntr = 0
                # # pbar2.refresh()
                continue

            elif "video" in content_type:
                force_fill_bar(pbar2)
                skipped = True
                cntr = 0
                # # pbar2.refresh()
                continue

            elif "application" in content_type:
                force_fill_bar(pbar2)
                skipped = True
                cntr = 0
                # # pbar2.refresh()
                continue

            elif "image" in content_type:
                force_fill_bar(pbar2)
                cntr = 0
                # # pbar2.refresh()
                continue

            try:
                response = requests.get(url, verify=False, headers=headers, timeout=10)
                skipped = False
            except urllib.error.URLError:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except ReadTimeoutError:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except requests.exceptions.SSLError as e:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except requests.exceptions.RequestException as e:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                force_fill_bar(pbar2)
                # ignore pages with errors and continue with next url
                skipped = True
                continue
            except urllib.error.HTTPError as e:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except urllib.error.URLError as e:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except socket.error as e:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except http.client.IncompleteRead as e:
                force_fill_bar(pbar2)
                skipped = True
                continue

            # print("Crawling URL %s" % url)

            try:
                response = requests.get(url, verify=False, headers=headers, timeout=10)
                ttlscrps.append('1') # dummy data to track total pages scanned
                pbar2.update(1)
                skipped = False

            except urllib.error.URLError:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except ReadTimeoutError:
                force_fill_bar(pbar2)
                skipped = True
                continue
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                force_fill_bar(pbar2)
                # ignore pages with errors and continue with next url
                skipped = True
                continue
            except requests.exceptions.SSLError as e:
                force_fill_bar(pbar2)
                skipped = True
                continue

            # extract all email addresses and add them into the resulting set
            # You may edit the regular expression as per your requirement
            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
            emails.update(new_emails)

            # print(emails)
            # create a beautiful soup for the html document
            soup = BeautifulSoup(response.text, 'lxml')

            # Once this document is parsed and processed, now find and process all the anchors i.e. linked urls in doc
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

        ttl_pages_scraped = int(len(ttlscrps))

        email_total_cnt = int(len(emails))
        em_cntr = email_total_cnt
        with open(r"scraped_emails.txt", 'r') as fe:
            fe_total_lines = len(fe.readlines())
        pbar.set_description(f"Pages Scanned: {ttl_pages_scraped}, Scraped Emails: {em_cntr}, Progress")
