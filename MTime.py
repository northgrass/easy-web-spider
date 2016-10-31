#encoding=utf-8
from lxml import html
from time import sleep

x = html.parse('http://www.mtime.com/hotest/')
groupsAll = []
# groups = x.xpath("//div[@class='mtiplist']")

base_url = 'http://www.mtime.com/hotest/{}'
next_page = "http://www.mtime.com/hotest/"
next_button_xpath = "//a[@id='key_nextpage']/@href"

file = open('mtime_info2.txt', 'a+')
file.write('电影名称\t评分\t导演\t演员\t上映日期\t排名情况\n')
while len(groupsAll) < 50 and next_page:
    dom = html.parse(next_page)
    groups = dom.xpath("//div[@class='mtiplist']")
    groupsAll += groups
    next_pages = dom.xpath(next_button_xpath)
    if next_pages:
        next_page = base_url.format(next_pages[0])
    else:
        print "No next button found"
        next_page = None
    sleep(1)

for group in groupsAll:
    titles = group.xpath(".//dt/a/text()")
    scores = group.xpath(".//div[@class='score']/strong/text()")
    director_name = group.xpath(".//dl/dd/ul/li[1]/text()")
    # print director_name[0].strip()=='导演：'.decode('utf-8')
    # 因为导演可能没有，但是主演都是有的
    if director_name[0].strip() == '导演：'.decode('utf-8'):
        director = group.xpath(".//dl/dd/ul/li[1]/a/text()")
        actors = group.xpath(".//dl/dd/ul/li[2]/*/text()")
    else:
        actors = group.xpath(".//dl/dd/ul/li[1]/*/text()")
        director = ['无导演'.decode('utf-8')]

    # 首先爬出3个li标签，通过看li标签下是否有a标签来判断是否是“上映时间”
    timeList = group.xpath(".//dl/dd/ul/li")
    # print timeList
    timeFlag = timeList[-1].xpath("./a")
    # print timeFlag
    if len(timeFlag) == 0:
        time = timeList[-1].xpath("./text()")
        # print time
    else:
        time = ['无上映时间'.decode('utf-8')]
    # print time


    ranks = group.xpath(".//dl/dd/p/*/text()")

    out = titles[0].replace("  ".decode('utf-8'),"----".decode('utf-8'))
    if len(scores) == 1 :
        out = out + "\t" + scores[0]
    else:
        out = out + "\t" + '无评分'.decode('utf-8')

    out = out + "\t" + director[0]+ "\t"
    for actor in actors:
        out = out + actor + ","
    # 为了去掉最后一个逗号
    out = out[:-1]
    # if time:
    out = out + "\t" + time[0].replace("上映日期： ".decode('utf-8'),"") + "\t"
    # else:
    #     out = out + "\t" + "上映时间未定\t".decode('utf-8')
    for rank in ranks:
        out = out + rank.replace(" ".decode('utf-8'),":".decode('utf-8')) + ","
    out = out[:-1]
    file.write(out.encode('utf-8')+"\n")

file.close()


