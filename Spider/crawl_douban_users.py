# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:40:48 2020

@author: 许继元
"""

import json
import random
import re
import time

import pandas as pd
import requests
from lxml import etree


def get_html(url):
    """
    @功能: 获取页面
    @参数: URL链接
    @返回: 页面内容
    """
    while True:
        try:
            time.sleep(random.randint(2, 3))
            res = requests.get(url, headers={'User-Agent': ua.chrome})
            if res.status_code == 200:
                return res.text
        except Exception as e:
            print("请求失败, 原因是 %s" % e)


def crawl_movies(num):
    """
    @功能: 爬取电影相关信息
    @参数: 用户数量/100(一共是100*num个用户)
    @返回: 电影列表(json)
    """
    movies_lists = []
    for i in range(num):
        url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=" + str(i * 20)  # 每个电影列表的URL(一个页面20部电影)
        while True:
            data = get_html(url)  # 获取电影列表页面
            dicts = json.loads(data)  # 把数据转换成json格式
            if dicts != {"msg": "检测到有异常请求从您的IP发出，请登录再试!", "r": 1}:
                break
        try:
            movies_lists.append(dicts['data'])
            print("成功获取20部电影的网页: ", dicts['data'])
        except Exception as e:
            print("获取资源失败, 原因是 %s" % e)

    return movies_lists


def crawl_users(movies_lists):
    """
    @功能: 爬取用户信息
    @参数: 电影列表
    @返回: 用户列表
    """
    time.sleep(10)
    user_lists = []  # 储存所有用户的信息
    for i in range(len(movies_lists)):
        for j in movies_lists[i]:
            movie_url = j['url']  # 电影链接
            text = get_html(movie_url)  # 获取每部电影的页面
            html = etree.HTML(text)  # 解析每部电影的页面

            # 每部电影下面的5个用户评论
            for j in range(5):
                user_url = html.xpath("//div[{}]/div/h3/span[2]/a/@href".format(j + 1))[0]  # 电影页面下的用户主页URL
                rating_out_raw = html.xpath("//div[{}]/div/h3/span[2]/span[2]/@class".format(j + 1))[0]

                try:
                    user_id = user_url.split('/')[-2]  # 电影下的用户ID
                except:
                    user_id = None

                user_reviews_url = user_url + 'reviews'  # 用户主页的评论页面URL
                user_reviews_html = get_html(user_reviews_url)  # 获取用户主页评论页面
                user_reviews_data = etree.HTML(user_reviews_html)  # 解析用户主页评论页面

                # 进入用户主页评论页面进行爬取
                for k in range(10):
                    try:
                        movie_in_id_raw = user_reviews_data.xpath("//div[3]/div[3]/div/div[1]/div[1]/div[{}]/div/a/@href".format(k + 1))[0]
                        movie_in_id = re.search(r'\d+', movie_in_id_raw).group(0)  # 提取用户主页评论的第k部电影ID

                        rating_in_raw = user_reviews_data.xpath("//div[{}]/div/header/span[1]/@class".format(k + 1))[0]
                        rating_in = re.search(r'\d+', rating_in_raw).group(0)
                        rating_in = float(rating_in[0] + '.' + rating_in[1])  # 用户主页评论页面的评分

                        user_list = [user_id, movie_in_id, rating_in]
                        user_lists.append(user_list)  # 把用户主页内的电影存入
                        print("溜进去存了1条数据!")
                    except:
                        print("该用户无电影评论!")
                        break

                try:
                    movie_out_id = re.search(r'\d+', movie_url).group(0)  # 从电影页面提取的电影ID
                except:
                    movie_out_id = None
                try:
                    rating_out = re.search(r'\d+', rating_out_raw).group(0)
                    rating_out = float(rating_out[0] + '.' + rating_out[1])  # 从电影页面下提取的用户评分
                except:
                    rating_out = None

                user_list = [user_id, movie_out_id, rating_out]
                user_lists.append(user_list)

            print("成功爬取5位用户信息!")

    return user_lists


def save_to_csv(user_lists):
    """
    @功能: 把用户信息存入csv文件
    @参数: 用户列表
    @返回: 无
    """
    item = ['user_id', 'movie_id', 'rating']  # 列索引
    USERS = pd.DataFrame(data=user_lists, columns=item)  # 转换为DataFrame数据格式
    USERS.to_csv('douban_users.csv', mode='a', encoding='utf-8')  # 存入csv文件
    print("成功将用户数据存入!")


if __name__ == '__main__':
    num = 4  # 100*num个用户
    movies_lists = crawl_movies(num)
    user_lists = crawl_users(movies_lists)  # 获取用户信息
    save_to_csv(user_lists)  # 存入csv文件
