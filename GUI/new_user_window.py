# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:10:23 2020

@author: 许继元
"""

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

import recommendation
import search_window
from movie_detailed_search import MovieDetailedSearch
from user_center import UserCenter


class NewMainWindow(QWidget):
    def __init__(self, movies):
        super(NewMainWindow, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("豆瓣电影推荐系统")
        self.setWindowIcon(QIcon('../douban.jpg'))  # 设置窗口图标
        self.resize(1400, 800)
        self.user_df = pd.read_csv('../data/douban_users.csv')
        self.user_df = self.user_df.iloc[:, [1, 2, 3]]
        self.movies_df = pd.read_csv('../data/douban_movies.csv', encoding='utf-8')
        self.movies_df = self.movies_df.iloc[:, [0, 1, 6, 15, 16]]
        self.movies_df = self.movies_df.drop_duplicates(subset='url')
        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})
        self.user = ''
        self.user_movie_num = len(list(self.user_df[self.user_df['user_id'] == self.user].movie_id))
        self.user_movie_num_show = str(self.user_movie_num)

        self.USER_PWD = dict()
        self.USER_Label = dict()
        f = open('../data/users_info.csv', 'a+', encoding='utf-8')
        f.seek(0)  # 文件指针指向开头
        for line in f:
            self.USER_PWD[line.split(',')[0]] = line.split(',')[1].strip()  # 存入用户名密码
            try:
                self.USER_Label[line.split(',')[0]] = line.split(',')[2].strip()  # 存入用户标签
            except:
                self.USER_Label[line.split(',')[0]] = None
        f.close()

        self.welcome_label = QLabel(self)
        self.user_label = ''

        self.welcome_label.setText("<h1>欢迎您! " + self.user + "</h1>")
        self.recommend_label = QLabel("<h1>根据您的喜好为您推荐以下电影:</h1>", self)

        self.recommend_table = QTableWidget(self)
        self.hot_movies_label = QLabel("<h1>热门电影:</h1>", self)
        self.hot_movies_table = QTableWidget(self)

        self.user_center = QPushButton("个人主页", self)
        self.user_center.clicked.connect(lambda: self.show_user_center(self.user, self.user_movie_num_show, self.user_label))
        self.movie_detailed_button = QPushButton("电影详细页面", self)
        self.movie_detailed_button.clicked.connect(self.movie_detailed)
        self.search_button = QPushButton("电影搜索", self)
        self.search_button.clicked.connect(self.search)
        self.hot_rec_movies = recommendation.rec_hot_movies()  # 热门电影
        self.rec_movies = movies

        self.v1_layout = QVBoxLayout()
        self.v2_layout = QVBoxLayout()
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h_layout = QHBoxLayout()

        self.h1_layout.addWidget(self.welcome_label)
        self.h1_layout.addWidget(self.user_center)
        self.v1_layout.addLayout(self.h1_layout)
        self.v1_layout.addWidget(self.recommend_label)
        self.v1_layout.addWidget(self.recommend_table)

        self.h2_layout.addWidget(self.hot_movies_label)
        self.h2_layout.addWidget(self.movie_detailed_button)
        self.h2_layout.addWidget(self.search_button)
        self.v2_layout.addLayout(self.h2_layout)
        self.v2_layout.addWidget(self.hot_movies_table)

        self.h_layout.addLayout(self.v1_layout)
        self.h_layout.addLayout(self.v2_layout)

        self.setLayout(self.h_layout)

        self.rec_movies_table_init()
        self.hot_movies_table_init()
        self.set_hot_movie_table(self.hot_rec_movies)
        self.set_rec_movies_table(movies)

    def rec_movies_table_init(self):
        self.recommend_table.setColumnCount(6)
        self.recommend_table.setHorizontalHeaderLabels(['电影名称', '主演', '电影评分', '电影类型', '上映时间', '电影链接'])
        self.recommend_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.recommend_table.setRowCount(0)

    def hot_movies_table_init(self):
        self.hot_movies_table.setColumnCount(6)
        self.hot_movies_table.setHorizontalHeaderLabels(['电影名称', '主演', '评分', '电影类型', '上映时间', '电影链接'])
        self.hot_movies_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hot_movies_table.setRowCount(0)

    def set_rec_movies_table(self, movies):
        self.movies = movies
        row = self.recommend_table.rowCount()
        try:
            for i in range(len(self.movies)):
                self.recommend_table.insertRow(row)
                self.name = "《" + self.movies[i][0] + "》"
                if pd.isna(self.movies[i][1]):
                    self.actors = "无"
                else:
                    self.actors = self.movies[i][1]
                self.rating = str(self.movies[i][2])
                self.style = self.movies[i][3]
                self.date = str(int(self.movies[i][4]))
                self.url = self.movies[i][5]

                self.recommend_table.setItem(row, 0, QTableWidgetItem(self.name))
                self.recommend_table.setItem(row, 1, QTableWidgetItem(self.actors))
                self.recommend_table.setItem(row, 2, QTableWidgetItem(self.rating))
                self.recommend_table.setItem(row, 3, QTableWidgetItem(self.style))
                self.recommend_table.setItem(row, 4, QTableWidgetItem(self.date))
                self.recommend_table.setItem(row, 5, QTableWidgetItem(self.url))
        except:
            pass

    def set_hot_movie_table(self, hot_rec_movies):
        row = self.hot_movies_table.rowCount()

        for i in range(len(self.hot_rec_movies)):
            self.hot_movies_table.insertRow(row)
            self.hot_movies_name = "《" + self.hot_rec_movies[i][0] + "》"
            self.hot_movies_actors = self.hot_rec_movies[i][1]
            self.hot_movies_rating = str(self.hot_rec_movies[i][2])
            if pd.isna(self.hot_rec_movies[i][4]) and pd.isna(self.hot_rec_movies[i][5]):
                self.hot_movies_style = self.hot_rec_movies[i][3]
            elif pd.isna(self.hot_rec_movies[i][5]):
                self.hot_movies_style = self.hot_rec_movies[i][3] + ' ' + self.hot_rec_movies[i][4]
            else:
                self.hot_movies_style = self.hot_rec_movies[i][3] + ' ' + \
                                        self.hot_rec_movies[i][4] + ' ' + \
                                        self.hot_rec_movies[i][5]

            self.hot_movies_date = str(int(self.hot_rec_movies[i][6]))
            self.hot_movies_url = self.hot_rec_movies[i][7]

            self.hot_movies_table.setItem(row, 0, QTableWidgetItem(self.hot_movies_name))
            self.hot_movies_table.setItem(row, 1, QTableWidgetItem(self.hot_movies_actors))
            self.hot_movies_table.setItem(row, 2, QTableWidgetItem(self.hot_movies_rating))
            self.hot_movies_table.setItem(row, 3, QTableWidgetItem(self.hot_movies_style))
            self.hot_movies_table.setItem(row, 4, QTableWidgetItem(self.hot_movies_date))
            self.hot_movies_table.setItem(row, 5, QTableWidgetItem(self.hot_movies_url))

    def movie_detailed(self):
        self.movie_detailed_fun = MovieDetailedSearch()
        self.movie_detailed_fun.show()

    # 搜索功能
    def search(self):
        self.search_func = search_window.SearchWindow()
        self.search_func.show()

    def show_user_center(self, user, num, label):
        self.show_user = UserCenter(user, num, label)
        self.show_user.show()
