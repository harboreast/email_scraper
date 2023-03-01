# email_scraper

Script is designed to loop through a text file of websites, crawl them, and search for email contact data. If found, the script will save the data. 

=== Associated text files ====

input_urls.txt - this is the list of urls the script will loop through format must be "http://www.domain.com" (or https).

ttl_pages_counter.txt - this file stores the current amount of single webpages that have been crawled, I did this to later add "start from where you left off functionality". Which I will add in coming days. The script will create this file on it's own and delete it after it's finished working. If the script crashes, for now you must manually delete this final before running the script.

scraped_emails.txt - this is the intial set of percieved scraped email data, at times "junk data" (non email address) will be scraped, when the script is done looping through the input_urls, a final sanitization will be done of the list to remove any unwanted data.

final_scraped_emails.txt - sanitized cleaned list of email contact data without any of previously discussed "junk data" (.jpg, @wix, etx.)

Note:
Script is designed to ignore javascript and media files. 
