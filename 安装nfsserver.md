# 安装nfs server

<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(27, 31, 35, 0.05);"></font>

# <font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(27, 31, 35, 0.05);">安装 nfs server</font>
```plain
dnf install nfs-utils -y
```

```plain
 systemctl enable --now nfs-server
```



```plain
systemctl status nfs-server
```

# 配置连接地址 目录
```plain
 cat /etc/exports
/home/shared_files 192.168.98.0/24(insecure,rw,async,root_squash)
/home/shared_files 172.10.0.0/16(insecure,rw,async,root_squash)
/home/shared_files 10.168.0.0/16(insecure,rw,async,root_squash)
/home/shared_files 10.1.0.0/16(insecure,rw,async,root_squash)
```

<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(27, 31, 35, 0.05);"></font>

```plain
exportfs -arv
```



> 更新: 2025-08-06 21:53:10  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/oac9p8x4fgc3gywt>