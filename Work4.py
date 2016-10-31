#encoding=utf-8
from lxml import html
import requests

url = 'https://book.douban.com/series/1163?page=11'
page = requests.get(url)
y = html.fromstring(page.content)
stars = y.xpath("//div[@class='star clearfix']/*")
for star in stars:
    print star.attrib['class'], star.text.strip() if star.attrib['class'] == 'rating_nums' or star.attrib['class'] == 'pl'  else ''