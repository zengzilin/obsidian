# redhat10编译安装nginx 1.26.2

# 下载必要依赖
dnf  install gcc gcc-c++ autoconf automake make openssl-devel

dnf install -y zlib-devel

wget [https://codeload.github.com/yaoweibin/nginx_upstream_check_module/zip/master](https://codeload.github.com/yaoweibin/nginx_upstream_check_module/zip/master)  -O nginx_upstream_check_module.zip 

unzip nginx_upstream_check_module.zip  -d /app/nginx/

[https://ftp.pcre.org/pub/pcre/pcre-8.45.tar.gz](https://ftp.pcre.org/pub/pcre/pcre-8.45.tar.gz) 或者 [https://downloads.sourceforge.net/project/pcre/pcre/8.45/pcre-8.45.tar.gz](https://downloads.sourceforge.net/project/pcre/pcre/8.45/pcre-8.45.tar.gz)

# ~~编译安装prce(不生效)~~
[https://blog.csdn.net/qq_44534541/article/details/143924185](https://blog.csdn.net/qq_44534541/article/details/143924185)

<font style="color:rgba(0, 0, 0, 0.9);">官方地址（最新版 8.45）：</font>

```plain
https://ftp.pcre.org/pub/pcre/pcre-8.45.tar.gz
```

<font style="color:rgba(0, 0, 0, 0.9);">国内镜像（若官方不可用）：</font>

```plain
https://downloads.sourceforge.net/project/pcre/pcre/8.45/pcre-8.45.tar.gz
```

tar -zxvf pcre-8.45.tar.gz  

cd pcre-8.45

./configure --prefix=/usr/local/pcre-8.45  # 指定安装路径 

make && sudo make install



# 编译安装nginx
**下载prce包，编译安装时指定包路径prce路径**

```plain
./configure --prefix=/app/nginx --pid-path=/app/nginx/pid/nginx.pid --error-log-path=/app/nginx/logs/error.log --http-log-path=/app/nginx/logs/access.log --with-pcre=/home/wallyt/pcre-8.45 --with-http_realip_module --with-http_ssl_module --with-stream --with-http_stub_status_module --with-file-aio --with-http_realip_module --with-http_gzip_static_module --with-debug --with-threads --with-stream_ssl_preread_module --with-stream_ssl_module --add-module=/app/nginx/nginx_upstream_check_module-master
```



```plain
make && make install
```



# rocky linux 9.x安装 nginx 1.26.3
wget [https://nginx.org/download/nginx-1.26.3.tar.gz](https://nginx.org/download/nginx-1.26.3.tar.gz)

tar xf 1.26.3.tar.gz

mkdir /app/nginx

cd xx.1.26.3

安装缺失的包

```plain
dnf install -y pcre-devel
```

预编译

```plain
./configure --prefix=/app/nginx --sbin-path=/app/nginx/bin/nginx --conf-path=/app/nginx/conf/nginx.conf --error-log-path=/app/nginx/logs/error.log --http-log-path=/app/nginx/logs/access.log --pid-path=/app/nginx/logs/nginx.pid --http-client-body-temp-path=/app/nginx/temp/client_body --http-proxy-temp-path=/app/nginx/temp/proxy --http-fastcgi-temp-path=/app/nginx/temp/fastcgi --http-uwsgi-temp-path=/app/nginx/temp/uwsgi --http-scgi-temp-path=/app/nginx/temp/scgi --with-http_ssl_module --with-http_gzip_static_module --with-stream
```



```plain
make && sudo make install
```

# 安装完报错处理
**<font style="color:#DF2A3F;">nginx: [emerg] mkdir() "/app/nginx/temp/client_body" failed (2: No such file or directory)</font>**

**<font style="color:#DF2A3F;">nginx: configuration file /app/nginx/conf/nginx.conf test failed</font>**

**<font style="color:#DF2A3F;">编译安装的nginx 需要手动创建必要文件夹</font>**

```plain
[root@localhost nginx]# mkdir -p /app/nginx/temp/{client_body,proxy,fastcgi}
```



# rock linux 9.x安装 jdk 11
下载jdk 11二进制包



配置环境变量

JAVA_HOME=/opt/java

PATH=/root/.local/bin:/root/bin:/opt/java/bin:/sbin:/bin:/usr/sbin:/usr/bin

OLDPWD=/opt/java





# 海付测试 环境nginx编译参数


 ./configure --prefix=/app/nginx --sbin-path=/app/nginx/bin/nginx --conf-path=/app/nginx/conf/nginx.conf --error-log-path=/app/nginx/logs/error.log --http-log-path=/app/nginx/logs/access.log --pid-path=/app/nginx/logs/nginx.pid --http-client-body-temp-path=/app/nginx/temp/client_body --http-proxy-temp-path=/app/nginx/temp/proxy --http-fastcgi-temp-path=/app/nginx/temp/fastcgi --http-uwsgi-temp-path=/app/nginx/temp/uwsgi --http-scgi-temp-path=/app/nginx/temp/scgi --with-http_ssl_module --with-http_gzip_static_module --with-stream --with-stream_ssl_preread_module --with-http_realip_module







> 更新: 2026-04-03 11:34:40  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gq9q7m8r6lt6596i>