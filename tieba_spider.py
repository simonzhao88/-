#coding=utf-8
import requests
from bs4 import BeautifulSoup
import time


base_url = 'http://tieba.baidu.com/f?ie=utf-8&kw=python3'
deep = 3
def get_html (url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = ('r.apparent_encoding','ignore')
        # r.encoding = 'utf-8'
        # print(r.encoding)
        return r.text
    except:
        return 'error'
# //*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a
def get_content(url):
    comments = []
    # 首先，把需要爬取信息的网页下载到本地
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    # 找到所有具有‘ j_thread_list clearfix’属性的li标签。返回一个列表类型。
    LiTags = soup.findAll('li',attrs={'class': ' j_thread_list clearfix'})
    # print(LiTags)
    # 通过循环找到每个帖子里需要的信息
    for li in LiTags:
        comment = {}
        try:
            # 开始筛选信息，并保存到字典中
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = "http://tieba.baidu.com/" + \
                              li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author '}).text.strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comments.append(comment)
        except:
            print('出错了')
    # print(comments)
    return comments
# http://tieba.baidu.com/f?ie=utf-8&kw=python3&red_tag=z1678996858
# http://tieba.baidu.com/f?kw=python3&ie=utf-8&pn=50

def Out2file(dict):
    # 将爬取到的文件写入到本地保存到当前目录的 TBTZ.txt文件中。

    with open('TBTZ.txt', 'a+') as f:
        for comment in dict:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t'.format(
                comment['title'], comment['link'], comment['name'], comment['time']))

        print('当前页面爬取完成')

url1 = 'http://tieba.baidu.com/f?kw=python3&ie=utf-8'
def main (base_url, deep):
    url_list = []
    # 将所有需要爬取的url存入列表
    for i in range(0, deep):
        url_list.append('http://tieba.baidu.com/f?kw=python3&ie=utf-8&pn=' + str(50 * i))
    print('所有的网页已经下载到本地！ 开始筛选信息。。。。')

    # 循环写入所有的数据
    for url in url_list:
        content = get_content(url)
        Out2file(content)
    print('所有的信息都已经保存完毕！')
if __name__ == '__main__':
    main(base_url, deep)

