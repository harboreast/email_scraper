# email_scraper

Single threaded data scraper that will loop through a txt file of predefined domains, crawl the domains and then scrape and save any found emails to txt.

When the script starts user is prompted with an input that asks if they want to check the urls, if "y" is selected the script will check each url in the file to see if it is active, if so the script resaves the urls into input_urls.txt, otherwise it will load input_urls.txt and start crawling the domain in search of email addresses to scrape.

====== Txt files associated with script ======

scraped_emails.txt is an uncleaned original list of perceieved email data.
final_scraped_emails.txt is the clensed list from scraped_emails.txt

I will update the script to be more incongnito with use of header data and proxies, just had no need at this point.
