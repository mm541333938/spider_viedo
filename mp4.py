import requests
from bs4 import BeautifulSoup
import os
import threading


# 请求和响应
def get_requests(url):
    html = requests.get(url).content
    return html
    # print(html)


def get_content(html):
    # html.parser    lxml 解析器
    soup = BeautifulSoup(html, 'html.parser')
    """ id (#)  --  class(.)"""
    # 获取每块数据
    content = soup.select('.j-r-list-c')
    url_list = []
    for item in content:
        name = item.find('a').text
        url_mp4_path = item.select('.j-video')[0].get('data-mp4')
        url_list.append((name, url_mp4_path))
    return url_list


# 多线程下载
def get_mp4_url(url_list):
    # 当前路径下创建一个文件夹啊
    file_path = os.path.join(os.getcwd(), 'spider_mp4')
    # 判断路径是不是存在
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for item in url_list:
        if item[1] == None:
            continue
        # 对要保存得文件名长度做判断，超过30 切片截取
        name_str = item[0].strip() if len(item[0]) < 30 else item[0].strip()[:27] + '...'
        print(name_str)
        url_list_mp4 = os.path.join(file_path, '%s.%s' % (name_str.strip(), item[1][-3:]))
        print(url_list_mp4)
        t = threading.Thread(target=save_mp4(url, url_list_mp4), args=(item[1], url_list_mp4))
        t.start()


# 保存
def save_mp4(url, url_list_mp4):
    response = get_requests(url)
    with open(url_list_mp4, 'wb') as f:
        f.write(response)


if __name__ == '__main__':
    url = "http://www.budejie.com/video/2"
    url_list = get_content(get_requests(url))
    get_mp4_url(url_list)
