# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:26:03 2020

@author: 许继元
"""

import sys

import pandas as pd
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class MovieDetailed(QWidget):
    def __init__(self, name):
        super(MovieDetailed, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影详细信息")
        self.setWindowIcon(QIcon('../Data/douban.jpg'))  # 设置窗口图标
        self.resize(1400, 800)
        self.name = name
        # 电影信息
        self.movies_detailed = pd.read_csv('../Data/douban_movies.csv', encoding='utf-8')
        self.movies_detailed = self.movies_detailed.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]

        self.pix = QPixmap(r'../MoviePosters/' + "{}".format(self.name) + '.jpg')
        self.pic = QLabel(self)
        self.pic.setPixmap(self.pix)

        try:
            if pd.isna(list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].english_name)[0]):
                self.english_name = ''
            else:
                self.english_name = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].english_name)[0]
            self.directors = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].directors)[0]
            self.writer = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].writer)[0]
            self.actors = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].actors)[0]
            self.rate = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].rate)[0]
            if pd.isna(list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style2)[0]) and pd.isna(list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style3)[0]):
                self.style = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style1)[0]
            elif pd.isna(list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style3)[0]):
                self.style = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style1)[0] + ' ' + \
                             list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style2)[0]
            else:
                self.style = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style1)[0] + ' ' + \
                             list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style2)[0] + ' ' + \
                             list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].style3)[0]
            self.country = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].country)[0]
            self.language = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].language)[0]
            self.date = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].date)[0]
            self.duration = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].duration)[0]
            self.introduction = list(self.movies_detailed[self.movies_detailed.name == "{}".format(self.name)].introduction)[0]

            self.name_label = QLabel("<font size=10><b>" + self.name + " " + self.english_name + "</b></font>")
            self.directors_label = QLabel("<h2>" + "导演: " + self.directors + "</h2>")
            self.writer_label = QLabel("<h2>" + "编剧: " + self.writer + "</h2>")
            self.actors_label = QLabel("<h2>" + "主演: " + self.actors.split(' ')[0] + "</h2>")
            self.style_label = QLabel("<h2>" + "类型: " + self.style + "</h2>")

            self.country_label = QLabel("<h2>" + "国家: " + self.country + "</h2>")
            self.language_label = QLabel("<h2>" + "语言: " + self.language + "</h2>")
            self.date_label = QLabel("<h2>" + "上映时间: " + str(int(self.date)) + "</h2>")
            self.duration_label = QLabel("<h2>" + "片长: " + str(int(self.duration)) + "</h2>")

            self.rate_label = QLabel("<h1>" + "评分: " + str(self.rate) + "</h1>")
            self.introduction_label = QLabel("<h1><b>电影简介:</b></h1>", self)
            self.introduction_browser = QTextBrowser(self)
            self.introduction_browser.setText("<h2>" + self.introduction + "</h2>")

            self.v1_layout = QVBoxLayout()
            self.v2_layout = QVBoxLayout()
            self.h_layout = QHBoxLayout()
            self.v_layout = QVBoxLayout()

            self.v1_layout.addWidget(self.directors_label)
            self.v1_layout.addWidget(self.writer_label)
            self.v1_layout.addWidget(self.actors_label)
            self.v1_layout.addWidget(self.style_label)

            self.v2_layout.addWidget(self.country_label)
            self.v2_layout.addWidget(self.language_label)
            self.v2_layout.addWidget(self.date_label)
            self.v2_layout.addWidget(self.duration_label)

            self.h_layout.addWidget(self.pic)
            self.h_layout.addLayout(self.v1_layout)
            self.h_layout.addLayout(self.v2_layout)
            self.h_layout.addWidget(self.rate_label)

            self.v_layout.addWidget(self.name_label)
            self.v_layout.addLayout(self.h_layout)
            self.v_layout.addWidget(self.introduction_label)
            self.v_layout.addWidget(self.introduction_browser)

            self.setLayout(self.v_layout)
        except:
            self.resize(200, 200)
            self.no_find = QLabel("<h1>对不起, 没有找到相关电影!</h1>", self)
            self.h_layout = QHBoxLayout()
            self.h_layout.addWidget(self.no_find)
            self.setLayout(self.h_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    detailed = MovieDetailed("复仇者联盟")
    detailed.show()
    sys.exit(app.exec_())
