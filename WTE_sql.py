# /usr/bin/python3
# coding:utf-8
from __future__ import unicode_literals

'''
author:QYK
mail:ethan.71@163.com
content:a py for creating TWE's database
'''

import pymysql

db = pymysql.connect("localhost", "root", "123456", charset="utf8")
cur = db.cursor()
try:
    cur.execute("create database TWE;")
    cur.execute("use TWE")
    cur.execute("create table user (id int auto_increment primary key,\
            name varchar(32) not null,pwd varchar(20) default '123456',\
            uid varchar(5),win int,lose int);")
    cur.execute("create table breakfast (id int auto_increment primary key,\
            user_id int,f_name varchar(64));")
    cur.execute("create table lunch (id int auto_increment primary key,\
            user_id int,f_name varchar(64));")
    cur.execute("create table dinner (id int auto_increment primary key,\
            user_id int,f_name varchar(64));")
    cur.execute("create table drinks (id int auto_increment primary key,\
            user_id int,f_name varchar(64));")
    db.commit()
except:
    db.rollback()
cur.close()
db.close()
