#encoding=utf-8
from lxml import html
from time import sleep
titles = []
base_url = 'http://www.mtime.com/hotest/{}'
next_page = "http://www.mtime.com/hotest/"

# These are the xpaths we determined from snooping
next_button_xpath = "//a[@id='key_nextpage']/@href"
headline_xpath = "//div[@class='picbox']/dl/dt/a/text()"

while len(titles) < 50 and next_page:
    dom = html.parse(next_page)
    headlines = dom.xpath(headline_xpath)
    print "Retrieved {} titles from url: {}".format(len(headlines), next_page)
    titles += headlines
    next_pages = dom.xpath(next_button_xpath)
    print next_pages
    if next_pages:
        next_page = base_url.format(next_pages[0])
        print next_page
    else:
        print "No next button found"
        next_page = None
    sleep(3)
for title in titles[:15]:
    print title

with open('mtime_titles.txt', 'wb') as out:
    out.write('\n'.join(titles).encode('utf-8'))
with open('mtime_titles.txt') as f:
    titles_ = f.readlines()

print "Well, we got {} Hot Movies!".format(len(titles_))

