# docker自定义data-root数据目录

docker数据默认存在/var/lib/docker目录，现在/var目录空间不够，报错

**<font style="color:#DF2A3F;">target kibana: failed to solve: failed to register layer: open /usr/share/kibana/node\_modules/fast-glob/out/providers/matchers/partial.js: no space left on device</font>**

将默认目录修改到/分区下的/docker目录

#### <font style="color:rgb(0, 0, 0);">永久解决方案（迁移 Docker 存储到 </font><code><font style="color:rgb(0, 0, 0);">/</font></code><font style="color:rgb(0, 0, 0);"> 分区）</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">将 Docker 存储目录迁移到空闲的 </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">/</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 分区，是一劳永逸的办法：</font>

##### <font style="color:rgb(0, 0, 0);">1. 停止 Docker 服务</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
sudo systemctl stop docker
sudo systemctl stop docker.socket  # 部分系统需额外停止 socket
```

##### <font style="color:rgb(0, 0, 0);">2. 迁移现有 Docker 数据到 </font><code><font style="color:rgb(0, 0, 0);">/</font></code>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
# 1. 在 /data 下创建新的 Docker 存储目录
sudo mkdir -p /docker

# 2. 迁移 /var/lib/docker 下的所有数据（保留权限）
sudo rsync -avz /var/lib/docker/ /data/docker/
```

##### <font style="color:rgb(0, 0, 0);">3. 备份原 Docker 目录（避免误删）</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
sudo mv /var/lib/docker /var/lib/docker.old
```

##### <font style="color:rgb(0, 0, 0);">4. 配置 Docker 使用新存储目录</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">创建 / 修改 Docker 配置文件</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">daemon.json</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
sudo vim /etc/docker/daemon.json
```

<font style="color:rgba(0, 0, 0, 0.85) !important;">添加以下内容（指定新的存储根目录）：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">json</font>**

```json
{
  "data-root": "/docker"
}
```

##### <font style="color:rgb(0, 0, 0);">5. 启动 Docker 服务并验证</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
# 启动 Docker
sudo systemctl start docker

# 验证 Docker 状态（确保启动成功）
sudo systemctl status docker

# 验证存储目录是否已切换到 /docker
docker info | grep "Docker Root Dir"
# 输出应显示：Docker Root Dir: /data/docker
```

### <font style="color:rgb(0, 0, 0);">验证与重试</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">完成上述配置后，再次查看 Docker 空间占用：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
docker system df
```


> 更新: 2025-09-19 00:00:47  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/wzxz4ilgccgb2ov8>