# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:55:59 2020

@author: 许继元
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class UserCenter(QWidget):
    def __init__(self, user, num, label):
        super(UserCenter, self).__init__()  # 使用super函数可以实现子类使用父类的方法
        self.setWindowTitle("个人主页")
        self.setWindowIcon(QIcon('../Data/douban.jpg'))  # 设置窗口图标
        self.resize(500, 150)

        self.user_label = QLabel(self)
        self.num_label = QLabel(self)
        self.label_label = QLabel(self)

        self.user_label.setText("<h1>您好!" + user + "</h1>")
        self.num_label.setText("<h2>您在豆瓣评论过" + num + "部电影</h2>")
        try:
            self.label_label.setText("<h2>您喜欢的电影类型是:" + label + "</h2>")
        except:
            self.label_label.setText("")

        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.user_label)
        self.v_layout.addWidget(self.num_label)
        self.v_layout.addWidget(self.label_label)

        self.setLayout(self.v_layout)
