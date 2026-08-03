# AlmaLinx8.10迁移升级到AlmaLinux9.7

<https://wiki.almalinux.org/elevate/ELevate-offline-guide.html#migrate-almalinux-8-to-almalinux-9>

文档里有个坑，在alma 8.10里直接yum安装leapp-upgrade leapp-data-almalinux会报错找不到，

yum install -y leapp-upgrade leapp-data-almalinux

解决方法 需要先安装yum 源

yum install -y \[http://repo.almalinux.org/elevate/elevate-release-latest-el$(rpm]\(http://repo.almalinux.org/elevate/elevate-release-latest-el$(rpm) --eval %rhel).noarch.rpm

sudo leapp preupgrade 执行报错

![1768472437434-74dca20a-300d-40cd-8de8-4ffe09877e05.png](./img/w6UbR5HMKtHDZ5nH/1768472437434-74dca20a-300d-40cd-8de8-4ffe09877e05-815670.png)

原因 Nework 静态文件写错了

<font style="color:rgb(6, 10, 38);">静态文件内容 </font>**<font style="color:rgb(6, 10, 38);">缺少了最开头的 </font>**<code>**<font style="color:rgb(6, 10, 38);">[connection]</font>**</code>**<font style="color:rgb(6, 10, 38);"> 小节</font>**<font style="color:rgb(6, 10, 38);">，这是导致 Leapp 报错的根本原因。</font>

***

:::danger
id=ens192

uuid=dbc8cbeb-f436-4a21-963d-90eba6cf1dd5

type=ethernet

interface-name=ens192

:::

\============================================================

```
                  REPORT OVERVIEW
```

\============================================================

修改完上述错误，和禁止root直接ssh登录之后，还有一个报错阻止了升级

:::danger
**<font style="color:#DF2A3F;">Upgrade has been inhibited due to the following problems:</font>**

**<font style="color:#DF2A3F;">    1. Newest installed kernel not in use</font>**

Reports summary:

```
Errors:                      0

Inhibitors:                  1

HIGH severity reports:       0

MEDIUM severity reports:     0

LOW severity reports:        2

INFO severity reports:       2
```

Before continuing, review the full report below for details about discovered problems and possible remediation instructions:

```
A report has been generated at /var/log/leapp/leapp-report.txt

A report has been generated at /var/log/leapp/leapp-report.json
```

:::

我之前因为上面的Network报错，执行了dnf upgrade,不应该执行upgrade的！！现在有两个内核版本，要求我用最新的才能继续操作迁移升级。

```plain
[root@localhost wftapp]# rpm -q kernel
kernel-4.18.0-553.el8_10.x86_64
kernel-4.18.0-553.92.1.el8_10.x86_64
```

修改默认内核并重启

```plain
sudo grubby --set-default /boot/vmlinuz-4.18.0-553.92.1.el8_10.x86_64
grubby --default-kernel
/boot/vmlinuz-4.18.0-553.92.1.el8_10.x86_64
reboot
```


> 更新: 2026-01-15 19:19:01  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xxsecz1cl1ypbcyt>