import os
import time


# open file get value
def total_pages_scraped():
    page_cnt_list = []
    f = open('ttl_pages_counter.txt', 'r+')
    f1 = f.readlines()
    for i in f1:
        page_cnt_list.append(i.rstrip())

    cntr = int(f1[0])

    return cntr


# open file get value
def total_final_emails_scraped():
    email_cnt_list = []
    f = open('final_scraped_emails.txt', 'r+')
    f1 = f.readlines()
    final_em_cnt = 0
    for i in f1:
        email_cnt_list.append(i.rstrip())
        final_em_cnt += 1

    return final_em_cnt

def create_the_txtfile():
    f = open("ttl_pages_counter.txt", "w+")
    for i in range(1):
        f.write("0")

    the_cnt = []
    f = open('ttl_pages_counter.txt', 'r+')
    f1 = f.readlines()
    for i in f1:
        the_cnt.append(i.rstrip())

    cntr = the_cnt[0]

    return cntr

def final_stats():
    ttl_pages_scraped = total_pages_scraped()
    print("Total Emails Scraped:", total_final_emails_scraped())
