# 创建sftp用户和in目录

### <font style="color:rgba(0, 0, 0, 0.9);">🔧</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">配置步骤</font>**

#### <font style="color:rgba(0, 0, 0, 0.9);">1.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">安装 OpenSSH 服务</font>**

```bash
sudo yum install openssh-server  # CentOS/RHEL 
sudo systemctl start sshd       # 启动服务
sudo systemctl enable sshd      # 设置开机自启
```

<font style="color:rgba(0, 0, 0, 0.9);">验证安装：</font><code><font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(27, 31, 35, 0.05);">sshd -v</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">确保 OpenSSH 版本 ≥4.8p1（支持</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(27, 31, 35, 0.05);">ChrootDirectory</font></code><font style="color:rgba(0, 0, 0, 0.9);">）</font>[<font style="color:rgb(22, 119, 255);">1</font>](https://blog.csdn.net/wbiblem/article/details/72082138)<font style="color:rgba(0, 0, 0, 0.9);">。</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">2.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">创建专用用户与目录</font>**

```bash
sudo useradd -m -s /sbin/nologin sftp-user  # 禁止Shell登录
sudo passwd sftp-user                      # 设置密码 
sudo mkdir -p /sftp_root/in                # 创建根目录及子目录
```

* **<font style="color:rgba(0, 0, 0, 0.9);">关键权限设置</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>

```bash
sudo chown root:root /sftp_root          # 根目录属主必须是root 
sudo chmod 755 /sftp_root                # 权限755或750[1]()
sudo chown sftp-user:sftp-user /sftp_root/in  # 子目录属主为用户 
sudo chmod 770 /sftp_root/in             # 允许用户读写
```

#### <font style="color:rgba(0, 0, 0, 0.9);">3.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">修改 SSH 配置文件 (</font>**<code>**<font style="color:rgba(0, 0, 0, 0.9);background-color:rgba(27, 31, 35, 0.05);">/etc/ssh/sshd_config</font>**</code>**<font style="color:rgba(0, 0, 0, 0.9);">)</font>**

<font style="color:rgba(0, 0, 0, 0.9);">在文件末尾添加：</font>

```plain
Match User sftp-user                       # 针对目标用户
  ChrootDirectory /sftp_root               # 锁定根目录 
  ForceCommand internal-sftp               # 强制仅用SFTP 
  AllowTcpForwarding no                    # 禁用端口转发
  X11Forwarding no                         # 禁用X11[3]()
```

#### <font style="color:rgba(0, 0, 0, 0.9);">4.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">重启服务并验证</font>**

```bash
sudo systemctl restart sshd
sftp -P 22 sftp-user@服务器IP              # 测试连接 
sftp> ls 
in/                                       # 应显示in目录 
sftp> cd in                               # 可进入目录 
sftp> put 本地文件                        # 测试上传
```

# 通过ssh key登录sftp

sftp -P 22 sftp-user@服务器IP              # 测试连接


> 更新: 2025-08-19 20:03:18  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/szkbb0fnf2hm2khf>