=== Installation notes ===

pip3 install urllib3

pip3 install requests

pip3 install bs4

pip3 install tld

pip3 install tqdm

pip3 install validators

pip3 install lxml


=== Gangster Scraper ===

Script is designed to loop through a text file of websites, crawl them, and search for email contact data. If found, the script will save the data. The amount of maximum pages per host to attempt to crawl is set in the variable called "max_crawl_pages", which is by default set to 33 and located on line 45 of main.py

If the script runs out of urls to crawl it will move on to the next host, it will also do this if a wide array of exceptions are raised with urllib3 and requests, etc. If you are only scraping one or two hosts, and they are large corporations or big websites, raise the number on the max_crawl_pages variable higher (xxx-x,xxx). The script is single threaded, it is not the quickest but the data it yields you should be beneficial.

If you are scraping a large amount of smaller "mom and pop" or "hobby" websites, max_crawl_pages should be defined at a lower value, that is for you to decide.

=== Associated text files ====

input_urls.txt - this is the list of urls the script will loop through format must be "http://www.domain.com" (or https).

ttl_pages_counter.txt - this file stores the current amount of single webpages that have been crawled, I did this to later add "start from where you left off functionality". Which I will add in coming days. The script will create this file on it's own and delete it after it's finished working. If the script crashes, for now you must manually delete this file before running the script.

scraped_emails.txt - this is the intial set of percieved scraped email data, at times "junk data" (non email address) will be scraped, when the script is done looping through the input_urls, a final sanitization will be done of the list to remove any unwanted data.

final_scraped_emails.txt - sanitized cleaned list of email contact data without any of previously discussed "junk data" (.jpg, @wix, etx.)

