# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:33:56 2020

@author: 许继元
"""

import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QTextBrowser, QTableWidgetItem, \
                            QVBoxLayout, QHBoxLayout, QLineEdit, QTableWidget, QHeaderView
from PyQt5.QtGui import QIcon
from movie_detailed import MovieDetailed

class MovieDetailedSearch(QWidget):
    def __init__(self):
        super(MovieDetailedSearch, self).__init__() # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("电影详细信息")
        self.setWindowIcon(QIcon('../douban.jpg')) # 设置窗口图标
        self.resize(500,150)

        self.search_label = QLabel("请输入完整的电影名称: ", self)
        self.search_line = QLineEdit(self)
        self.search_button = QPushButton("搜索", self)
        
        self.h_layout = QHBoxLayout()
        
        self.h_layout.addWidget(self.search_label)
        self.h_layout.addWidget(self.search_line)
        self.h_layout.addWidget(self.search_button)
        
        self.setLayout(self.h_layout)
        
        self.search_button.clicked.connect(lambda: self.search(self.search_line.text()))
        

    def search(self, name):
        self.detailed = MovieDetailed(name)
        self.detailed.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    search = MovieDetailedSearch()
    search.show()
    sys.exit(app.exec_())