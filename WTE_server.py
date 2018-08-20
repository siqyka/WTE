#/usr/bin/python3
# coding:utf-8
from __future__ import unicode_literals


'''
author:QYK
mail:ethan.71@163.com
content:TWE's server
'''

import socket
import threading
import pymysql
import random


class TWE_server(object):

    def __init__(self):
        self.ADDR = ("0.0.0.0", 7771)
        self.name = ""
        self.pwd = ""

    # 连接套接字
    def client_socket(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.ADDR)
        self.sock.listen(10)

    # 连接数据库
    def conn_sql(self):
        self.db = pymysql.connect(
            "localhost", "root", "123456", charset="utf8")
        self.cur = self.db.cursor()
        self.cur.execute("use TWE;")

    # 创建线程
    def serve_forever(self):
        self.client_socket()
        self.conn_sql()
        print("Listen...")
        while True:
            conn, addr = self.sock.accept()
            self.clientThread = threading.Thread(
                target=self.handle_thing, args=(conn,))
            self.clientThread.setDaemon(True)
            self.clientThread.start()

    # 线程事件
    def handle_thing(self, conn):
        self.conn = conn
        while True:
            data = conn.recv(2048).decode()
            data = data.split("#")
            if data[0] == "RG":
                self.register(data)
            elif data[0] == "LG":
                self.login(data)
            elif data[0] == "QE":
                self.query(data)
            elif data[0] == "AT":
                self.alter(data)
            elif data[0] == "Q":
                print(self.name, "退出！")

    # 注册
    def register(self, data):
        # data-->[flag,name,pwd]
        print(data)
        self.name = data[1]
        self.pwd = data[2]
        self.cur.execute(
            "select count(*) from user where name ='%s';" % self.name)
        count = self.cur.fetchall()
        if count[0][0] == 0:
            self.conn.send(b"OK")
            try:
                self.cur.execute(
                    "insert into user values(null,'%s','%s');"
                    % (self.name, self.pwd))
                self.db.commit()
            except:
                self.db.rollback()
                self.conn.secd(b"UserInsertError")
        else:
            self.conn.send(b"UserAlreadyExists")

    # 登录
    def login(self, data):
        # data-->[flag,name,pwd]
        self.name = data[1]
        self.pwd = data[2]
        self.cur.execute(
            "select name,pwd from user where name ='%s';" % self.name)
        count = self.cur.fetchall()
        try:
            if count[0][0] == self.name and count[0][1] == self.pwd:
                self.conn.send(b"OK")
            else:
                self.conn.send(b"UorPisError")
        except:
            self.conn.send(b"NoUser")

    # 查询(随机选择菜品)
    def query(self, data):
        # data-->[flag,genre]
        genre = data[1]
        if genre == "BF":
            fflag = "breakfast"
        elif genre == "LC":
            fflag = "lunch"
        elif genre == "DN":
            fflag = "dinner"
        elif genre == "DK":
            fflag = "drinks"

        self.cur.execute(
            "select f_name from %s where user_id =\
            (select id from user where name='%s');" % (fflag, self.name))
        goods = self.cur.fetchall()

        self.cur.execute(
            "select count(*) from %s where user_id =\
            (select id from user where name='%s');" % (fflag, self.name))
        total = self.cur.fetchall()[0][0]
        if total>0:
            result = goods[random.randint(0, total - 1)][0]
            self.conn.send(b"%s" % result)
        else:
            self.conn.send(b"NoFood")

    # 修改
    def alter(self, data):
        # data-->[flag,alterflag,genre,goods]
        aflag = data[1]
        genre = data[2]
        goods = data[3]
        if genre == "BF":
            fflag = "breakfast"
        elif genre == "LC":
            fflag = "lunch"
        elif genre == "DN":
            fflag = "dinner"
        elif genre == "DK":
            fflag = "drinks"

        self.cur.execute(
            "select id from user where name='%s';" % self.name)
        uid = self.cur.fetchall()[0][0]

        if aflag == "DEL":
            try:
                self.cur.execute(
                    "delete from %s where user_id=%s and f_name='%s';"
                    % (fflag, uid, goods))
                self.db.commit()
                self.conn.send(b"AlterSucceed")
            except:
                self.conn.send(b"AlterDefeat")

        elif aflag == "ALT":
            try:
                self.cur.execute(
                    "insert into %s value(null,%s,'%s');"
                    % (fflag, uid, goods))
                self.db.commit()
                self.conn.send(b"AlterSucceed")
            except:
                self.db.rollback()
                self.conn.send(b"AlterDefeat")


def main():
    twe_s = TWE_server()
    twe_s.serve_forever()


if __name__ == '__main__':
    main()
