# centos 7.9安装 ansible

kubespray 不同版本对应不同版本的ansible

安装python3.10

[https://blog.csdn.net/Bsummer/article/details/140001234](https://blog.csdn.net/Bsummer/article/details/140001234)

<font style="color:rgb(66, 139, 221);background-color:rgb(15, 25, 42);">git clone </font>[<font style="color:rgb(66, 139, 221) !important;">https://gitlab.swifer.co/fbu-public/kubespray.git</font>](https://gitlab.swifer.co/fbu-public/kubespray.git)

<font style="color:rgb(66, 139, 221);background-color:rgb(15, 25, 42);">cd kubespray/</font>

<font style="color:rgb(66, 139, 221);background-color:rgb(15, 25, 42);">切换到 release-2.26</font>

<font style="color:rgb(66, 139, 221);background-color:rgb(15, 25, 42);">git checkout release-2.26</font>

安装ansible等必要依赖

pip3 install -r  requirements.txt 或者

 pip3  install -r requirements.txt -i [http://mirrors.aliyun.com/pypi/simple/](http://mirrors.aliyun.com/pypi/simple/) --trusted-host mirrors.aliyun.com

验证ansible是否安装成功





> 更新: 2025-04-19 15:03:45  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ooxren3eikfa5nxv>