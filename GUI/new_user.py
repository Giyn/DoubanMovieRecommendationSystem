# -*- coding: utf-8 -*-
"""
Created on Mon May 18 06:41:27 2020

@author: 许继元
"""

import re
import sys

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTextEdit

from new_user_window import NewMainWindow


class NewUser(QWidget):
    def __init__(self, user):
        super(NewUser, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("豆瓣电影推荐系统")
        self.setWindowIcon(QIcon('../Data/douban.jpg'))  # 设置窗口图标
        self.resize(400, 400)

        self.movies_df = pd.read_csv('../Data/douban_movies.csv', encoding='utf-8')
        self.movies_df = self.movies_df.iloc[:, [0, 1, 5, 6, 7, 8, 9, 12, 15, 16]]

        self.movies_df = self.movies_df.drop_duplicates(subset='url')
        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})

        self.movies_df['style1'] = self.movies_df['style1'].fillna('0')  # 缺失值填充

        self.new_user_label1 = QLabel("<h2>由于您是新用户</h2>")
        self.new_user_label2 = QLabel("<h2>我们在此诚挚地询问您喜欢的电影类型,以便我们更好地向您推荐电影:</h2>")
        self.new_user_label3 = QLabel("<h3>例如: 剧情、动作、喜剧、科幻、悬疑、爱情、恐怖等</h3>")
        self.new_user_like = QTextEdit(self)
        self.new_user_button = QPushButton("提交", self)
        try:
            self.new_user_button.clicked.connect(lambda: self.submit_like(re.search("[\u4e00-\u9fa5]{2}", self.new_user_like.toPlainText()).group(0)))
        except:
            pass

        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.new_user_label1)
        self.v_layout.addWidget(self.new_user_label2)
        self.v_layout.addWidget(self.new_user_label3)
        self.v_layout.addWidget(self.new_user_like)
        self.v_layout.addWidget(self.new_user_button)

        self.setLayout(self.v_layout)

    def submit_like(self, style):
        self.new_user_like = self.movies_df[self.movies_df['style1'].str.contains('{}'.format(style))]
        self.new_user_rec = self.new_user_like[self.new_user_like.rate >= 6.5]

        self.new_user_rec = self.new_user_rec.iloc[:, [1, 2, 3, 4, 7, 9]]
        self.temp2 = []
        for i in list(self.new_user_rec):
            self.temp1 = []
            for j in range(len(list(self.new_user_rec.name.unique()))):
                self.temp1.append(self.new_user_rec['{}'.format(i)].values.tolist()[j])
            self.temp2.append(self.temp1)

        self.new_user_rec_movies = []  # 存储新用户推荐电影
        for k in range(len(self.temp2[0])):
            self.temp3 = []
            for l in range(len(self.temp2)):
                self.temp3.append(self.temp2[l][k])
            self.new_user_rec_movies.append(self.temp3)

        self.new_user_rec_movies = self.new_user_rec_movies[:15]

        self.new = NewMainWindow(self.new_user_rec_movies)
        self.new.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    new = NewUser("a")
    new.show()
    sys.exit(app.exec_())
