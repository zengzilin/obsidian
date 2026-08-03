# gitlab更新域名证书后gitlab仓库不可用

# 拉取镜像报证书校验失败
![1755151617719-d8f0d2da-451c-455c-a829-42203ea65f10.png](./img/mpCUzBartjhrReqZ/1755151617719-d8f0d2da-451c-455c-a829-42203ea65f10-038664.png)

登录也报错

![1755151700123-43eabbd8-ec2e-4937-a2d1-54aef0eab7f9.png](./img/mpCUzBartjhrReqZ/1755151700123-43eabbd8-ec2e-4937-a2d1-54aef0eab7f9-417922.png)

# 解决方法
:::info
更新证书后需要重新加载gitlab配置，重启服务

:::

```plain
[tiqmokwadmin@cin-tiq-ew1-p-git-01 star.tiqmopaymentkuwait.com]$ docker exec -it b88e50c4159d /bin/bash
root@kw-prod-git:/# gitlab-ctl reconfigure
gitlab-ctl restart nginx
gitlab-ctl restart registry
```





> 更新: 2025-08-14 14:13:23  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/nu5l4rs08sv5maa6>