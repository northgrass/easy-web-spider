#encoding=utf-8
from lxml import html
import urllib2
import re
import requests

base_url = 'https://movie.douban.com/top250?{}'
first_page = 'https://movie.douban.com/top250'
headline = ".//div[@id='content']/h1/text()"
next_page_href = ".//div[@class='paginator']/span[@class='next']/a/@href"
next_page_tag = ".//div[@class='paginator']/span[@class='next']/a"
group_url = ".//div[@class='article']/ol[@class='grid_view']/li"
groupsAll = []
file = file = open('douban_test.txt', 'a+')

while len(groupsAll) < 50:

    next_page = first_page
    # x = html.parse(next_page)
    x = html.parse(urllib2.urlopen(next_page))
    groups = x.xpath(group_url)
    groupsAll = groupsAll + groups
    next_page_flag = x.xpath(next_page_tag)
    if next_page_flag:
        next_page = base_url.format(x.xpath(next_page_href))
    else:
        next_page = None
        print "No Next Pages!"

for group in groupsAll:
    titleAll_url = ".//div[@class='info']/div[@class='hd']/a/span/text()"
    titleAll = group.xpath(titleAll_url)
    out = ""
    for title in titleAll:
        # print title
        regex_first = re.compile("\s*\/\s+")
        regex_second = re.compile("^\S\/\S")
        new_title = re.sub(regex_first,'/'.decode('utf-8'),title)
        re_title = re.sub(regex_second,'/'.decode('utf-8'),new_title)

        out = out + re_title

    out = out + "\t"

    player_url = ".//div[@class='info']/div[@class='hd']/span[@class='playable']/text()"
    player = group.xpath(player_url)
    if player:
        out = out + player[0] + "\t"
    else:
        out = out + '[不可播放]'.decode('utf-8') + "\t"

    score_url = ".//div[@class='info']/div[@class='bd']/div[@class='star']/span[@class='rating_num']/text()"
    score = group.xpath(score_url)
    out = out + score[0] + "\t"

    comment_num_url = ".//div[@class='info']/div[@class='bd']/div[@class='star']/span[4]/text()"
    comment_num = group.xpath(comment_num_url)
    out = out + comment_num[0] + "\t"

    introduction_url = ".//div[@class='info']/div[@class='bd']/p[@class='quote']/span[@class='inq']/text()"
    introduction = group.xpath(introduction_url)
    out = out + introduction[0] + "\t"

    actors_url = ".//div[@class='info']/div[@class='bd']/p[1]/text()"
    actors = group.xpath(actors_url)
    if actors:
        for actor in actors:
            if "导演".decode('utf-8') in actor:
                director_extract = re.compile(".*?:(.*?)[^a-zA-z]+[:|\.]")
                director = re.findall(director_extract, actor)
                out = out + director[0].strip() + "\t"
                # print director[0].strip()

                stardom_ectract = re.compile(".*?[a-zA-z].*?:(.*?)$")
                stardom = re.findall(stardom_ectract, actor)
                if stardom:
                    stardoms = stardom[0].strip()
                else:
                    stardoms =  '主演未显示'.decode('utf-8')

                out = out + stardoms + "\t"

                # print actor
            else:
                regex_extract = re.compile(".*?(\d{4}).*?")
                year_match = re.findall(regex_extract, actor)
                if year_match:
                    year = year_match[0].strip()
                else:
                    year = '无年份'.decode('utf-8')
                out = out + year + "\t"

    else:
        print "No Actors!"

    file.write(out.encode('utf-8') + '\n')






