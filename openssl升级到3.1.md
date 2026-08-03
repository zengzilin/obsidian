# openssl升级到3.1

下载

执行

./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib 

**报错**

Can't locate IPC/Cmd.pm in @INC (@INC contains: /root/openssl-3.1.1/util/perl /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 . /root/openssl-3.1.1/external/perl/Text-Template-1.56/lib) at /root/openssl-3.1.1/util/perl/OpenSSL/config.pm line 19. BEGIN failed--compilation aborted at /root/openssl-3.1.1/util/perl/OpenSSL/config.pm line 19. Compilation failed in require at /root/openssl-3.1.1/Configure line 23. BEGIN failed--compilation aborted at /root/openssl-3.1.1/Configure line 23.

**<font style="color:#DF2A3F;">解决方法</font>**

安装perl-IPC-Cmd

 yum install perl-IPC-Cmd



> 更新: 2025-06-04 11:06:22  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/oeqxsnqmpnrzz7v6>