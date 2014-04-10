myfunc
======

Description
=======
an improve version of fedora Func, easy to install and run for everyone(not only root to install and run)

FUNC安装
=======

Step1:
下载相应版本的openssl放进$HOME/download目录，Makefile中的版本为1.0.1e，如果版本不同，请修改Makefile

下载相应版本的python放进$HOME/download目录，Makefile中的版本为2.7.3，如果版本不同，请修改Makefile

下载相应版本的py放进$HOME/download目录，Makefile中的版本为2.7.3，如果版本不同，请修改Makefile

下载相应版本的pyOpenSSL放进$HOME/download目录，Makefile中的版本为0.11，如果版本不同，请修改Makefile

Step2:
    $ make
    $ make [install|install-openssl|install-python|install-pyOpenssl|install-func]

其中install表示一次性安装所有的，及包含了install-*的所有目标，默认安装路径位于$HOME/local下，若路径不一样，请修改Makefile。
安装结束后func的相关执行文件会存在于$HOME/local/Python2.7.3/bin目录，请修改Makefile。


FUNC配置
=======
安装完后配置文件位于$HOME/local/Python2.7.3/etc目录下

master(或者叫overlord)启动前要配置的文件：
etc/certmaster/certmaster.conf: 配置master本身的监听端口
etc/func/overlord.conf：配置minion的监听端口，master向该服务端口的minion发命令，该master下的所有minion必需均使用该监听端口

minion(或者叫slave)启动前要配置的文件：
etc/certmaster/minion.conf: master的监听信息，minion连接到该master
etc/func/minion.conf：minion本身的监听端口，与master中etc/func/overlord.conf的端口一致

FUNC启动
=======

Step1: 启动master
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster

Step2: 启动minion
$ cd $HOME/local/Python2.7.3/bin && ./python funcd 

Step3: 签名信任
查看待签名列表
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster-ca -l
$ platform1

签名
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster-ca -s platform1

测试连通性
$ cd $HOME/local/Python2.7.3/bin && ./python func '*' ping
$ [ok...] platform1


签名管理常用操作(这些操作均在master执行)
--------------
查看待签名列表
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster-ca -l

查看已签名列表
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster-ca -l

执行签名
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster-ca -s platform1

取消签名
$ cd $HOME/local/Python2.7.3/bin && ./python certmaster-ca -c platform1

【注意】
取消签名后，需将minion中的etc/pki/certmaster目录下对应于该minion的cert证书删除，如这里的platform1.cert,
否则当下次再次启动minion时，在master的certmaster-ca -l中将看不到该minion

FUNC API调用例子
================
deploy.py和test_deploy.sh是用使用Func API做自动部署的例子

Q & A
=========

1. 移除并重新创建overlord(master)之后，地址端口都没改变，为什么ping不通minion(slave)了？查看日志文件也没有发现？

   因为overlord重新产生了CA，所有minion都必须干掉原有证书，重新启动funcd，以再次发起签名请求，
   方法：删除$HOME/local/Python2.7.3/etc/pki/certmaster目录下的minion_name.cert(如platform.cert)证书文件即可。

2. minion启动funcd出现以下错误：
   Exception occured: <class 'socket.gaierror'>
   Exception value: [Errno -2] Name or service not known
   ...

   请检查$HOME/local/Python2.7.3/etc/certmaster/minion.conf的certmaster，指定的hostname是否可以解析。

3. overlord(master)和minion(slave)都可以正常启动，但在overlord(master)上执行func操作命令会出现以下错误：
   ...
   File "/home/Python2.7.3/local/Python2.7.3/lib/python2.7/site-packages/func/overlord/client.py", line 550, in setup_ssl
     myname = func_utils.get_hostname_by_route()
   File "/home/Python2.7.3/local/Python2.7.3/lib/python2.7/site-packages/func/utils.py", line 107, in get_hostname_by_route
     s.connect_ex((server, port))
   File "/home/Python2.7.3/local/Python2.7.3/lib/python2.7/socket.py", line 224, in meth
     return getattr(self._sock,name)(*args)
   socket.gaierror: [Errno -2] Name or service not known

   请在overlord(master)上检查etc/certmaster/minion.conf的certmaster，上面两个程序会读到该参数，以找到自己的证书文件。

4. 如果多个minion(slave)的其中若干个更换了IP或hostname，可能会导致overlord(master)上执行各类操作命令都很慢。

   请在overlord(master)上执行certmaster-ca --list-signed，然后把其中旧的IP或hostname删除，例如：
   certmaster-ca -c 192.168.59.34

