import urllib3
import scrape_emails
from tqdm.auto import tqdm
from bs4.builder import XMLParsedAsHTMLWarning
import warnings
from collections import deque
import list_cleaner
import yt
import lists_and_shit
from fake_headers import Headers

headers = Headers(os="mac", headers=True).generate()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)


if __name__ == '__main__':

    with open(r"input_urls.txt", 'r') as fp:
        total_lines = len(fp.readlines())
        # print('\rTotal urls loaded:', total_lines, '\nTotal emails scraped:', end="")

    num_lines = sum(1 for line in open('input_urls.txt', 'r'))

    # lists, groups, datasets etc.
    lists_and_shit.las()

    urls = []
    f = open('input_urls.txt', 'r+')
    f1 = f.readlines()
    for i in f1:
        urls.append(i.rstrip())

    # a set of fetched emails
    emails = set()
    em_cntr = 0

    # track amount of total pages scraped between all loaded domains.
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

        # increment current position of domain cntr var for tracking
        if domain_cntr is not len(urls):
            domain_cntr += 1

        cntr = 0

        skipped = False

        scrape_emails.scraper_main(unprocessed_urls,
                                   processed_urls,
                                   cntr,
                                   starting_url,
                                   domain_cntr,
                                   urls,
                                   ttl_pages_scraped,
                                   pbar,
                                   pbar2,
                                   emails,
                                   headers)

    list_cleaner.ctl()

    yt.cracker()
