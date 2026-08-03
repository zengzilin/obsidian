# ssh秘钥登录sftp

### <font style="color:rgb(6, 6, 7);">1. 准备 SSH 密钥对</font>

```bash
ssh-keygen -t ed25519 -f ssh_host_ed25519_key < /dev/null





ssh-keygen -t rsa -b 4096 -f ssh_host_rsa_key < /dev/null





```

### <font style="color:rgb(6, 6, 7);">2. 准备 SSH 公钥</font>

```plain
ssh-keygen -t rsa -b 2048     
```

<font style="color:rgb(6, 6, 7);">然后，将公钥复制到一个目录中,如</font>

/home/foo/id\_rsa.pub

### <font style="color:rgb(6, 6, 7);">3. 运行 SFTP 容器</font>

docker run     -v /home/foo/ssh\_host\_ed25519\_key:/etc/ssh/ssh\_host\_ed25519\_key     -v /home/foo/ssh\_host\_rsa\_key:/etc/ssh/ssh\_host\_rsa\_key   -v /home/foo/id\_rsa.pub:/home/foo/.ssh/keys/id\_rsa.pub:ro  -v /home/foo/share:/home/foo/share     -p 2222:22 -d atmoz/sftp     foo::1001

### <font style="color:rgb(6, 6, 7);">4. 登录到 SFTP</font>

<font style="color:rgb(6, 6, 7);">在容器启动并运行后，您可以使用以下命令通过 SSH 密钥登录到 SFTP：</font>

```bash
sftp -oPort=2222 foo@localhost
```

<font style="color:rgb(6, 6, 7);">这里，</font>`foo`<font style="color:rgb(6, 6, 7);"> 是容器内的用户，</font>`localhost`<font style="color:rgb(6, 6, 7);"> 是宿主机的地址，</font>`2222`<font style="color:rgb(6, 6, 7);"> 是您映射到宿主机的端口。</font>

### <font style="color:rgb(6, 6, 7);">5. 处理文件权限</font>

```bash
[foo@kubespray ~]$ ll /home/foo/.ssh/id_rsa
-rw------- 1 foo foo 1675 Dec 24 11:36 /home/foo/.ssh/id_rsa

```


> 更新: 2024-12-24 13:50:50  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/wcg3tnbzutvv85cr>