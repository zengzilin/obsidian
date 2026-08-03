# AlmaLinux\Rocky 8/9配置网络

<font style="color:rgb(6, 10, 38);">在 AlmaLinux Rocky Linux中配置 IP 地址，通常使用 </font>**<font style="color:rgb(6, 10, 38);">NetworkManager</font>**<font style="color:rgb(6, 10, 38);"> 或传统的 </font>**<font style="color:rgb(6, 10, 38);">network-scripts</font>**<font style="color:rgb(6, 10, 38);">（在较旧版本中）。从 AlmaLinux 8 开始，默认使用 </font>**<font style="color:rgb(6, 10, 38);">NetworkManager + nmcli</font>**<font style="color:rgb(6, 10, 38);"> 或 </font>**<font style="color:rgb(6, 10, 38);">nm-connection-editor</font>**<font style="color:rgb(6, 10, 38);"> 进行网络管理</font>

<font style="color:rgb(6, 10, 38);"></font>

## **<font style="color:rgb(6, 10, 38);">方法一：使用</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">nmcli</font></code>**<font style="color:rgb(6, 10, 38);">（推荐，适用于命令行）</font>**

### **<font style="color:rgb(6, 10, 38);">1. 查看当前连接</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
nmcli connection show
```

<font style="color:rgb(6, 10, 38);">输出类似：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">text</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
NAME    UUID                                  TYPE      DEVICE
ens192  abcdefgh-1234-5678-90ab-cdef12345678  ethernet  ens192
```

<font style="color:rgb(6, 10, 38);">记下连接名称（如</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">ens192</font></code><font style="color:rgb(6, 10, 38);">）。</font>

### **<font style="color:rgb(6, 10, 38);">2. 配置静态 IP（以连接名为</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">ens192</font></code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">为例）</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
sudo nmcli con mod ens192 ipv4.addresses 192.168.1.100/24
sudo nmcli con mod ens192 ipv4.gateway 192.168.1.1
sudo nmcli con mod ens192 ipv4.dns "8.8.8.8,8.8.4.4"
sudo nmcli con mod ens192 ipv4.method manual
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">如果是 DHCP，则设为</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">auto</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
sudo nmcli con mod ens192 ipv4.method auto
```

### **<font style="color:rgb(6, 10, 38);">3. 重启连接使配置生效</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
sudo nmcli con down ens192 && sudo nmcli con up ens192
```

# 使用方法一遇到的问题

almalinux 本来就有一个ens192的网卡，但是没有连上device,没有被NetworkManager接管 如下图

![1768466469367-efbcebe5-f875-4f1a-8d10-57813bfe3833.png](./img/_2sumSZ5vUrSk5ZP/1768466469367-efbcebe5-f875-4f1a-8d10-57813bfe3833-807416.png)

但是我按照方法1的方法添加ipv4地址，一直不生效，DEVICE 一直不生效

GPT说 exsi的网卡配置会有影响，我去修改exsi的网络配置报错如下

:::danger
操作失败! 任务名称	重新配置虚拟机 目标	192.168.4.120(tiqmo 集群模版) 状态	无法连接虚拟设备“ethernet0”

:::

于是我关机修改了ip网段，从4.0改到3.0,再从3.0改回4.0

![1768466627405-43e43116-47f1-4678-a4e6-89bf7f705704.png](./img/_2sumSZ5vUrSk5ZP/1768466627405-43e43116-47f1-4678-a4e6-89bf7f705704-624376.png)

重新开机后查看网卡device，<font style="color:rgb(6, 10, 38);">NetworkManager 已经管理该设备（</font><code><font style="color:rgb(6, 10, 38);">DEVICE: ens192</font></code>

![1768466746848-a9d61c93-6047-461c-809c-deca4e0eb8ff.png](./img/_2sumSZ5vUrSk5ZP/1768466746848-a9d61c93-6047-461c-809c-deca4e0eb8ff-320247.png)

但是ip信息还是没有正确显示，我参考rockylinuix 9.5 配置了静态ip文件，也没用

![1768466814884-15e563cf-2048-46ec-b252-9dea2569a70b.png](./img/_2sumSZ5vUrSk5ZP/1768466814884-15e563cf-2048-46ec-b252-9dea2569a70b-418801.png)

## 结论：

device问题解决之后，还是需要用nmcli命令去配置ip以及重启网络

```plain
sudo nmcli con mod ens192 ipv4.method manual 
sudo nmcli con mod ens192 ipv4.addresses "192.168.4.120/24"
sudo nmcli con mod ens192 ipv4.gateway "192.168.4.1" 、
sudo nmcli con mod ens192 ipv4.dns "8.8.8.8,1.2.4.8"
sudo nmcli con up ens192
```

<font style="color:#DF2A3F;">虽然新建了静态文件配置，但在文件里修改ip没有效果，restart NetworkManager配置也还是没用，Rocky Linux是可以生效的！！</font>

<font style="color:#DF2A3F;">所以Almalinux最靠谱的改ip地址的方法是用命令！！ </font>

```plain
sudo nmcli con mod ens192 ipv4.addresses "192.168.4.120/24"
sudo nmcli con down ens192
sudo nmcli con up ens192
```

# **<font style="color:rgb(6, 10, 38);">方法二：编辑配置文件（传统方式，适用于熟悉 network-scripts 的</font>**

## **<font style="color:rgb(6, 10, 38);">用户）</font>**

<font style="color:rgba(6, 10, 38, 0.7) !important;">⚠️</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 注意：AlmaLinux 8+ 默认不再使用</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">/etc/sysconfig/network-scripts/</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">，但如果你安装了</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">network-scripts</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">包，仍可使用。</font>

### **<font style="color:rgb(6, 10, 38);">1. 安装 network-scripts（如果未安装）</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
sudo dnf install network-scripts -y
```

### **<font style="color:rgb(6, 10, 38);">2. 编辑网卡配置文件（假设网卡为</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">ens192</font></code>**<font style="color:rgb(6, 10, 38);">）</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
sudo vi /etc/sysconfig/network-scripts/ifcfg-ens192
```

<font style="color:rgb(6, 10, 38);">静态 IP 示例内容：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">ini</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
TYPE=Ethernet
BOOTPROTO=none
NAME=ens192
DEVICE=ens192
ONBOOT=yes
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4
```


> 更新: 2026-01-15 17:55:48  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/efvvd5qkh0wks0wa>