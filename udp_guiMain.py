#!/usr/bin/env python
#coding=utf-8
from Tkinter import *
import tkMessageBox
import string
import Pmw
from udpTool import udpTool
from upd_workManager import WorkManager
from upd_workManager import Work
import time
import Queue


class udp(object):
    'udp class'
    def __init__(self,master):

        master.configure(background = 'gray')
        # self.udptool = udpTool(133,135,8089)
        self.beginip=100
        self.endip=150
        self.contralLabel = Label(master,bg='gray', text='控制命令:')
        self.contralLabel.grid(row=1,column=1)
        self.cmdInt =1;
        self.cmdStr=StringVar() #wntime.com
        self.contralEntry = Entry(master,width=15,bg='gray',textvariable=self.cmdStr)
        self.workManager = None
        tmp=  'wntime.com'+str(self.cmdInt)
        self.cmdStr.set(tmp)
        self.contralEntry.grid(row=1, column=2)
        self.isRunable= True
        # 控制命令 下拉列表
        commandType = ('1', '2', '3', '4')
        dropdown = Pmw.ComboBox(
            	master,
                selectioncommand = self.selectCmdType,
                labelpos = 'n',
            	scrolledlist_items = commandType,)
        dropdown.grid(row=1,column=3)
        first = commandType[0]
        dropdown.selectitem(first)

        #发送指令 button
        self.sendButton = Button(master,bg='gray', text='发送', command=self.sendMessage)
        self.sendButton.grid(row=1, column=15)

        #---------- 网络范围
        self.ipStrLabel = Label(master,bg='gray', text='扫描范围:')
        self.ipStrLabel.grid(row=0,column=1)

        self.ipLabel = Label(master,bg='gray',text='192.168.2.1  ~~ 192.168.2.254')
        self.ipLabel.grid(row=0,column=2)

        # 此方法是利用线程池做的ip地址发送
        self.sendButton = Button(master,fg='gray', text='接收', command=self.startReviceData)
        self.sendButton.grid(row=0, column=15)

        # 此方法是利用生产者消费者模型做的不间断扫描
        #self.sendButton2 = Button(master,fg='gray', text='多线程接收', command=self.startMuliThreadReviceData)
        #self.sendButton2.grid(row=0, column=15)



        # self.sendButton.bind('<Button-1>', self.startReviceData)

        self.sendButton = Button(master,fg='gray', text='停止', command=self.stopReviceData)
        self.sendButton.grid(row=0, column=16)

        self.clearButton = Button(master,fg='gray', text='清空', command=self.clear)
        self.clearButton.grid(row=2, column=15,columnspan=4)

        self.frame = Frame(master, width=500, height=100, bd=1)
        self.frame.grid(row=3,column=1,columnspan=4)
        self.deviceListFrame = Frame(self.frame, bd=2, relief=SUNKEN)

        self.text=Text(self.deviceListFrame, height=25, width =70)
        self.text.insert(END, '点击【接收】按钮开始接收数据\n')
        self.text.pack(side=LEFT, fill=X, padx=5)

        self.sb = Scrollbar(self.deviceListFrame, orient=VERTICAL, command=self.text.yview)
        self.sb.pack(side=RIGHT, fill=Y)
        self.sb2 = Scrollbar(self.deviceListFrame, orient=VERTICAL, command=self.text.yview)
        self.sb.pack(side=LEFT, fill=Y)
        self.text.configure(yscrollcommand=self.sb.set)
        self.deviceListFrame.pack(fill=X,padx=5)


    '监听下拉框改变函数'
    def selectCmdType(self,cmdInt):
        tmp=  'wntime.com'+str(cmdInt)
        self.cmdStr.set(tmp)
        print self.cmdStr.get().strip()

    def test(self):
        self.text.insert(END, time.strftime('%H:%M:%S'))
    def handle(self):
        time.sleep(20)

    '监听【接收数据】按钮 向设备进行数据发送'
    def startReviceData(self):
        self.text.insert(END, time.strftime('%H:%M:%S')+' 开始接收数据，请耐心等待...\n')
        work_manager =  WorkManager(dataText=self.text,beginip=self.beginip,endip=self.endip)

    '监听【停止接收】按钮'
    def stopReviceData(self):
        #self.product.stop()
        #self.consumer.stop()
        self.text.insert(END, time.strftime('%H:%M:%S')+' 点击【接收】按钮开始接收数据\n')
        self.isRunable=False

    '开始多线程不间断接收数据信息'
    def startMuliThreadReviceData(self):
        self.product =  ProducerThread()
        self.product.setDaemon(True)
        self.consumer = ConsumerThread()
        self.self.consumer.setDaemon(True)
        self.product.start()
        self.consumer.start();

    def getMailInfo(self):
        self.sendToAdd = self.sendToEntry.get().strip()
        self.subjectInfo = self.subjectEntry.get().strip()
        self.sendTextInfo = self.sendText.get(1.0, END)


    def sendMessage(self):
        tkMessageBox.showinfo('提示','你设备端功能实现了么？？？？')

        return
        self.getMailInfo()
        body = string.join(("From: %s" % self.sender, "To: %s" % self.sendToAdd, "Subject: %s" % self.subjectInfo, "", self.sendTextInfo), "\r\n")
        try:
            self.smtp.sendmail(self.sender, [self.sendToAdd], body)
        except Exception, e:
            tkMessageBox.showerr('发送失败', "%s" % e)
            return
        tkMessageBox.showinfo('提示', '邮件已发送成功！')

    '清空局域网设备列表'
    def clear(self):
        self.text.delete(1.0,END)
        self.text.insert(END, '....重新开始接收传感器数据......\n')


if __name__ == '__main__':
    root = Tk()
    root.geometry('800x500+512+512')
    root.title('空气质量检测仪--传感器质检程序')
    udp =udp(root)

    mainloop()

