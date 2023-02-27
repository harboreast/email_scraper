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
