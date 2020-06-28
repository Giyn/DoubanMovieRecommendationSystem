# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:20:24 2020

@author: 许继元
"""

import pymysql
import csv


# 连接本地数据库
conn = pymysql.connect(host='localhost',
                       user='root',
                       passwd='xjyxjy0723',
                       charset='utf8')

cur = conn.cursor() # 创建一个可以执行SQL语句的游标对象
cur.execute("create database movie") # 创建数据库
cur.execute("use movie") # 使用数据库

# 创建表
sql_create = """
                create table douban_movies( 
                ID int NOT NULL,
                name varchar(50) DEFAULT NULL,
                english_name varchar(100) DEFAULT NULL,
                directors varchar(100) DEFAULT NULL,
                writer varchar(50) DEFAULT NULL,
                actors varchar(150) DEFAULT NULL,
                rate varchar(30) DEFAULT NULL,
                style1 varchar(30) DEFAULT NULL,
                style2 varchar(30) DEFAULT NULL,
                style3 varchar(30) DEFAULT NULL,
                country varchar(50) DEFAULT NULL,
                language varchar(50) DEFAULT NULL,
                date varchar(30) DEFAULT NULL,
                duration varchar(30) DEFAULT NULL,
                introduction varchar(5000) DEFAULT NULL,
                dataID varchar(30) DEFAULT NULL,
                url varchar(500) DEFAULT NULL,
                pic varchar(500) DEFAULT NULL
                )
             """

try:
    cur.execute(sql_create)
except Exception as e:
    print(e)
    conn.rollback()
    print('数据库创建操作错误回滚')


with open('doubanMovies.csv', 'r', encoding='utf-8') as f:
    read = csv.reader(f)
    for each in list(read)[1:]:
        i = tuple(each)
        sql = "INSERT INTO douban_movies VALUES" + str(i) # 使用SQL语句添加数据
        cur.execute(sql) # 执行SQL语句
    
    conn.commit() # 提交数据
    cur.close() # 关闭游标
    conn.close() # 关闭数据库