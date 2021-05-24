# -*- coding: utf-8 -*-
"""
Created on Thu May 14 01:30:22 2020

@author: 许继元
"""

import sys

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class SearchWindow(QWidget):
    def __init__(self):
        super(SearchWindow, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影搜索")
        self.setWindowIcon(QIcon('../Data/douban.jpg'))  # 设置窗口图标
        self.resize(600, 800)
        # 电影信息
        self.movies_df = pd.read_csv('../Data/douban_movies.csv', encoding='utf-8')
        self.movies_df = self.movies_df.iloc[:, [0, 1, 6, 15, 16]]
        self.movies_df = self.movies_df.drop_duplicates(subset='url')
        self.movies_df = self.movies_df.rename(columns={'Unnamed: 0': 'Movie_ID'})

        self.search_label = QLabel("<h3>请输入电影名称:</h3>", self)
        self.search_edit = QLineEdit(self)
        self.search_button = QPushButton("搜索", self)
        self.search_button.clicked.connect(lambda: self.Fuzzy_search(self.search_edit.text()))
        self.search_browser = QTextBrowser(self)

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.h_layout.addWidget(self.search_label)
        self.h_layout.addWidget(self.search_edit)
        self.h_layout.addWidget(self.search_button)

        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.search_browser)

        self.setLayout(self.v_layout)

    # 模糊搜索功能
    def Fuzzy_search(self, keyword):
        self.search_browser.clear()
        flag = 1
        if keyword == '':
            flag = 0
            self.search_browser.clear()
            self.search_browser.setText("<h2>输入不能为空!</h2>")
        else:
            self.search_browser.clear()
            if list(self.movies_df[self.movies_df['name'].str.contains('{}'.format(keyword))].name) == []:
                self.search_browser.append("<h2>很抱歉,没有找到相关电影!</h2>")
            self.movie_list = list(self.movies_df[self.movies_df['name'].str.contains('{}'.format(keyword))].name[:15])
            self.rating_list = list(self.movies_df[self.movies_df['name'].str.contains('{}'.format(keyword))].rate[:15])
            self.url_list = list(self.movies_df[self.movies_df['name'].str.contains('{}'.format(keyword))].url[:15])

        try:
            for i in range(15):
                if flag == 0:
                    break
                self.name = self.movie_list[i]
                self.rating = str(self.rating_list[i])
                self.url = self.url_list[i]
                self.content = "<h3>" + "《" + self.name + "》" + "  评分:" + self.rating + "</h3>" + '\n' + "<h3>" + "  链接:" + self.url + "</h3>"
                self.search_browser.append(self.content)
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    search = SearchWindow()
    search.show()
    sys.exit(app.exec_())
