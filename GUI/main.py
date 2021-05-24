# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:51:13 2020

@author: 许继元
"""

import sys

from PyQt5.QtWidgets import QApplication

from login import Login

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Login = Login()
    Login.show()
    sys.exit(app.exec_())
