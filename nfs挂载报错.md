# nfs挂载报错

<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);">Running transaction Preparing : Installing : libtirpc-1.3.3-9.el9.x86\_64 Installing : libnfsidmap-1:2.5.4-34.el9.x86\_64 Running scriptlet: rpcbind-1.2.6-7.el9.x86\_64 Installing : rpcbind-1.2.6-7.el9.x86\_64 Running scriptlet: rpcbind-1.2.6-7.el9.x86\_64 Failed to preset unit: Unit file /etc/systemd/system/rpcbind.service is masked.</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">错误提示</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;background-color:rgba(0, 0, 0, 0);">Failed to preset unit: Unit file /etc/systemd/system/rpcbind.service is masked</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">表明</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;background-color:rgba(0, 0, 0, 0);">rpcbind.service</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">被系统</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0) !important;background-color:rgba(0, 0, 0, 0);">屏蔽（masked）</font>**<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">了，导致无法正常安装或启动。这是系统级别的保护机制，会阻止被屏蔽的服务启动。</font>

### <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">解决步骤：</font>

#### <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">1. 解除</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">rpcbind.service</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">的屏蔽</font>

**<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0);">bash</font>**

```bash
sudo systemctl unmask rpcbind.service
```

* <code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">mask</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">会将服务文件链接到</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">/dev/null</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">，彻底禁用服务；</font><code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">unmask</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">会恢复服务文件，允许其正常启动。</font>

#### <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">2. 重新安装或配置</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">rpcbind</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">（确保服务文件正常）</font>

<font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">如果是在安装过程中出现的错误，解除屏蔽后重新安装相关包：</font>

**<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0);">bash</font>**

```bash
sudo dnf reinstall rpcbind libtirpc libnfsidmap
```

#### <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">3. 启动并启用</font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">rpcbind</font></code><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">服务</font>

**<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0);">bash</font>**

```bash
# 启动服务
sudo systemctl start rpcbind

# 检查状态（确保为 active (running)）
sudo systemctl status rpcbind

# 设置开机自启
sudo systemctl enable rpcbind
```


> 更新: 2025-11-08 12:59:44  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/kzlh8gy559bevm8x>