import requests
from bs4 import BeautifulSoup as bsp

url = 'http://www.aoshu.com/tk/aszsd/xc/drxc/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.95 Safari/537.36'}

response = requests.get(url, headers=headers)
response.encoding = 'gb2312'

html = bsp(response.text, 'html.parser')

print(html)
