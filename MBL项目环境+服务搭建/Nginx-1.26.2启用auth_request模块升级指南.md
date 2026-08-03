# Nginx 1.26.2 启用 auth_request 模块升级指南

## 1. 升级目标

当前 Nginx 信息：

```text
nginx version: nginx/1.26.2
prefix: /app/nginx
```

当前编译参数中没有 `--with-http_auth_request_module`，因此不能使用 `auth_request` 和 `auth_request_set` 指令。

本次升级保持 Nginx 版本和原有编译参数不变，只增加：

```text
--with-http_auth_request_module
```

`auth_request` 属于 Nginx 源码内置的可选模块，不需要另外下载模块源码，但必须重新编译 Nginx 二进制。

## 2. 变更风险和注意事项

1. 必须使用与当前运行版本完全一致的 Nginx `1.26.2` 源码。
2. 必须保留原有第三方模块 `nginx_upstream_check_module-master`，否则现有配置可能出现 `unknown directive`。
3. 必须确认 `/home/wallyt/pcre-8.45` 和第三方模块源码目录仍然存在。
4. 编译完成后不要直接执行 `make install`，避免覆盖配置和安装目录中的其他文件。
5. 替换 Nginx 二进制后，普通 `reload` 不会让旧 master 进程加载新模块。必须重启 Nginx，或执行平滑二进制升级。
6. 变更前应安排维护窗口，并确认有主机登录权限和回滚条件。

## 3. 变更前检查

### 3.1 确认当前版本和编译参数

```bash
/app/nginx/sbin/nginx -V 2>&1
```

保存输出，便于与新二进制进行对比：

```bash
/app/nginx/sbin/nginx -V 2>&1 \
  > /app/nginx/nginx-build-before-auth-request.txt
```

### 3.2 检查相关源码目录

```bash
ls -ld /home/wallyt/pcre-8.45
ls -ld /app/nginx/nginx_upstream_check_module-master
```

如果任何目录不存在，应先找回原编译使用的源码。不要临时移除对应参数。

### 3.3 检查当前配置和进程

```bash
/app/nginx/sbin/nginx -t
ps -ef | grep '[n]ginx'
cat /app/nginx/pid/nginx.pid
```

### 3.4 检查磁盘空间

```bash
df -h /app /home/wallyt
```

## 4. 准备 Nginx 1.26.2 源码

如果原来的 `nginx-1.26.2` 源码目录仍然存在，可以直接使用。否则重新下载：

```bash
cd /home/wallyt
curl -fLO https://nginx.org/download/nginx-1.26.2.tar.gz
tar -xzf nginx-1.26.2.tar.gz
cd /home/wallyt/nginx-1.26.2
```

确认源码版本：

```bash
grep '#define NGINX_VERSION' src/core/nginx.h
```

预期包含：

```text
#define NGINX_VERSION      "1.26.2"
```

## 5. 重新编译 Nginx

### 5.1 清理旧的编译结果

仅在 Nginx 源码目录中执行：

```bash
cd /home/wallyt/nginx-1.26.2
make clean 2>/dev/null || true
```

### 5.2 执行 configure

以下参数来自当前 `nginx -V` 输出。原参数中 `--with-http_realip_module` 重复出现，本次保留一次即可。

```bash
./configure \
  --prefix=/app/nginx \
  --pid-path=/app/nginx/pid/nginx.pid \
  --error-log-path=/app/nginx/logs/error.log \
  --http-log-path=/app/nginx/logs/access.log \
  --with-pcre=/home/wallyt/pcre-8.45 \
  --with-http_realip_module \
  --with-http_ssl_module \
  --with-stream \
  --with-http_stub_status_module \
  --with-file-aio \
  --with-http_gzip_static_module \
  --with-debug \
  --with-threads \
  --with-stream_ssl_preread_module \
  --with-stream_ssl_module \
  --with-http_auth_request_module \
  --add-module=/app/nginx/nginx_upstream_check_module-master
```

检查 `configure` 最终输出中的安装路径是否仍然指向 `/app/nginx`。

### 5.3 编译

```bash
make -j"$(nproc)"
```

不要执行：

```bash
make install
```

编译生成的新二进制位于：

```text
/home/wallyt/nginx-1.26.2/objs/nginx
```

## 6. 验证新二进制

### 6.1 检查版本和模块

```bash
cd /home/wallyt/nginx-1.26.2
./objs/nginx -V 2>&1
./objs/nginx -V 2>&1 | grep -- '--with-http_auth_request_module'
```

第二条命令必须能够匹配到：

```text
--with-http_auth_request_module
```

### 6.2 使用新二进制检查现有配置

```bash
./objs/nginx -t -p /app/nginx/ -c conf/nginx.conf
```

预期输出：

```text
syntax is ok
test is successful
```

如果出现 `unknown directive`，尤其是 upstream 健康检查相关指令，说明第三方模块没有正确编译。此时禁止替换生产二进制。

### 6.3 可选：提前验证 auth_request 指令

可以先将计划使用的 `auth_request` 配置加入 Nginx 配置文件，然后仅使用新二进制检查：

```bash
./objs/nginx -t -p /app/nginx/ -c conf/nginx.conf
```

注意：在新二进制正式生效前，不要使用旧 Nginx 执行 reload，否则旧 master 会因为不认识 `auth_request` 指令而拒绝加载配置。

## 7. 备份并部署新二进制

### 7.1 备份当前文件

```bash
cp -a /app/nginx/sbin/nginx \
  /app/nginx/sbin/nginx-1.26.2-before-auth-request

cp -a /app/nginx/conf \
  /app/nginx/conf-before-auth-request
```

确认备份存在：

```bash
ls -l /app/nginx/sbin/nginx*
ls -ld /app/nginx/conf-before-auth-request
```

### 7.2 将新二进制复制为临时文件

```bash
cp /home/wallyt/nginx-1.26.2/objs/nginx \
  /app/nginx/sbin/nginx.new

chown --reference=/app/nginx/sbin/nginx \
  /app/nginx/sbin/nginx.new

chmod --reference=/app/nginx/sbin/nginx \
  /app/nginx/sbin/nginx.new
```

再次验证临时二进制：

```bash
/app/nginx/sbin/nginx.new -V 2>&1 | grep auth_request
/app/nginx/sbin/nginx.new -t -p /app/nginx/ -c conf/nginx.conf
```

### 7.3 替换磁盘上的 Nginx 二进制

```bash
mv /app/nginx/sbin/nginx /app/nginx/sbin/nginx.old
mv /app/nginx/sbin/nginx.new /app/nginx/sbin/nginx
```

验证：

```bash
/app/nginx/sbin/nginx -V 2>&1 | grep auth_request
/app/nginx/sbin/nginx -t
```

此时只是磁盘上的二进制已替换，正在运行的 master 进程仍然是旧版本代码。必须选择下面一种方式使新二进制生效。

## 8. 使新二进制生效

### 方案 A：维护窗口重启（推荐）

该方式步骤最简单，但会有短暂连接中断。优先使用现有 systemd 服务管理方式。先确认服务名：

```bash
systemctl list-units --type=service | grep -i nginx
```

如果 Nginx 由 `nginx.service` 管理：

```bash
systemctl restart nginx
systemctl status nginx --no-pager
```

如果没有 systemd 服务，使用 Nginx 自身命令：

```bash
/app/nginx/sbin/nginx -s quit

# 确认旧进程已经退出后再启动
ps -ef | grep '[n]ginx'
/app/nginx/sbin/nginx
```

不要在旧进程尚未退出时重复启动。

### 方案 B：平滑二进制升级

该方式可以尽量避免中断，但操作比重启复杂。执行前必须完成新二进制和配置检查。

#### 8.1 记录旧 master PID

```bash
OLD_MASTER_PID=$(cat /app/nginx/pid/nginx.pid)
echo "$OLD_MASTER_PID"
ps -fp "$OLD_MASTER_PID"
```

#### 8.2 启动新 master

向旧 master 发送 `USR2`：

```bash
kill -USR2 "$OLD_MASTER_PID"
```

检查 PID 文件和进程：

```bash
ls -l /app/nginx/pid/nginx.pid*
cat /app/nginx/pid/nginx.pid
cat /app/nginx/pid/nginx.pid.oldbin
ps -ef | grep '[n]ginx'
tail -n 100 /app/nginx/logs/error.log
```

正常情况下：

- `/app/nginx/pid/nginx.pid` 是新 master PID；
- `/app/nginx/pid/nginx.pid.oldbin` 是旧 master PID；
- 新旧 worker 会在短时间内同时存在。

如果没有生成 `.oldbin` PID 文件，或者 error log 出现启动失败，应停止后续步骤并执行回滚。

#### 8.3 验证新 master

```bash
NEW_MASTER_PID=$(cat /app/nginx/pid/nginx.pid)
echo "old=$OLD_MASTER_PID new=$NEW_MASTER_PID"
ps -fp "$NEW_MASTER_PID"

curl -I http://127.0.0.1/
```

应根据实际监听端口、域名和 HTTPS 配置修改 `curl` 测试命令。

#### 8.4 让旧 worker 平滑退出

新 master 和业务请求验证正常后：

```bash
kill -WINCH "$OLD_MASTER_PID"
```

检查旧 worker 是否退出、新 worker 是否正常处理请求：

```bash
ps -ef | grep '[n]ginx'
tail -n 100 /app/nginx/logs/error.log
```

#### 8.5 退出旧 master

确认新 master 稳定后：

```bash
kill -QUIT "$OLD_MASTER_PID"
```

最终检查：

```bash
ps -ef | grep '[n]ginx'
cat /app/nginx/pid/nginx.pid
/app/nginx/sbin/nginx -t
```

## 9. 配置 auth_request

以下示例假设：

- 认证服务为 `127.0.0.1:8081/verify`；
- 业务服务为 `127.0.0.1:8080`；
- 客户端通过 `Authorization: Bearer <token>` 传递凭据。

```nginx
upstream auth_backend {
    server 127.0.0.1:8081;
    keepalive 16;
}

upstream application_backend {
    server 127.0.0.1:8080;
    keepalive 32;
}

server {
    listen 443 ssl;
    server_name example.com;

    location / {
        auth_request /_auth;

        # 从认证子请求响应头中获取用户信息，并传递给业务服务。
        auth_request_set $auth_user $upstream_http_x_auth_user;
        proxy_set_header X-Auth-User $auth_user;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_pass http://application_backend;
    }

    location = /_auth {
        # 禁止外部客户端直接访问内部认证地址。
        internal;

        proxy_pass http://auth_backend/verify;

        # 认证子请求通常只需要请求头，不需要原请求体。
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";

        proxy_set_header Authorization $http_authorization;
        proxy_set_header Cookie $http_cookie;
        proxy_set_header X-Original-URI $request_uri;
        proxy_set_header X-Original-Method $request_method;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

认证服务的响应规则：

| 认证响应 | Nginx 行为 |
|---|---|
| `2xx` | 认证通过，继续访问业务 upstream |
| `401` | 返回未认证 |
| `403` | 返回无权限 |
| 其他状态码 | 认证子请求异常，通常返回 `500` |

认证成功后的用户信息应通过响应头传递，例如：

```http
HTTP/1.1 200 OK
X-Auth-User: user-1001
```

## 10. 配置验证和功能测试

### 10.1 检查并重新加载配置

确认新 master 已经生效后执行：

```bash
/app/nginx/sbin/nginx -t
/app/nginx/sbin/nginx -s reload
```

### 10.2 测试未携带认证信息的请求

```bash
curl -kiv https://example.com/
```

预期返回 `401` 或业务定义的未登录响应。

### 10.3 测试携带 Token 的请求

```bash
curl -kiv \
  -H 'Authorization: Bearer test-token' \
  https://example.com/
```

有效 Token 应通过认证并访问业务 upstream；无效 Token 应返回 `401` 或 `403`。

### 10.4 检查日志

```bash
tail -n 200 /app/nginx/logs/error.log
tail -n 200 /app/nginx/logs/access.log
```

排障期间可以为认证子请求单独配置日志：

```nginx
location = /_auth {
    internal;

    access_log /app/nginx/logs/auth_request_access.log;
    error_log /app/nginx/logs/auth_request_error.log info;

    proxy_pass http://auth_backend/verify;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header Authorization $http_authorization;
    proxy_set_header X-Original-URI $request_uri;
}
```

生产稳定后建议将认证错误日志级别恢复为默认值，避免产生过多日志。

## 11. 回滚方案

### 11.1 配置回滚

如果只是 `auth_request` 配置有问题，先恢复配置备份：

```bash
mv /app/nginx/conf /app/nginx/conf-with-auth-request.failed
mv /app/nginx/conf-before-auth-request /app/nginx/conf
```

检查配置：

```bash
/app/nginx/sbin/nginx -t
```

### 11.2 维护窗口二进制回滚

```bash
cp -a /app/nginx/sbin/nginx-1.26.2-before-auth-request \
  /app/nginx/sbin/nginx.rollback

chown --reference=/app/nginx/sbin/nginx \
  /app/nginx/sbin/nginx.rollback

chmod --reference=/app/nginx/sbin/nginx \
  /app/nginx/sbin/nginx.rollback

mv /app/nginx/sbin/nginx /app/nginx/sbin/nginx-with-auth-request.failed
mv /app/nginx/sbin/nginx.rollback /app/nginx/sbin/nginx

/app/nginx/sbin/nginx -t
```

随后通过 systemd 重启，或者停止当前进程后重新启动旧二进制。

### 11.3 平滑升级过程中的快速回退

如果已经执行 `USR2`，但尚未退出旧 master，并且新 master 工作异常，可以执行：

```bash
NEW_MASTER_PID=$(cat /app/nginx/pid/nginx.pid)
OLD_MASTER_PID=$(cat /app/nginx/pid/nginx.pid.oldbin)

# 恢复旧 master 的 worker。
kill -HUP "$OLD_MASTER_PID"

# 平滑退出新 master。
kill -QUIT "$NEW_MASTER_PID"
```

然后恢复旧二进制和不包含 `auth_request` 的配置，并检查 PID 文件及进程状态。

如果旧 master 已执行 `QUIT` 并退出，则不能再使用该快速回退方式，需要按维护窗口回滚旧二进制并重启。

## 12. 变更完成检查表

- [ ] 新旧 Nginx 版本均为 `1.26.2`。
- [ ] 新编译参数包含 `--with-http_auth_request_module`。
- [ ] 原有 `nginx_upstream_check_module-master` 已保留。
- [ ] 新二进制执行现有配置检查成功。
- [ ] 原二进制和配置已经备份。
- [ ] 新 master 进程已经运行，旧 master 已按计划退出。
- [ ] 未认证请求返回预期状态码。
- [ ] 有效认证请求能够正常访问业务 upstream。
- [ ] Nginx error log 没有新增持续性错误。
- [ ] 已确认回滚文件仍然保留。

