#!/usr/bin/python
__author__ = 'agoss'

from datetime import datetime
import os
import re

from bs4 import BeautifulSoup
import requests


def main():
    t_start = datetime.now()
    global page_link
    global season

    print '\n**********START**********\n' + str(t_start.strftime('%Y%m%d__%H:%M:%S'))

    base_link = 'http://scores.collegesailing.org/'
    page_list = []

    i = 17  # loop through past fall and spring seasons dating back to 2010
    while i >= 10:
        page_list.insert(len(page_list), base_link + 'f' + str(i) + '/')  # fall
        page_list.insert(len(page_list), base_link + 's' + str(i) + '/')  # spring
        i -= 1

    for page_link in page_list:
        print '\nScraping web page: ' + page_link
        page_content = get_page_content(page_link)
        season = page_link[-4:-1]

        print 'Extracting all html elements where table row is stored...\n'
        for row in page_content.select('tr[class*="row"]'):
            sub_page = re.findall(r'"([^"]*)"', str(row.next_element.contents[0]))
            print sub_page[0]
            if 'Team' in str(row.contents[3]):
                continue
            else:
                perform_sub_page_extraction(sub_page[0])
            with open("scores.txt", "a") as my_file:
                my_file.write('\n')

    t_end = datetime.now()
    os.rename('./scores.txt', './' + str(t_end.strftime('%Y%m%d_%H%M%S_')) + 'scores.txt')
    print '\n**********DONE**********\n' + str(t_end - t_start) + ' elapsed'


def get_page_content(pagelink):
    try:
        page_response = requests.get(pagelink, timeout=5)  # parse html
        if page_response.status_code == 200:
            page_content = BeautifulSoup(page_response.content, "html.parser")  # extract page content
            return page_content
        else:
            print(page_response.status_code)
            return
    except requests.Timeout as e:
        print(str(e))
    except:
        raise  # other exception, catch-all


def perform_sub_page_extraction(sub_page):
    sub_page_link = page_link + sub_page
    page_content = get_page_content(sub_page_link)
    if page_content is None:
        pass  # skip 404 pages or other status codes
    else:
        first = True
        # extract all html elements where table row is stored
        for row in page_content.select('tr[class*="row"]'):
            if first:
                with open("scores.txt", "a") as my_file:
                    my_file.write(season + '|' + sub_page + '|')
            else:
                with open("scores.txt", "a") as my_file:
                    my_file.write('\n' + season + '|' + sub_page + '|')
            i = 1
            while i < len(row.contents):
                with open("scores.txt", "a") as my_file:
                    data = re.search(r'>(.*?)<', str(row.contents[i])).group(1)
                    if i == len(row.contents) - 1:
                        my_file.write(data)
                    elif 'schoolname' in str(row.contents[i]):
                        data = re.search(r'"name">(.*?)<', str(row.contents[i])).group(1)
                        my_file.write(data + '|')
                    elif len(data) > 0:
                        my_file.write(data + '|')
                first = False
                i += 1


if __name__ == '__main__':
    try:
        main()
    except:
        raise
