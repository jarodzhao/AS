import sqlite3
import time
import random
import requests
from bs4 import BeautifulSoup as bsp

first = True


def fetch_list(lis):
    for item in lis:
        a = item.find('a')
        it = a.text
        ih = a['href']
        print('%s\n%s' % (it,ih))


def get_xc_item2(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/55.0.2883.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'

    # 题库列表 html
    content = bsp(r.text, 'html.parser')
    return content


def fetch_tk_item(content, url):

    # pages
    page_html = content.find('div', class_='btn-pages')
    pages_a_s = page_html.find_all('a')

    # 翻页列表，包含开头的[上一页]和末尾的[下一页]
    pages = []
    for p in pages_a_s:
        pages.append(p.text)

    # 总页数
    max_page = pages.pop(len(pages) - 2)

    # 列表页中的所有列表项，第一页
    global first
    lis = None

    for i in range(1, int(max_page) + 1):
        print('max_page=%s | page=%s | first=%s\n%s' % (max_page, i, first, url))
        if first:
            lis = content.find('div', class_='tk-con').find_all('li')
            # print('url = %s' % url)
            first = False
        else:
            # 第二页开始到最大页数
            url_t = url + 'index_' + str(i) + '.shtml'

            content = get_xc_item2(url_t)  # 这里 content 是页面 html 源码
            lis = content.find('div', class_='tk-con').find_all('li')
            print('url_t = %s' % url_t)

        fetch_list(lis)

        print('------------ 休息一下， 5 秒后继续... -------\n')
        time.sleep(5)

    first = True


def get_xc_item(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/55.0.2883.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    r.encoding = 'gb2312'

    # 题库列表 html
    content = bsp(r.text, 'html.parser')

    fetch_tk_item(content, url)

    wait = int(random.random() * 5)
    print('等待 %s 秒后继续下一页...\n' % wait)
    time.sleep(wait)


def get_xc():
    conn = sqlite3.connect('aoshu.db3')
    cur = conn.cursor()

    sql = "select * from tk_menu where title='行程问题'"
    rs = cur.execute(sql)

    for item in rs:
        url = item[4]
        get_xc_item(url)

    cur.close()
    conn.close()


if __name__ == '__main__':
    get_xc()
