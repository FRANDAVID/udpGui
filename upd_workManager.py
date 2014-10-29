# !/usr/bin/env python
# -*- coding:utf-8 -*-

import Queue
import threading
import time
import socket
from Tkinter import *
from rc4base64 import rc4base64
isRunable= True
class WorkManager(object):
    def __init__(self, dataText=None,work_num=255,thread_num=100,beginip=2,endip=250,port=8089,network='192.168.2.'):
        self.num = work_num
        self.work_queue = Queue.Queue(maxsize = work_num)
        self.threads = []
        self.beginip=beginip
        self.endip=endip
        self.port=port
        self.network=network
        self.dataText=dataText
        self.__init_work_queue(work_num)
        self.__init_thread_pool(thread_num)
    """
        初始化线程
    """
    def __init_thread_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))

    """
        初始化工作队列
    """
    def __init_work_queue(self, jobs_num):
        for ip in xrange(self.beginip,self.endip):    ## 'ping' addresses 192.168.1.1 to .1.255
            addr = str(self.network) + str(ip)
            self.add_job(do_job,self.dataText,addr,self.port)
        print '当前工作队列中的任务个数',self.work_queue.qsize()
        # for i in range(jobs_num):
        #     self.add_job(do_job, i)

    def init_work_queue(self, jobs_num):
        for ip in xrange(self.beginip,self.endip):    ## 'ping' addresses 192.168.1.1 to .1.255
            addr = str(self.network) + str(ip)
            self.add_job(do_job,self.dataText,addr,self.port)
        print '重新进入工作队列中的任务个数',self.work_queue.qsize()
        # for i in range(jobs_num):
        #     self.add_job(do_job, i)



    """
        添加一项工作入队
    """
    def add_job(self, func, *args):
        self.work_queue.put((func, list(args)))#任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread): #定义主类时被默认调用了！
    isRunable=True
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.work_queue = work_queue
        self.temp_queue = work_queue
        self.start()


    def run(self):
        #死循环，从而让创建的线程在一定条件下关闭退出
        while isRunable:
            try:
                do, args = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                do(args)
                self.work_queue.put((do,args))
            except Exception ,e:
                print e
                break

#具体要做的任务
def do_job(args): #传入gui 传感器列表对象用来追加数据
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('test',(args[1] ,args[2]))
    data = s.recv(1024)
    encodeData = data.split('param=');
    reg = encodeData[1]
    decodeData= rc4base64.RC4decode(rc4base64.base64decode(reg), 'wntime.com')
    print '【',time.strftime('%H:%M:%S'),'】===>【接收到',args[1],'】数据', decodeData
    args[0].insert(END, decodeData+'\n')

if __name__ == '__main__':
    start = time.time()
    work_manager =  WorkManager()#或者work_manager =  WorkManager(10000, 20)
    # work_manager.wait_allcomplete() #为了实现异步效果 就不能wait le
    end = time.time()
    print "cost all time: %s" % (end-start)

