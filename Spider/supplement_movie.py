# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:10:23 2020

@author: 许继元
"""

import random
import re
import time

import pandas as pd
import requests
from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()


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


def crawl_user_movies():
    """
    @功能: 补充用户观看过的电影信息
    @参数: 无
    @返回: 电影信息
    """
    user_df = pd.read_csv('douban_users.csv')
    user_df = user_df.iloc[:, [1, 2, 3]]
    user_movies = list(user_df['movie_id'].unique())
    movies = []  # 储存电影
    count = 1  # 日志参数

    for i in user_movies:
        url = 'https://movie.douban.com/subject/{}/'.format(str(i))
        text = get_html(url)  # 获取每部电影的页面
        if text == None:
            count += 1  # 日志参数
            continue
        html = etree.HTML(text)  # 解析每部电影的页面

        info = html.xpath("//div[@class='subject clearfix']/div[@id='info']//text()")  # 每部电影的相关信息

        # 电影ID
        dataID = i

        # 电影名称
        name = html.xpath("//*[@id='content']/h1/span[1]/text()")[0]
        name = name.split(' ')[0]

        # 电影英文名称
        english_name = html.xpath("//*[@id='content']/h1/span[1]/text()")[0]
        # 判断字符串中是否存在英文
        if bool(re.search('[A-Za-z]', english_name)):
            english_name = english_name.split(' ')  # 分割字符串以提取英文名称
            del english_name[0]  # 去除中文名称
            english_name = ' '.join(english_name)  # 重新以空格连接列表中的字符串
        else:
            english_name = None

        # 导演
        flag = 1
        directors = []
        for i in range(len(info)):
            if info[i] == '导演':
                for j in range(i + 1, len(info)):
                    if info[j] == '编剧':
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文或英文
                        if (u'\u4e00' <= ch <= u'\u9fff') or (bool(re.search('[a-z]', info[j]))):
                            directors.append(info[j].strip())
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        directors = ''.join(directors)  # 转换为字符串形式

        # 编剧
        flag = 1
        writer = []
        for i in range(len(info)):
            if info[i] == '编剧':
                for j in range(i + 1, len(info)):
                    if info[j] == '主演':
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文或英文
                        if (u'\u4e00' <= ch <= u'\u9fff') or (bool(re.search('[a-z]', info[j]))):
                            writer.append(info[j].strip())
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        writer = ''.join(writer)  # 转换为字符串形式

        # 主演
        flag = 1
        actors = []
        for i in range(len(info)):
            if info[i] == '编剧':
                for j in range(i + 1, len(info)):
                    if info[j] == '主演':
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文或英文
                        if (u'\u4e00' <= ch <= u'\u9fff') or (bool(re.search('[a-z]', info[j]))):
                            actors.append(info[j].strip())
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        actors = ''.join(actors)  # 转换为字符串形式

        # 电影评分
        try:
            rate = html.xpath("//div[@class='rating_wrap clearbox']/div[@class='rating_self clearfix']/strong[@class='ll rating_num']/text()")[0]
        except:
            rate = None

        # 电影类型
        flag = 1
        style = []
        for i in range(len(info)):
            if info[i] == '类型:':
                for j in range(i + 1, len(info)):
                    if (info[j] == '制片国家/地区:') or (info[j] == '官方网站:'):
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文
                        if u'\u4e00' <= ch <= u'\u9fff':
                            style.append(info[j])
                            if len(style) == 3:
                                flag = 0
                                break
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break

        # 把电影类型分开存储
        if len(style) == 0:
            style1 = None
            style2 = None
            style3 = None
        if len(style) == 1:
            style1 = style[0]
            style2 = None
            style3 = None
        if len(style) == 2:
            style1 = style[0]
            style2 = style[1]
            style3 = None
        if len(style) == 3:
            style1 = style[0]
            style2 = style[1]
            style3 = style[2]

        # 国家
        flag = 1
        country = []
        for i in range(len(info)):
            if info[i] == r'制片国家/地区:':
                for j in range(i + 1, len(info)):
                    if info[j] == '语言:':
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文
                        if u'\u4e00' <= ch <= u'\u9fff':
                            country.append(info[j].strip())
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        country = country[0].split(r'/')
        country = country[0]

        # 电影语言
        flag = 1
        language = []
        for i in range(len(info)):
            if info[i] == '语言:':
                for j in range(i + 1, len(info)):
                    if info[j] == '上映日期:':
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文
                        if u'\u4e00' <= ch <= u'\u9fff':
                            language.append(info[j].strip())
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        try:
            language = language[0].split(r'/')
            language = language[0]
        except:
            language = None

        # 电影上映日期
        flag = 1
        date = []
        for i in range(len(info)):
            if info[i] == '上映日期:':
                for j in range(i + 1, len(info)):
                    if (info[j] == '片长:') or (info[j] == '又名:'):
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文或英文
                        if (u'\u4e00' <= ch <= u'\u9fff') or (bool(re.search('[a-z]', info[j]))):
                            date.append(re.search(r'\d+', info[j]).group(0))
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        date = ''.join(date)  # 转换为字符串形式

        # 电影片长
        flag = 1
        duration = []
        for i in range(len(info)):
            if info[i] == '片长:':
                for j in range(i + 1, len(info)):
                    if (info[j] == '又名:') or (info[j] == 'IMDb链接:'):
                        flag = 0
                        break
                    for ch in info[j]:
                        # 判断字符串中是否存在中文
                        if u'\u4e00' <= ch <= u'\u9fff':
                            info[j] = info[j].split('/')[0]
                            duration.append(re.search(r'\d+', info[j].strip()).group(0))
                            flag = 0
                            break
                    if flag == 0:
                        break
            if flag == 0:
                break
        duration = ''.join(duration)  # 转换为字符串形式

        # 海报图片
        pic = html.xpath("//div[@id='mainpic']/a[@class='nbgnbg']/img/@src")[0]

        # 电影简介
        introduction = ''.join(html.xpath("//div[@class='related-info']/div[@id='link-report']/span/text()")).strip().replace(' ', '').replace('\n', '').replace('\xa0', '').replace(u'\u3000', u' ')

        # 把每部电影的信息存入一个列表，再append进去movies总列表
        each_movie = [name, english_name, directors, writer, actors, rate, style1, style2, style3,
                      country, language, date, duration, introduction, dataID, url, pic]
        movies.append(each_movie)

        print("成功解析第" + str(count) + "部电影的信息: ", each_movie)
        count += 1  # 日志参数

    return movies


def save_to_csv(movies):
    """
    @功能: 把电影信息存入csv文件
    @参数: 电影列表
    @返回: 无
    """
    item = ['name', 'english_name', 'directors', 'writer', 'actors', 'rate', 'style1', 'style2',
            'style3', 'country', 'language', 'date', 'duration', 'introduction', 'dataID', 'url',
            'pic']  # 列索引
    MOVIES = pd.DataFrame(data=movies, columns=item)  # 转换为DataFrame数据格式
    MOVIES.to_csv('doubanMovies.csv', mode='a', encoding='utf-8')  # 存入csv文件


if __name__ == '__main__':
    movies = crawl_user_movies()  # 获取电影信息
    save_to_csv(movies)  # 存入csv文件
