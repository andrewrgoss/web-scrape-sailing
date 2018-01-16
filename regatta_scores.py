#!/usr/bin/python
__author__ = 'agoss'

import re

from bs4 import BeautifulSoup
import requests


def main():
    global page_link
    page_link = 'http://scores.collegesailing.org/f17/'  # fetch the content for url
    page_content = get_page_content(page_link)

    # extract all html elements where table row is stored
    for row in page_content.select('tr[class*="row"]'):
        sub_page = re.findall(r'"([^"]*)"', str(row.next_element.contents[0]))
        print sub_page[0]
        perform_sub_page_extraction(sub_page[0])
        # print row.next_element.contents[0]

    print '\n**********DONE**********\n'


def get_page_content(page_link):
    try:
        page_response = requests.get(page_link, timeout=5)  # parse html
        if page_response.status_code == 200:
            page_content = BeautifulSoup(page_response.content, "html.parser")  # extract page content
        else:
            print(page_response.status_code)  # notify, try again
    except requests.Timeout as e:
        print(str(e))
    except:
        raise  # other exception, catch-all
    return page_content


def perform_sub_page_extraction(sub_page):
    sub_page_link = page_link + sub_page
    page_content = get_page_content(sub_page_link)
    first = True

    # extract all html elements where table row is stored
    for row in page_content.select('tr[class*="row"]'):
        if first:
            with open("scores.txt", "a") as my_file:
                my_file.write(sub_page + '|')
        else:
            with open("scores.txt", "a") as my_file:
                my_file.write('\n' + sub_page + '|')
        i = 1
        while i < len(row.contents):
            with open("scores.txt", "a") as my_file:
                data = re.search(r'>(.*?)<', str(row.contents[i])).group(1)
                if len(data) > 0:
                    my_file.write(data + '|')
            first = False
            i += 1


if __name__ == '__main__':
    try:
        main()
    except:
        raise
