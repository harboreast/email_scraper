import requests


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
    wcntr = 0
    cntr = 0

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
                print(f"{xxx}: is reachable,  {get.status_code}")
                cntr += 1
                urls.append(xxx)
            else:
                print(f"{xxx}: Failed. {get.status_code}")
                wcntr += 1

        # Exception
        except requests.exceptions.RequestException as e:
            # print URL with Errs
            print(f"{xxx}: Failed.")
            continue

    print("Initially Loaded:", len(urls))
    print(f"Working: {cntr} \n Failed: {wcntr}")
    cntr = 0
    return urls
