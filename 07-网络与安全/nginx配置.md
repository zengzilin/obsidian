# nginx配置

<code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">ssl_dhparam</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 指令用于指定一个包含 </font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">Diffie-Hellman (DH) 参数</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">的文件。这个文件是用于在 SSL/TLS 握手过程中，安全地交换密钥，以实现</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">前向保密 (Forward Secrecy)</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">简单来说，它的作用是让客户端（如浏览器）和服务器（你的 Nginx）在不安全的网络中，协商出一个只有它们俩才知道的、临时的会话密钥。</font>

### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">🔐</font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 为什么要用它？</font>**

#### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">1. 实现前向保密 (Forward Secrecy)</font>**

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">这是</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">ssl_dhparam</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">最核心的价值。</font>

* **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">没有前向保密</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：如果攻击者录制了你所有的加密通信，并在未来某一天成功窃取了你的服务器私钥 (</font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">ssl_certificate_key</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">)，他就可以用这个私钥解密你</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">过去所有</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">的通信内容。</font>
* **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">有前向保密</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：即使服务器的私钥在未来被泄露，攻击者也无法解密</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">过去</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">的通信。因为每次会话的密钥都是通过 DH 算法临时生成、用完即弃的，与服务器的长期私钥是分离的。</font>

#### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">2. 增强密钥交换的安全性</font>**

* **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">默认风险</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：如果不配置</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">ssl_dhparam</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，Nginx 可能会使用 OpenSSL 默认的、强度较弱的 DH 参数（例如 1024 位），这在现代计算能力下存在被破解的风险。</font>
* **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">自定义强参数</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：通过</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">ssl_dhparam</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">指令，你可以指定一个自己生成的、强度更高的 DH 参数文件（如 2048 位或更高），从而大大提升密钥交换过程的安全性。</font>

### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">🛠️</font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 如何生成 dhparam.pem 文件？</font>**

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">你可以通过 OpenSSL 工具生成这个文件。在服务器上执行以下命令即可：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
# 生成一个 2048 位的强 DH 参数文件
openssl dhparam -out /app/nginx/conf/ssl/dhparam.pem 2048
```

**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">请注意</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：生成过程会消耗一定的 CPU 资源并花费一些时间，特别是位数越高（如 4096），耗时越长。生成完成后，确保文件路径和权限与你的 Nginx 配置匹配即可。</font>


> 更新: 2026-04-03 11:19:13  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rinfi56o5f19ba4k>