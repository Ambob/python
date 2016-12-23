#!/usr/bin/env python  
# -*- coding: utf-8 -*
import serial
import serial.tools.list_ports
import time
import os
from time import sleep
import sys
import json
import socket
#子函数，将返回的数据以16进制形式展现
def add_imei_to_server(imei,phone):
    HOST="temp.hbd.so"
    PORT=9729
    s=None
    print "is",socket.getaddrinfo(HOST,PORT,socket.AF_UNSPEC,socket.SOCK_STREAM)
    if (socket.getaddrinfo(HOST,PORT,socket.AF_UNSPEC,socket.SOCK_STREAM)):
        for res in socket.getaddrinfo(HOST,PORT,socket.AF_UNSPEC,socket.SOCK_STREAM):
            af,socktype,proto,canonname,sa = res
            try:
                s=socket.socket(af,socktype,proto)
            except socket.error,msg:
                s=None
                continue
            try:
                s.connect(sa)
            except socket.error,msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print "不能与服务器建立连接......."
        else:
            send_data="imei_phone"+imei+"_"+phone
            s.sendall(send_data)
            s.close()
def hexShow(argv):  
    result = ''  
    hLen = len(argv)  
    for i in xrange(hLen):  
        hvol = ord(argv[i])  
        hhex = '%02x'%hvol  
        result += hhex+' '  
    return result
def read_command(ser,pinchuan):
    #发出去
    ser.write(pinchuan)
    #读一行
    read_text=ser.read(10240)
    print "返回值是:",read_text.strip()
    #转成16进制字符串
    result=hexShow(read_text)
def com_open(ser1,config_json):
    try:
        ser=serial.Serial(ser1,9600,timeout=2)
    except Exception as e:
        print "串口打开失败，请检查"
        raise e
    finally:
        for a in config_json:
            if(a=="serial"):
                pass
            else:
                print "设置",a,"下发",config_json[a]
                read_command(ser,config_json[a].encode()+'\r\n')
                sleep(2)
        ser.close()
if __name__ == '__main__':
    port_list=list(serial.tools.list_ports.comports())
    file_name_list=sys.argv[0].split("/")[0:-1]
    path_name=''
    for a in file_name_list:
        path_name+=a+"/"
    imei=sys.argv[1]
    phone=sys.argv[2]
    with open(path_name+"config.json","r") as fp:
        config_json=json.loads(fp.read())
    print "当前设置的串口为:",config_json["serial"]
    for a in port_list:
        serial_find=0
        print "检测到电脑上存在串口:",a[0]
        if (config_json["serial"]==a[0]):
            add_imei_to_server(imei,phone)
            serial_find=1
            com_open(config_json["serial"],config_json)
            break
    if(serial_find==0):
        print "请检查config.json里面的serial设置是否正确，或者USB数据线是否插入"