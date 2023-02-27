import urllib.error
import os
from header_asci import headr_asci

def las():
    with open('scraped_emails.txt', 'w') as f:
        f.write('test@test.com')

    # used to resize everything in terminal to fit neatly
    cmd = 'mode 101,40'
    os.system(cmd)

    headr_asci()

    email_addys = []
    scraped_emails = []
