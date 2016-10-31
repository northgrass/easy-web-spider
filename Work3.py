#encoding=utf-8
from lxml import html

y = html.parse('http://music.baidu.com/top/dayhot')
next_page = y.XPATH("//a[@class='page-navigator-next']/@href")
print next_page

print [str(next_page[0]).strip()]

print ['http://music.baidu.com' +
       str(next_page[0])
           .replace('\\t', '')
           .replace('\\n', '')
           .replace('[\'', '').replace('\']', '')
           .strip()
      ]

