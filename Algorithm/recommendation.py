# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:53:55 2020

@author: 许继元
"""

import random

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity  # 计算余弦相似度

# 用户信息
user_df = pd.read_csv('../Data/douban_users.csv')
user_df = user_df.iloc[:, [1, 2, 3]]

# 电影信息
movies_df = pd.read_csv('../Data/douban_movies.csv', encoding='utf-8')
movies_df = movies_df.iloc[:, [0, 1, 5, 6, 7, 8, 9, 12, 15, 16]]
movies_df = movies_df.drop_duplicates(subset='url')
movies_df = movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})

# 用户ID映射
usersMap = dict(enumerate(list(user_df['user_id'].unique())))  # 电影id与其对应索引的映射关系
usersMap = dict(zip(usersMap.values(), usersMap.keys()))  # 键值互换

# 电影ID映射
moviesMap_raw = dict(enumerate(list(movies_df['dataID'])))  # 电影id与其对应索引的映射关系
moviesMap = dict(zip(moviesMap_raw.values(), moviesMap_raw.keys()))  # 键值互换

n_users = user_df.user_id.unique().shape[0]  # 用户总数
n_movies = movies_df.Movie_ID.unique().shape[0]  # 电影总数

data_matrix = np.zeros((n_users, n_movies))  # 用户-物品矩阵雏形

# 构造用户-物品矩阵
for line in user_df.itertuples():
    try:
        data_matrix[usersMap[str(line[1])], moviesMap[line[2]]] = line[3]
    except:
        pass

# 电影余弦相似度矩阵
item_similarity = cosine_similarity(data_matrix.T)  # 转置之后计算的才是电影的相似度


def rec_hot_movies():
    """
    @功能: 获取热门推荐电影
    @参数: 无
    @返回: 热门推荐电影列表
    """
    hot_movies = []
    hot_movies_raw = movies_df[movies_df.date >= 2019]
    hot_movies_raw = hot_movies_raw[hot_movies_raw.rate >= 8.7]
    hot_movies_raw = hot_movies_raw.iloc[:, [1, 2, 3, 4, 5, 6, 7, 9]]

    for i in list(hot_movies_raw):
        temp = []
        for j in range(len(list(hot_movies_raw.name.unique()))):
            temp.append(hot_movies_raw['{}'.format(i)].values.tolist()[j])
        hot_movies.append(temp)

    hot_rec_movies = []  # 存储热门推荐电影
    for k in range(len(hot_movies[0])):
        temp_rec_movies = []
        for l in range(len(hot_movies)):
            temp_rec_movies.append(hot_movies[l][k])
        hot_rec_movies.append(temp_rec_movies)

    return hot_rec_movies


def Recommend(movie_id, k):  # movie_id:电影名关键词，k:为最相似的k部电影
    """
    @功能: 获得推荐电影列表
    @参数: 电影ID、每部电影选取最相似的数目
    @返回: 推荐电影列表
    """
    movie_list = []  # 存储结果
    try:
        # 过滤电影数据集，搜索找到对应的电影的id
        movieid = list(movies_df[movies_df['dataID'] == movie_id].Movie_ID)[0]
        # 获取该电影的余弦相似度数组
        movie_similarity = item_similarity[movieid]
        # 返回前k个最高相似度的索引位置
        movie_similarity_index = np.argsort(-movie_similarity)[
                                 1:k + 1]  # argsort函数是将数组元素从小到大排列，返回对应的索引数组

        for i in movie_similarity_index:
            rec_movies = []  # 每部推荐的电影
            rec_movies.append(list(movies_df[movies_df.Movie_ID == i].name)[0])  # 电影名
            rec_movies.append(list(movies_df[movies_df.Movie_ID == i].actors)[0])  # 主演

            if pd.isna(list(movies_df[movies_df.Movie_ID == i].style2)[0]) and pd.isna(list(movies_df[movies_df.Movie_ID == i].style3)[0]):
                style = list(movies_df[movies_df.Movie_ID == i].style1)[0]
            elif pd.isna(list(movies_df[movies_df.Movie_ID == i].style3)[0]):
                style = list(movies_df[movies_df.Movie_ID == i].style1)[0] + ' ' + \
                        list(movies_df[movies_df.Movie_ID == i].style2)[0]
            else:
                style = list(movies_df[movies_df.Movie_ID == i].style1)[0] + ' ' + \
                        list(movies_df[movies_df.Movie_ID == i].style2)[0] + ' ' + \
                        list(movies_df[movies_df.Movie_ID == i].style3)[0]
            rec_movies.append(style)  # 电影类型
            rec_movies.append(list(movies_df[movies_df.Movie_ID == i].rate)[0])  # 电影评分
            rec_movies.append(list(movies_df[movies_df.Movie_ID == i].url)[0])  # 电影链接

            movie_list.append(rec_movies)  # 列表中的元素为列表，存储相关信息
    except:
        pass

    return movie_list


def find_user_like(user_id):
    user_seen_movies = user_df[user_df['user_id'] == '{}'.format(user_id)].movie_id  # 用户看过的电影的ID
    userlike_movies = []  # 储存用户比较喜欢的电影ID
    for i in list(user_seen_movies):
        if list(user_df[user_df['movie_id'] == i].rating)[0] >= 4:
            userlike_movies.append(
                list(user_df[user_df['movie_id'] == i].movie_id)[0])  # 找出用户比较喜欢的电影的ID

    user_like_movies = []  # 储存用户喜欢的随机5部
    try:
        for i in range(5):
            user_like_movies.append(random.choice(userlike_movies))

        rec = []
        for each in user_like_movies:
            rec.extend(Recommend(each, 7))
    except:
        return None

    return rec
