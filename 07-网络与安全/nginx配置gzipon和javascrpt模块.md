# nginx配置gzip on和javascrpt模块



# 需求：公司项目新增游戏模块，需要支持请求头压缩
## ’


因为流向是CF->nginx->ingress

所以nginx是作为转发，要配置proxy pass，并且将header  Accept-Encoding 也转发给ingress

 proxy_redirect off;

        proxy_set_header Host  $host;

        proxy_set_header X-Real-IP $remote_addr;

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        proxy_pass [http://192.168.4.63;](http://192.168.4.63;)

        proxy_set_header Accept-Encoding $http_accept_encoding;



## 配置完上面的nginx配置之后，游戏页面还是加载不出来
需要在CF层面上再配置相关策略





> 更新: 2024-10-08 20:48:21  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/iwnbpv8wimo1q4rp>