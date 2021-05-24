# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:53:55 2020

@author: 许继元
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from new_user import NewUser


# 注册窗口
class SigninPage(QDialog):
    def __init__(self):
        super().__init__()
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
        self.setWindowTitle('注册')  # 设置窗口标题
        self.setWindowIcon(QIcon('../data/douban.jpg'))  # 设置窗口图标
        self.signin_user_label = QLabel('用户名:', self)  # 文本设置
        self.signin_pwd_label = QLabel('密码:', self)
        self.signin_pwd2_label = QLabel('密码:', self)
        self.signin_user_line = QLineEdit(self)  # 单行文本编辑器
        self.signin_pwd_line = QLineEdit(self)
        self.signin_pwd2_line = QLineEdit(self)
        self.signin_button = QPushButton('注册', self)  # 命令按钮

        self.user_h_layout = QHBoxLayout()  # 水平排列小部件
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()  # 垂直排列小部件

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    def layout_init(self):
        self.user_h_layout.addWidget(self.signin_user_label)
        self.user_h_layout.addWidget(self.signin_user_line)
        self.pwd_h_layout.addWidget(self.signin_pwd_label)
        self.pwd_h_layout.addWidget(self.signin_pwd_line)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)

    def lineedit_init(self):
        # 显示密码掩码字符
        self.signin_pwd_line.setEchoMode(QLineEdit.Password)
        self.signin_pwd2_line.setEchoMode(QLineEdit.Password)

        # 文本更改时发出信号
        self.signin_user_line.textChanged.connect(self.check_input_func)
        self.signin_pwd_line.textChanged.connect(self.check_input_func)
        self.signin_pwd2_line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.check_signin_func)

    def check_input_func(self):
        if self.signin_user_line.text() and self.signin_pwd_line.text() and self.signin_pwd2_line.text():
            self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)

    def check_signin_func(self):
        if self.signin_pwd_line.text() != self.signin_pwd2_line.text():
            QMessageBox.critical(self, '通知', '两次密码不一致!')
        elif self.signin_user_line.text() not in self.USER_PWD:
            QMessageBox.information(self, '通知', '成功注册!')
            f = open('../data/users_info.csv', 'a+', encoding='utf-8')
            info = self.signin_user_line.text() + ',' + self.signin_pwd_line.text() + '\n'
            f.write(info)
            f.close()
            self.USER_PWD[self.signin_user_line.text()] = self.signin_pwd_line.text()
            self.close()
            self.new = NewUser(self.signin_user_line.text())
            self.new.show()
        else:
            QMessageBox.critical(self, '通知', '该用户名已被注册!')

        self.signin_user_line.clear()
        self.signin_pwd_line.clear()
        self.signin_pwd2_line.clear()
