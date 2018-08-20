#/usr/bin/python3
# -*- coding: utf-8 -*-


'''
author:QYK
mail:ethan.71@163.com
content:WTE's server
'''

import socket
import tkinter as tk
import sys
import time


class WTE_client(object):

    def __init__(self):
        hostaddr = socket.gethostbyname(
            socket.getfqdn(socket.gethostname()))  # 获取本机IP
        self.ADDR = ('176.17.112.197', 7771)
        print(self.ADDR)

    # 连接服务器
    def serve_forever(self):
        self.conn = socket.socket()
        self.conn.connect(self.ADDR)
        self.primart_interface()

    # 一级登录界面
    def primart_interface(self):
        self.root = tk.Tk()
        self.root.geometry("220x150")
        self.root.title("登录界面")

        self.label1 = tk.Label(self.root, text="用户名：")
        self.label1.place(x=20, y=20, width=50)
        self.label2 = tk.Label(self.root, text="密码：")
        self.label2.place(x=20, y=50, width=50)
        self.label3 = tk.Label(self.root, text="")
        self.label3.place(x=50, y=75, width=120)

        self.entry1 = tk.Entry(self.root, )
        self.entry1.place(x=70, y=20, width=130)
        self.entry2 = tk.Entry(self.root, show="*")
        self.entry2.place(x=70, y=50, width=130)

        self.button1 = tk.Button(self.root, text="注册",
                                 command=self.register_gui)
        self.button1.place(x=40, y=100, width=50)
        self.button2 = tk.Button(self.root, text="登录", command=self.login)
        self.button2.place(x=130, y=100, width=50)

        self.root.mainloop()
        # self.secondary_interface_gui()

    # 登录界面与服务器通信的函数
    def login(self):
        print("注册界面")
        name = self.entry1.get()
        pwd = self.entry2.get()
        msg = "LG#%s#%s" % (name, pwd)
        self.conn.send(msg.encode())
        data = self.conn.recv(2048).decode()
        if data == "OK":
            print("登录成功！")
            self.go_secondary_interface1()
        elif data == "UorPisError":
            print("用户名或密码，请重试！")
            self.label3["text"] = ""
            self.label3["text"] = "用户名或密码，请重试！"
        elif data == "NoUser":
            self.label3["text"] = "无此用户，请注册"

    # 注册界面的gui
    def register_gui(self):
        self.root.destroy()  # 销毁登录界面

        # 创建注册界面
        self.root1 = tk.Tk()
        self.root1.geometry("250x180")
        self.root1.title("注册界面")

        self.label1 = tk.Label(self.root1, text="用户名：")
        self.label1.place(x=20, y=20, width=70)
        self.label2 = tk.Label(self.root1, text="密码：")
        self.label2.place(x=20, y=50, width=70)
        self.label3 = tk.Label(self.root1, text="确认密码：")
        self.label3.place(x=20, y=80, width=70)
        self.label4 = tk.Label(self.root1, text="")
        self.label4.place(x=50, y=110, width=150)
        self.button = tk.Button(self.root1, text="返回",
                                command=self.back_primart_interface,
                                relief="flat")
        self.button.place(x=180, y=145)

        self.entry1 = tk.Entry(self.root1, )
        self.entry1.place(x=90, y=20, width=130)
        self.entry2 = tk.Entry(self.root1, show="*")
        self.entry2.place(x=90, y=50, width=130)
        self.entry3 = tk.Entry(self.root1, show="*")
        self.entry3.place(x=90, y=80, width=130)

        self.button1 = tk.Button(
            self.root1, text="立即注册", command=self.register)
        self.button1.place(x=75, y=140, width=100)

        self.root1.mainloop()

    # 点击注册界面返回时销毁注册界面并再测调用登录界面
    def back_primart_interface(self):
        self.root1.destroy()
        self.primart_interface()

    # 注册界面的与服务器通信的函数
    def register(self):
        name = self.entry1.get()
        pwd = self.entry2.get()
        pwd_ag = self.entry3.get()
        if pwd != pwd_ag:
            self.label4["text"] = ""
            self.label4["text"] = "两次密码不同！"
        else:
            msg = "RG#%s#%s" % (name, pwd)
            self.conn.send(msg.encode())
            data = self.conn.recv(2048).decode()
            if data == "OK":
                print("注册成功！")
                self.label4["text"] = "注册成功！"
                time.sleep(3)
                self.go_secondary_interface2()
            elif data == "UserInsertError":
                print("系统错误，请重试！")
                self.label4["text"] = ""
                self.label4["text"] = "系统错误，请重试！"
            elif data == "UserAlreadyExists":
                print("用户名已经存在，请重试！")
                self.label4["text"] = ""
                self.label4["text"] = "用户名已经存在，请重试！"

    # 二级主界面
    def secondary_interface_gui(self):
        self.root2 = tk.Tk()
        self.root2.geometry("300x200")
        self.root2.title("今天吃什么？")

        eat = tk.StringVar()

        self.radiobutton1 = tk.Radiobutton(
            self.root2, text="早餐", variable=eat, value="BF")
        self.radiobutton1.place(x=30, y=50)
        self.radiobutton2 = tk.Radiobutton(
            self.root2, text="午餐", variable=eat, value="LC")
        self.radiobutton2.place(x=90, y=50)
        self.radiobutton3 = tk.Radiobutton(
            self.root2, text="晚餐", variable=eat, value="DN")
        self.radiobutton3.place(x=150, y=50)
        self.radiobutton4 = tk.Radiobutton(
            self.root2, text="饮料", variable=eat, value="DK")
        self.radiobutton4.place(x=210, y=50)

        self.label1 = tk.Label(self.root2, text="吃吃吃吃！")
        self.label1.place(x=75, y=100, width=150)

        self.button1 = tk.Button(
            self.root2, text="今天吃什么？", command=lambda:
            self.secondary_interface(eat.get()))
        self.button1.place(x=100, y=130, width=100)

        self.topmenu = tk.Menu(self.root2)
        self.tj = tk.StringVar()
        self.root2.config(menu=self.topmenu)
        tmenu1 = tk.Menu(self.topmenu)
        tmenu1.add_radiobutton(label="早餐", value="BF",
                               variable=self.tj, command=self.alter_gui)
        tmenu1.add_radiobutton(label="午餐", value="LC",
                               variable=self.tj, command=self.alter_gui)
        tmenu1.add_radiobutton(label="晚餐", value="DN",
                               variable=self.tj, command=self.alter_gui)
        tmenu1.add_radiobutton(label="饮料", value="DK",
                               variable=self.tj, command=self.alter_gui)
        self.topmenu.add_cascade(label="添加", menu=tmenu1)

        tmenu2 = tk.Menu(self.topmenu)
        tmenu2.add_command(label="注销", command=self.back_primart_interface)
        tmenu2.add_command(label="退出", command=self.quit)
        self.topmenu.add_cascade(label="系统", menu=tmenu2)

        self.root2.mainloop()

        #     elif x == "alter":
        #         msg = "AT#DEL#LC#宫保鸡丁"
        #         self.conn.send(msg.encode())
        #         data = self.conn.recv(1024).decode()
        #         if data == "AlterSucceed":
        #             print("修改成功！")
        #         elif data == "AlterDefeat":
        #             print("修改失败！")
        #     else:
        #         print("请正确输入命令！")

    #修改菜单界面
    def alter_gui(self):
        food={"BF":"早餐","LC":"午餐","DN":"晚餐","DK":"饮料"}
        self.root3 = tk.Tk()
        self.root3.geometry("500x500")
        self.root3.title(food[self.tj.get()])
        
        self.root3.mainloop()

    # 随机函数
    def secondary_interface(self, flag):
        msg = "QE#%s" % flag
        self.conn.send(msg.encode())
        data = self.conn.recv(1024).decode()
        if data == "NoFood":
            self.label1["text"] = "吃空气！"
        else:
            self.label1["text"] = data

    # 登录跳到二级界面
    def go_secondary_interface1(self):
        self.root.destroy()
        self.secondary_interface_gui()

    # 注册跳到二级界面
    def go_secondary_interface2(self):
        self.root1.destroy()
        self.secondary_interface_gui()

    # 注销，跳转到登录界面
    def back_primart_interface(self):
        self.root2.destroy()
        self.primart_interface()

    # 推出客户端
    def quit(self):
        self.root2.destroy()


def main():
    wte_c = WTE_client()
    wte_c.serve_forever()


if __name__ == '__main__':
    main()
