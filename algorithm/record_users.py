# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:57:57 2020

@author: 许继元
"""

import pandas as pd

# 用户信息
user_df = pd.read_csv('douban_users.csv')
user_df = user_df.iloc[:, [1, 2, 3]]

# 电影信息
movies_df = pd.read_csv('douban_movies.csv', encoding='utf-8')
movies_df = movies_df.iloc[:, [0, 1, 6, 7, 8, 9, 15, 16]]
movies_df = movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})

all_users_id = list(user_df['user_id'].unique())  # 所有用户的ID


def find_user_label(user_id):
    """
    @功能: 找到用户的标签（喜欢的电影类型）
    @参数: 用户的ID
    @返回: 用户的标签（list）
    """
    user_seen_movies = user_df[user_df['user_id'] == '{}'.format(user_id)].movie_id  # 用户看过的电影的ID

    userlike_movies = []  # 储存用户比较喜欢的电影ID
    for i in list(user_seen_movies):
        if list(user_df[user_df['movie_id'] == i].rating)[0] >= 4:
            userlike_movies.append(list(user_df[user_df['movie_id'] == i].movie_id)[0])  # 找出用户比较喜欢的电影的ID

    user_label = []  # 储存用户标签
    for j in userlike_movies:
        try:
            user_label.append(list(movies_df[movies_df['dataID'] == j].style1)[0])
            user_label.append(list(movies_df[movies_df['dataID'] == j].style2)[0])
            user_label.append(list(movies_df[movies_df['dataID'] == j].style3)[0])
        except:
            pass

    # 去除nan
    for k in user_label:
        if pd.isna(k):
            user_label.remove(k)

    user_label = list(set(user_label))  # 去重

    # 去除nan
    for k in user_label:
        if pd.isna(k):
            user_label.remove(k)

    return user_label


def save_to_csv(all_users_id):
    """
    @功能: 把用户信息存入csv文件
    @参数: 用户ID
    @返回: 无
    """
    all_users = []
    for i in all_users_id:
        user_labels = ' '.join(find_user_label(str(i)))
        temp = [i, '123456', user_labels]
        all_users.append(temp)

    item = ['ID', 'PassWord', 'Label']  # 列索引
    USERS = pd.DataFrame(data=all_users, columns=item)  # 转换为DataFrame数据格式
    USERS.to_csv('users_info.csv', mode='a', encoding='utf-8')  # 存入csv文件
    print("成功存入csv文件!")


if __name__ == '__main__':
    save_to_csv(all_users_id)
