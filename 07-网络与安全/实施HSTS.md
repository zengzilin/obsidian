# 实施HSTS

#### **<font style="color:rgb(0, 0, 0) !important;">2. Nginx 服务器</font>**

* **<font style="color:rgb(0, 0, 0) !important;">步骤 1：HTTPS Server 块配置 HSTS</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">\ </font><font style="color:rgba(0, 0, 0, 0.85) !important;">编辑</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">/etc/nginx/sites-available/maxilife</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">，在</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">server { listen 443 ssl; }</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">中添加：</font>**<font style="color:rgba(0, 0, 0, 0.85);">nginx</font>**

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
```

![1753065438440-50e14dd6-7e9f-45b7-803c-9607ea5f45b1.png](./img/mycF1BgLS6SqggD2/1753065438440-50e14dd6-7e9f-45b7-803c-9607ea5f45b1-472380.png)<font style="color:rgba(0, 0, 0, 0.85) !important;">\ </font>

* **<font style="color:rgb(0, 0, 0) !important;">步骤 2：HTTP 重定向（80 端口）</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">\ </font><font style="color:rgba(0, 0, 0, 0.85) !important;">在</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">server { listen 80; }</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">中添加：</font>**<font style="color:rgba(0, 0, 0, 0.85);">nginx</font>**

```nginx
return 301 https://$server_name$request_uri;
```

![1753065438408-2ee6df7c-64bf-446a-b936-bb809f2543b9.png](./img/mycF1BgLS6SqggD2/1753065438408-2ee6df7c-64bf-446a-b936-bb809f2543b9-656682.png)<font style="color:rgba(0, 0, 0, 0.85) !important;">\ </font>

* **<font style="color:rgb(0, 0, 0) !important;">重启 Nginx</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">systemctl restart nginx</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">。</font>


> 更新: 2025-07-21 10:37:58  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/msykmvcm0qfqwstz>