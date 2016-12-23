第一次使用

首先安装serial模块
>打开'终端',输入

~~~bash
sudo easy_install install pyserial
~~~
然后下载usb－serial驱动

https://sourceforge.net/projects/osx-pl2303/

安装后重启电脑

然后


正常使用

~~~bash
sudo python ~/Desktop/avl11_set/avl11_set.py
~~~
有类似下面的返回

~~~bash
/dev/cu.usbserial send is *000000,015,1,temp.hbd.so,9729#

/dev/cu.usbserial recieve is

CMD bytes: 1F 
*000000,015,1,temp.hbd.so,9729#
ComdType:015(SETIPANDPORT)
Mode:01 
IP/Domain Name:temp.hbd.so
Port:9729

~~~

即为ok