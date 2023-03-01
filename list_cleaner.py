import time

import requests
from colors import bcolors


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


def first_url_check():
    start_urls = []
    urls = []
    failed_hosts_cntr = 0
    f = open('input_urls.txt', 'r+')
    f1 = f.readlines()

    for xx in f1:
        start_urls.append(xx.rstrip())

    for xxx in start_urls:
        try:
            # Get Url
            get = requests.get(xxx, verify=True, timeout=5)
            # if the request succeeds
            if get.status_code == 200:
                print(f"""{bcolors.Green}{xxx}: is reachable,  {get.status_code}""")
                urls.append(xxx)
            else:
                print(f"""{bcolors.FAIL}{xxx}: Failed. {get.status_code}""")
                failed_hosts_cntr += 1

        # Exception
        except requests.exceptions.RequestException as e:
            # print URL with Errs
            print(f"{xxx}: Failed.")
            continue

    with open(r'input_urls.txt', 'w') as fp:
        for item in urls:
            # write each item on a new line
            fp.write("%s" % item)

    time.sleep(15)
    ttl_original_urls = len(urls)

    return urls, ttl_original_urls, failed_hosts_cntr
