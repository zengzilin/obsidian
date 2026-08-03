# GCP虚拟机使用ssh key登录

从浏览器登录虚拟机，创建用户，比如testmq。

# 在metadata添加sshkey公钥
创建testmq名下的sshkey

```plain
ssh-keygen -t rsa -f ~/.ssh/testmq -C testmq
```

将公钥复制到GCP compute enginx控制台的元数据下面

![1763628823406-470bfd8c-554c-4778-900c-80edde80083d.png](./img/RhNB9ZwoIk_WmcgE/1763628823406-470bfd8c-554c-4778-900c-80edde80083d-817171.png)

![1763628854849-4d264c2f-5150-43d0-9ca8-8e1f112a9d82.png](./img/RhNB9ZwoIk_WmcgE/1763628854849-4d264c2f-5150-43d0-9ca8-8e1f112a9d82-425006.png)

<font style="color:#DF2A3F;">！！在元数据下面添加sshkey 意味着所有虚拟机都可以凭借同一个私钥登录</font>

[testmq@instance-20251120-034717 .ssh]$ pwd

/home/testmq/.ssh

```plain
$ cat testmq.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC0EIkq6Tkx+XLbDEiRZmvYNokSdp/t4bjNAEstoi4Bb8AKOL46FlzBEZXeGx6+i6P0qd+tBUbYUpB5wttMS8IMtEdFp1eWAw+XAJhNQfuH9m1hfQ4tSSySrZacEpRO8xoPTtm7lwI73oHn4dZ/DI+1QjNKSLK1WB656zbeI9T7iEXkX/nC6YQiuCeKXzz/Y0H4yy8eRZssYMUX9XDvnba4+Os27KN5QunLhcWnpY9vL7KAAigZIDeSt2F6t/MgHNLUWCnSFOLG80WeARHcUpw0gAGOULOHwViPjQOpRqRNHuXWioYeRKwVnkDY7QN6xPyX+TDIU0feGUnPkLqEKO3mFf0h9TeiYLwJR44BOnWcZsTkbEig/m6mgfHZlj0pIGDPTXhRdK9eEC3vBW5ASur3wvR2pTiKHNLen5NV6rER4lrw/NVub+dJiTm3Ln/9WmWxm+ZAfLVBomexr411jakV9cW9f8tCUVwa70+UPlG5YsncJQpxmmazdkRj+VRv2vs= testmq
```



# 单独给某一台机器添加sshkey公钥
![1763628795085-4e5569c3-e89e-4248-953a-2fe3f3235cf3.png](./img/RhNB9ZwoIk_WmcgE/1763628795085-4e5569c3-e89e-4248-953a-2fe3f3235cf3-397662.png)



> 更新: 2025-11-20 16:56:51  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/kzlp6s995ea2uwz6>