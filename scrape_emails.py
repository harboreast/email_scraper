from urllib.parse import urlsplit
import re
import http
import socket
import requests.exceptions
from bs4 import BeautifulSoup


def scraper_main(unprocessed_urls,
                 processed_urls,
                 cntr,
                 starting_url,
                 domain_cntr,
                 urls,
                 ttl_pages_scraped,
                 pbar,
                 pbar2,
                 emails,
                 headers):

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

        # check url for banned keywords
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

        # pbar2.refresh()
        # if domain_cntr is not len(urls):
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
                response = requests.get(url, timeout=10, verify=True, headers=headers)
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

            # print("Crawling URL %s" % url)

            try:
                response = requests.get(url, timeout=10, verify=True, headers=headers)
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

        email_total_cnt = int(len(emails))
        em_cntr = email_total_cnt
        with open(r"scraped_emails.txt", 'r') as fe:
            fe_total_lines = len(fe.readlines())
        pbar.set_description(f"Pages Scanned: {ttl_pages_scraped}, Scraped Emails: {em_cntr}, Progress")
