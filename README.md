# email_scraper

Single threaded data scraper that will loop through a txt file of predefined domains, crawl the domains and then scrape and save any found emails to txt.

To change the amount of pages scraped per host (domain) edit:

line 60 of scraper py with: 
pbar2 = tqdm(desc='while loop', total=[TOTAL AMOUNT YOU WANT TO CHANGE HERE], position=1, leave=False)

and

line 97 of scraper.py with:
if cntr >= [SAME AMOUNT DEFINED ABOVE, HERE AS WELL]:


====== Txt files associated with script ======

scraped_emails.txt is an uncleaned original list of perceieved email data.
final_scraped_emails.txt is the clensed list from scraped_emails.txt

I will update the script to be more incongnito with use of header data and proxies, just had no need at this point.
