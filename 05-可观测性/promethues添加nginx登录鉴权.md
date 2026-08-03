# promethues添加 nginx 登录鉴权

# 生成 Prometheus & alertmanager密码


:::info
htpasswd -c auth-prom admin

kubectl create secret generic prometheus-basic-auth --from-file=auth=auth-prom -n monitoring

:::

<font style="color:rgb(171, 178, 191);background-color:rgb(40, 44, 52);"></font>



> 更新: 2025-03-21 23:40:14  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/myhq1e7hg41k584g>