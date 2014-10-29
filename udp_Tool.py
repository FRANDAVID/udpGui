#!/usr/bin/env python
#coding=utf-8
'use UDP send echo message to server. 初始版本为单线程，后续版本改为多线程'
import socket
from rc4base64 import rc4base64
import time
class udpTool(object):

    '__init__'
    def __init__(self,beginip,endip,port,timeout=0):
        self.network='192.168.2.' # ip起始地址
        self.port=port
        self.beginip=beginip
        self.endip=endip
        self.timeout=timeout #经过单设备测试，单次，单设备返回需要经过37秒的时间
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    '循环ip地址'
    def run(self,s):
        print '程序开始循环ip地址192.168.2.2 ~~192.168.2.254'
        for ip in xrange(self.beginip,self.endip):    ## 'ping' addresses 192.168.1.1 to .1.255
            addr = str(self.network) + str(ip)
            print '向【',addr,'】发送试探数据'
            #s.settimeout(self.timeout)
            s.sendto('test',(addr ,self.port))
            print 'time:【',time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())), '】数据已经发送'
            # 接收数据:
            try:
                data = s.recv(1024)
                print 'time:【',time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())),'】已经接收到数据'
                encodeData = data.split('param=');
                reg = encodeData[1]
                print 'encodeData',reg
                print 'decodeData',rc4base64.RC4decode(rc4base64.base64decode(reg), 'wntime.com')

            except Exception, e:
                continue

        self.s.close()
    def runWithIp(self,iplist,s):
        print '程序开始循环ip地址192.168.2.2 ~~192.168.2.254'
        for ip in iplist:    ## 'ping' addresses 192.168.1.1 to .1.255
            addr = str(ip)
            print '向【',addr,'】发送试探数据'
            #s.settimeout(self.timeout)
            s.sendto('test',(addr ,self.port))
            print 'time:【',time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())), '】数据已经发送'
            # 接收数据:
            try:
                data = s.recv(1024)
                print 'time:【',time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())),'】已经接收到数据'
                encodeData = data.split('param=');
                reg = encodeData[1]
                print 'encodeData',reg
                print 'decodeData',rc4base64.RC4decode(rc4base64.base64decode(reg), 'wntime.com')

            except Exception, e:
                continue

        self.s.close()
    '提供gui调用的socket 函数 由gui 负责循环ip'
    def runWithNoLoop(self,s,addr,port):
        # print '向【',addr,'】发送试探数据'
        #s.settimeout(self.timeout)
        s.sendto('test',(addr ,port))
        print 'time:【',time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())), '】数据已经发送'
        # 接收数据:
        data = s.recv(1024)
        print 'time:【',time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())),'】已经接收到数据'
        encodeData = data.split('param=');
        reg = encodeData[1]
        print 'encodeData',reg
        decodeData= rc4base64.RC4decode(rc4base64.base64decode(reg), 'wntime.com')
        print 'decodeData',rc4base64.RC4decode(rc4base64.base64decode(reg), 'wntime.com')
        return decodeData
    '停止发送试探数据'
    def stopSocket(self):
        self.s.close();

'提供gui调用的socket 函数 由gui 负责循环ip'
def runWithThread(s,addr,port):
        print '向【',addr,'】发送试探数据'
        #s.settimeout(self.timeout)
        s.sendto('test',(addr ,port))
        print '【',time.strftime('%H:%M:%S'),'】===>【',addr,'】发送数据'
        # 接收数据:
        data = s.recv(1024)
        encodeData = data.split('param=');
        reg = encodeData[1]
        decodeData= rc4base64.RC4decode(rc4base64.base64decode(reg), 'wntime.com')
        print '【',time.strftime('%H:%M:%S'),'】===>【',addr,'】数据', decodeData
        return decodeData
if __name__=='__main__':
    udptool = udpTool(beginip=133,endip=137,port=8089)
    iplist=['192.168.2.144','192.168.2.107']
    udptool.runWithIp(iplist,udptool.s)
    # udptool.run(udptool.s)
    # udptool.runWithNoLoop(udptool.s,'192.168.2.133', 8089)


