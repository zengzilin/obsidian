# 服务器上安装rsync服务

（一）  在backup服务器上安装rsync服务



部署环境：64位的Centos6.7系统；内核2.6.32-573

[root@backup ~]# uname -a

Linux backup 2.6.32-573.el6.x86_64 #1 SMPThu Jul 23 15:44:03 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux

Rsync服务端部署步骤：



1. 检查是否已安装rsync服务

[root@backup ~]# rpm -qa |grep rsync

rsync-3.0.6-12.el6.x86_64



2.编辑rsync的配置文件/etc/rsyncd.conf(默认不存在)

#rsync_config___start

#created by oldboy 20170301

uid = rsync（虚拟用户:远程访问共享文件）

gid = rsync(虚拟用户组)

use chroot = no （安全相关）

max connections = 200（最大连接数）

timeout = 300（超时时间）

pid file = /var/run/rsyncd.pid（进程号所在文件）

lock file = /var/run/rsync.lock（锁文件）

log file = /var/log/rsyncd.log（日志文件）

ignore errors（忽略错误）

read only = false （可写）

list = false（不能列表）

hosts allow = 172.16.1.0/24 （允许远程访问的网段）

hosts deny = 0.0.0.0/32（拒绝远程访问的网段）

auth users = rsync_backup（远程访问账号）

secrets file = /etc/rsync.password（远程访问密码文件）



[backup]（模块名称）

path = /backup（服务器供访问的目录）

[nfsbackup]（可添加多个模块）

path = /nfsbackup



3.新建虚拟用户；

 [root@backup ~]# mkdir useradd rsync -s/sbin/nologin –M

[root@backup ~]# tail /etc/passwd|greprsync

rsync:x:510:510::/home/rsync:/sbin/nologin

新建访问目录并改变属主，属组

[root@backup ~]# mkdir -p /backup/

[root@backup ~]# chown rsync.rsync -R/backup/

[root@backup ~]# ls -ld /backup/

drwxr-xr-x. 4 rsync rsync 4096 3月  14 19:24 /backup/



4.编辑远程访问密码文件/etc/rsync.password,并改变其权限

[root@backup ~]# cat /etc/rsync.password

rsync_backup:123456

[root@backup ~]# chmod 600/etc/rsync.password

[root@backup ~]# ls -l /etc/rsync.password

-rw-------. 1 root root 20 3月   2 00:46 /etc/rsync.password



5.启动rsync daemon服务

[root@backup ~]# rsync –daemon

检查其是否启动成功：

方法一：

[root@backup ~]# ps -ef|grep rsync

root      4036      1  0 06:01 ?        00:00:00 rsync --daemon

root      4444   4337  0 10:32 pts/0    00:00:00 grep rsync

方法二：

[root@backup ~]# lsof -i:873

COMMAND PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME

rsync  4036 root    3u  IPv4 20432      0t0  TCP *:rsync (LISTEN)

rsync  4036 root    5u  IPv6 20433      0t0  TCP *:rsync (LISTEN)



6.将rsync加入开机自启动

[root@backup ~]# tail -1 /etc/rc.local   

/usr/bin/rsync –daemon



Rsync客户端部署

1.修改/etc/rsync.password文件

[root@nfs01 ~]# cat /etc/rsync.password

123456

[root@nfs01 ~]# ls -l /etc/rsync.password

-rw-------. 1 root root 7 3月   2 00:05 /etc/rsync.password

2.创建备份目录

[root@nfs01 ~]# mkdir -p /backup/



检验客户端推送更新是否生效

客户端推送：方法一

[root@nfs01 backup]# ll

总用量 20

drwxr-xr-x 2 root root 4096 3月  13 00:14 172.16.1.31

-rw-r--r-- 1 root root  788 3月  15 00:00 backup_2017-03-14.tar.gz

drwxr-xr-x 2 root root 4096 3月   6 18:33 data

-rw-r--r-- 1 root root   68 3月  15 00:00 flag_2017-03-14.log

-rw-r--r-- 1 root root  417 3月  14 19:00 hosts

[root@nfs01 backup]# touch stu{1..4}

[root@nfs01 backup]# ll

总用量 20

drwxr-xr-x 2 root root 4096 3月  13 00:14 172.16.1.31

-rw-r--r-- 1 root root  788 3月  15 00:00 backup_2017-03-14.tar.gz

drwxr-xr-x 2 root root 4096 3月   6 18:33 data

-rw-r--r-- 1 root root   68 3月  15 00:00 flag_2017-03-14.log

-rw-r--r-- 1 root root  417 3月  14 19:00 hosts

-rw-r--r-- 1 root root    0 3月  15 00:13 stu1

-rw-r--r-- 1 root root    0 3月  15 00:13 stu2

-rw-r--r-- 1 root root    0 3月  15 00:13 stu3

-rw-r--r-- 1 root root    0 3月  15 00:13 stu4

[root@nfs01 backup]#rsync -avz /backup/ rsync_backup@172.16.1.41::backup--password-file=/etc/rsync.password  

sending incremental filelist

./

stu1

stu2

stu3

stu4

出现上述红体字命令的结果证明更新备份成功。

方法二

[root@nfs01 backup]# rsync -avz /backup/rsync://rsync_backup@172.16.1.41/backup--password-file=/etc/rsync.password   

sending incremental file list

./

stu1

stu2

stu3

stu4



sent 451 bytes  received 89 bytes  1080.00 bytes/sec

total size is 2140  speedup is 3.96



客户端从服务端拉取：

方法一

[root@nfs01backup]#rsync -avz--exclude={stu2,stu3} rsync://rsync_backup@172.16.1.41/backup /backup/--password-file=/etc/rsync.password

方法二：

[root@nfs01backup]# rsync -avz--exclude={stu2,stu3,stu4} rsync_backup@172.16.1.41::backup /backup/--password-file=/etc/rsync.password



（二）在nfs服务器上安装inotify

2.1检查环境并安装inotify-tools

[root@nfs01 data]# ls -l/proc/sys/fs/inotify/（有这个文件，表示支持inotify）

总用量 0

-rw-r--r-- 1 root root 0 3月  15 15:29 max_queued_events

-rw-r--r-- 1 root root 0 3月  15 15:29 max_user_instances

-rw-r--r-- 1 root root 0 3月  15 15:29 max_user_watches

[root@nfs01 data]# rpm -qa inotify-tools(检查是否已安装)

[root@nfs01data]#wget -O  /etc/yum.repos.d/epel.repo [http://mirrors.aliyun.com/repo/epel-6.（yum安装inotify-tools需下载第三方yum源）](http://mirrors.aliyun.com/repo/epel-6.（yum安装inotify-tools需下载第三方yum源）)

 [root@nfs01 data]# yum install inotify-tools –y



> 更新: 2024-09-14 08:31:16  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ledxef0xlcytto8p>