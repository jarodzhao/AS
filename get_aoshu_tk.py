import sqlite3
import time
import requests
from bs4 import BeautifulSoup as bsp


def in_db(menu_item):
	conn = sqlite3.connect('aoshu.db3')
	cursor = conn.cursor()

	cursor.execute('create table if not exists tk_menu (id_, title, title_url, item, item_url)')
	sql = "INSERT INTO tk_menu VALUES ('" + str(time.time()) + "', '" + menu_item["title"] + "', '" + menu_item["title_url"] + "', '" + menu_item["item"] + "', '" + menu_item["item_url"] +"')"
	print(sql)
	cursor.execute(sql)

	conn.commit()
	conn.close()


url = 'http://www.aoshu.com/tk/aszsd/xc/drxc/'
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}

r = requests.get(url, headers=headers)
r.encoding = 'gb2312'
content = bsp(r.text, 'html.parser')

tk_menu = content.find('div', class_='tk-menu')
class_1 = tk_menu.find_all('h3')

menu_list = []

for t in class_1:
	# 菜单项
	list_item = {}

	# 大标题
	title = t.find('a').text
	title_url = t.find('a')['href']

	# 小标题
	items = t.next_sibling.next_sibling.find_all('a')
	menu_items = []

	for item in items:
		menu_items.append(item.text + '&&' + item['href'])

	# 字典来
	list_item['title'] = title
	list_item['title_url'] = title_url
	list_item['items'] = menu_items

	menu_list.append(list_item)


for li in menu_list:
	menu_item = {}
	menu_item['title'] = (li['title'])
	menu_item['title_url'] = (li['title_url'])
	items = li['items']
	for i in items:
		i_0 = i.split('&&')
		menu_item['item'] = (i_0[0])
		menu_item['item_url'] = (i_0[1])
		in_db(menu_item)

