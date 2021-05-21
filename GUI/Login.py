# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:51:13 2020

@author: 许继元
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from MainWindow import MainWindow
from Sign import SigninPage


# 登录窗口
class Login(QWidget):
    def __init__(self):
        super().__init__()  # 调用基类方法
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
        self.resize(400, 200)  # 窗口尺寸
        self.setWindowTitle('豆瓣电影推荐系统')  # 设置窗口标题
        self.setWindowIcon(QIcon('../douban.jpg'))  # 设置窗口图标
        self.user_label = QLabel('用户名:', self)  # 文本设置
        self.pwd_label = QLabel('密码:', self)
        self.user_line = QLineEdit(self)  # 单行文本编辑器
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('登录', self)  # 命令按钮
        self.signin_button = QPushButton('注册', self)

        self.grid_layout = QGridLayout()  # 将小部件布置在网格中
        self.h_layout = QHBoxLayout()  # 水平排列小部件
        self.v_layout = QVBoxLayout()  # 垂直排列小部件

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()
        self.signin_page = SigninPage()  # 提供登录标准功能的基类

    def layout_init(self):
        self.grid_layout.addWidget(self.user_label, 0, 0, 2, 1)  # 布局控件
        self.grid_layout.addWidget(self.user_line, 0, 1, 2, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0, 2, 1)
        self.grid_layout.addWidget(self.pwd_line, 1, 1, 2, 1)
        self.h_layout.addWidget(self.login_button)  # 添加登录按钮
        self.h_layout.addWidget(self.signin_button)  # 添加注册按钮
        self.v_layout.addLayout(self.grid_layout)  # 将布局添加到框的末尾
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def lineedit_init(self):
        self.user_line.setPlaceholderText('输入用户名')  # 在输入框显示浅灰色的提示文本
        self.pwd_line.setPlaceholderText('输入密码')
        self.pwd_line.setEchoMode(QLineEdit.Password)  # 显示密码掩码字符

        # 文本更改时发出信号
        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.check_login_func)  # 输入文本后即可点击
        self.signin_button.clicked.connect(self.show_signin_page_func)  # 显示注册页面

    def check_login_func(self):
        if self.USER_PWD.get(self.user_line.text()) == self.pwd_line.text():
            QMessageBox.information(self, '通知', '成功登录!')
            self.close()
            self.MainWindow = MainWindow(self.user_line.text())
            self.MainWindow.show()
        else:
            QMessageBox.critical(self, '通知', '用户名或密码错误!')
        self.pwd_line.clear()

    def show_signin_page_func(self):
        self.signin_page.exec_()
        f = open('../data/users_info.csv', 'a+', encoding='utf-8')
        f.seek(0)  # 文件指针指向开头
        for line in f:
            self.USER_PWD[line.split(',')[0]] = line.split(',')[1].strip()  # 存入用户名密码
        f.close()

    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)  # 可点击
        else:
            self.login_button.setEnabled(False)  # 不可点击
