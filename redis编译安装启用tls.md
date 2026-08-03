# redis 编译安装启用tls

# 下载必要包
<font style="color:rgb(0, 0, 0);">sudo dnf install -y openssl-devel gcc wget tar </font>

wget -O redis-7.2.3.tar.gz [https://github.com/redis/redis/archive/refs/tags/7.2.3.tar.gz](https://github.com/redis/redis/archive/refs/tags/7.2.3.tar.gz)

tar  xf redis-7.2.3.tar.gz

cd redis-7.2.3/

# 编译开启tls并安装
<font style="color:rgb(0, 0, 0);">make BUILD_TLS=yes </font>

<font style="color:rgb(0, 0, 0);">sudo make install </font>





> 更新: 2025-08-06 16:47:39  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ggdfmd4zhgzsfnzr>