# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:40:48 2020

@author: 许继元
"""

from lxml import etree
import requests
import random
import re
import time
import json
import pandas as pd

def get_html(url, proxies):
    """
    @功能: 获取页面
    @参数: URL链接、代理IP列表
    @返回: 页面内容
    """
    failed = 1 # 请求失败参数
    headers = [
                  {'User-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
                  {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"},
                  {'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)"},
                  {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)"},
                  {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"},
                  {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36"}
              ]

    while True:
        try:
            if failed % 5 == 0:
                proxies  = get_proxy()
                print("请求失败次数太多,更新代理IP!")
            time.sleep(1)
            res = requests.get(url=url, headers=random.choice(headers), proxies=random.choice(proxies))
            if res.status_code == 200:
                return res.text
        except:
            print("请求失败!")
            failed = failed + 1


def get_proxy():
    """
    @功能: 获取代理IP
    @参数: 无
    @返回: 代理IP列表
    """
    proxies = [] # 存储代理IP

    url = 'http://127.0.0.1:59977/getip?price=0&word=&count=5&type=json&detail=false'
    res = requests.get(url=url)

    ip = re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', res.text) # 提取IP
    port = re.findall(r'\d{4,5}', res.text) # 提取端口号

    while True:
        try:
            # 拼接
            for i in range(5):
                ip[i] = ip[i] + ':' + port[i]
        
            # 存入proxies列表
            for i in range(5):
                proxies.append({'https': 'https://' + ip[i], 'http': 'http://' + ip[i]})
        
            return proxies
        except:
            print("获取代理时出错")
            res = requests.get(url=url)
            ip = re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', res.text) # 提取IP
            port = re.findall(r'\d{4,5}', res.text) # 提取端口号


def crawl_movies(num):
    """
    @功能: 爬取电影相关信息
    @参数: 用户数量/100(一共是100*num个用户)
    @返回: 电影列表(json)
    """
    movies_lists = []
    update = 0 # 更新代理IP的参数
    for i in range(num):
        if update % 40 == 0:
            proxies = get_proxy()
            print("更新代理IP!")
        url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=" + str(i*20)  # 每个电影列表的URL(一个页面20部电影)
        while True:
            data = get_html(url, proxies) # 获取电影列表页面
            dicts = json.loads(data) # 把数据转换成json格式
            if dicts != {"msg":"检测到有异常请求从您的IP发出，请登录再试!","r":1}:
                break

        try:
            movies_lists.append(dicts['data'])
            print("成功获取20部电影的网页!")
            update = update + 1
        except:
            print("获取资源失败")
    return movies_lists


def crawl_users(movies_lists):
    """
    @功能: 爬取用户信息
    @参数: 电影列表
    @返回: 用户列表
    """
    time.sleep(10)
    user_lists = [] # 储存所有用户的信息
    update = 0 # 用于更新代理的参数
    for i in range(len(movies_lists)):
        for j in movies_lists[i]:
            movie_url = j['url'] # 电影链接
            if update % 250 == 0:
                proxies = get_proxy()
                print("更新代理IP!")
            text = get_html(movie_url, proxies) # 获取每部电影的页面
            html = etree.HTML(text) # 解析每部电影的页面

            # 每部电影下面的5个用户评论
            for j in range(5):
                user_url = html.xpath("//div[{}]/div/h3/span[2]/a/@href".format(j+1))[0] # 电影页面下的用户主页URL
                rating_out_raw = html.xpath("//div[{}]/div/h3/span[2]/span[2]/@class".format(j+1))[0]

                try:
                    user_id = user_url.split('/')[-2] # 电影下的用户ID
                except:
                    user_id = None
                
                user_reviews_url =  user_url + 'reviews' # 用户主页的评论页面URL
                user_reviews_html = get_html(user_reviews_url, proxies) # 获取用户主页评论页面
                user_reviews_data = etree.HTML(user_reviews_html) # 解析用户主页评论页面
                
                # 进入用户主页评论页面进行爬取
                for k in range(10):
                    try:
                        movie_in_id_raw = user_reviews_data.xpath("//div[3]/div[3]/div/div[1]/div[1]/div[{}]/div/a/@href".format(k+1))[0]
                        movie_in_id = re.search(r'\d+', movie_in_id_raw).group(0) # 提取用户主页评论的第k部电影ID
                        
                        rating_in_raw = user_reviews_data.xpath("//div[{}]/div/header/span[1]/@class".format(k+1))[0]
                        rating_in = re.search(r'\d+', rating_in_raw).group(0)
                        rating_in = float(rating_in[0] + '.' + rating_in[1]) # 用户主页评论页面的评分
                        
                        user_list = [user_id, movie_in_id, rating_in]
                        user_lists.append(user_list) # 把用户主页内的电影存入
                        print("溜进去存了1条数据!")
                    except:
                        print("该用户无电影评论!")
                        break
                
                try:
                    movie_out_id = re.search(r'\d+', movie_url).group(0) # 从电影页面提取的电影ID
                except:
                    movie_out_id = None
                try:
                    rating_out = re.search(r'\d+', rating_out_raw).group(0)
                    rating_out = float(rating_out[0] + '.' + rating_out[1]) # 从电影页面下提取的用户评分
                except:
                    rating_out = None

                user_list = [user_id, movie_out_id, rating_out]
                user_lists.append(user_list)
            update += 1

            print("成功爬取5位用户信息!")

    return user_lists


def save_to_csv(user_lists):
    """
    @功能: 把用户信息存入csv文件
    @参数: 用户列表
    @返回: 无
    """
    item = ['user_id', 'movie_id', 'rating'] # 列索引
    USERS = pd.DataFrame(data=user_lists, columns=item) # 转换为DataFrame数据格式
    USERS.to_csv('douban_users.csv', mode='a', encoding='utf-8') # 存入csv文件
    print("成功将用户数据存入!")


if __name__ == '__main__':
    num = 4 # 100*num个用户
    movies_lists = crawl_movies(num)
    user_lists = crawl_users(movies_lists) # 获取用户信息
    save_to_csv(user_lists) # 存入csv文件