# containerd 名令 ctr（原生 CLI）和 crictl

### <font style="color:rgba(0, 0, 0, 0.9);">一、常用工具对比

一、常用工具对比</font> <font style="color:rgba(0, 0, 0, 0.9);">containerd 提供</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">ctr</font></code><font style="color:rgba(0, 0, 0, 0.9);">（原生 CLI）和</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">crictl</font></code><font style="color:rgba(0, 0, 0, 0.9);">（Kubernetes CRI 工具）两种镜像管理工具，区别如下：</font><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">containerd 提供ctr（原生 CLI）和crictl（Kubernetes CRI 工具）两种镜像管理工具，区别如下：</font>

| **<font style="color:rgba(0, 0, 0, 0.9);">功能</font>** | <code>**<font style="color:rgba(0, 0, 0, 0.9);">ctr</font>**</code><br/>**<font style="color:rgba(0, 0, 0, 0.9);"> </font>\*\*\*\*<font style="color:rgba(0, 0, 0, 0.9);">命令</font>** | <code>**<font style="color:rgba(0, 0, 0, 0.9);">crictl</font>**</code><br/>**<font style="color:rgba(0, 0, 0, 0.9);"> </font>\*\*\*\*<font style="color:rgba(0, 0, 0, 0.9);">命令（K8s 环境）</font>** |
| :--- | :--- | :--- |
| <font style="color:rgba(0, 0, 0, 0.9);">查看镜像列表</font> | <code><font style="color:rgba(0, 0, 0, 0.9);">ctr images list</font></code> | <code><font style="color:rgba(0, 0, 0, 0.9);">crictl images</font></code> |
| <font style="color:rgba(0, 0, 0, 0.9);">拉取镜像</font> | <code><font style="color:rgba(0, 0, 0, 0.9);">ctr images pull <镜像名></font></code> | <code><font style="color:rgba(0, 0, 0, 0.9);">crictl pull <镜像名></font></code> |
| <font style="color:rgba(0, 0, 0, 0.9);">删除镜像</font> | <code><font style="color:rgba(0, 0, 0, 0.9);">ctr images remove <镜像名></font></code> | <code><font style="color:rgba(0, 0, 0, 0.9);">crictl rmi <镜像名></font></code> |
| <font style="color:rgba(0, 0, 0, 0.9);">导出镜像</font> | <code><font style="color:rgba(0, 0, 0, 0.9);">ctr images export <tar路径></font></code> | <font style="color:rgba(0, 0, 0, 0.9);">不支持</font> |
| <font style="color:rgba(0, 0, 0, 0.9);">导入镜像</font> | <code><font style="color:rgba(0, 0, 0, 0.9);">ctr images import <tar路径></font></code> | <font style="color:rgba(0, 0, 0, 0.9);">不支持</font> |
| **<font style="color:rgba(0, 0, 0, 0.9);">适用场景</font>** | <font style="color:rgba(0, 0, 0, 0.9);">通用容器管理</font> | <font style="color:rgba(0, 0, 0, 0.9);">专为 Kubernetes 设计，需指定命名空间（如</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">-n k8s.io</font></code><br/><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">）</font> |

***

### <font style="color:rgba(0, 0, 0, 0.9);">二、镜像生命周期管理</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1. 基础操作</font><font style="color:rgba(0, 0, 0, 0.9);">

</font><font style="color:rgba(0, 0, 0, 0.9);">1. 基础操作</font>

* **<font style="color:rgba(0, 0, 0, 0.9);">拉取镜像</font>**

```plain
bash

复制
ctr images pull docker.io/library/nginx:alpine   # 完整格式 
ctr images pull nginx:alpine                    # 简写（默认使用docker.io ）
```

* **<font style="color:rgba(0, 0, 0, 0.9);">查看镜像</font>**

```plain
bash

复制
ctr images list                          # 列出所有镜像 
ctr images list | grep nginx            # 过滤镜像 
ctr images check                        # 检测镜像完整性[2]()
```

* **<font style="color:rgba(0, 0, 0, 0.9);">删除镜像</font>**

```plain
bash

复制
ctr images remove docker.io/library/nginx:alpine
```

* **<font style="color:rgba(0, 0, 0, 0.9);">镜像标记与推送</font>**

```plain
bash

复制
ctr images tag nginx:alpine my-registry.com/nginx:v1   # 重命名 
ctr images push my-registry.com/nginx:v1              # 推送至私有仓库[5]()
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 镜像导入与导出</font>

* **<font style="color:rgba(0, 0, 0, 0.9);">导出镜像为 TAR 包</font>**

```plain
bash

复制
ctr images export nginx.tar  docker.io/library/nginx:alpine
```

* **<font style="color:rgba(0, 0, 0, 0.9);">从 TAR 包导入镜像</font>**

```plain
bash

复制
ctr images import nginx.tar           # 自动解析镜像名 
ctr images import --base-name myapp myapp.tar   # 指定名称[10]()
```

***

### <font style="color:rgba(0, 0, 0, 0.9);">三、高级操作</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1. 多平台镜像管理</font>

* **<font style="color:rgba(0, 0, 0, 0.9);">指定平台拉取</font>**

```plain
bash

复制
ctr images pull --platform linux/arm64 nginx:alpine  # 拉取 ARM 架构镜像 
ctr images pull --all-platforms nginx:alpine         # 拉取所有平台镜像[6]()
```

* **<font style="color:rgba(0, 0, 0, 0.9);">挂载镜像内容</font>**

```plain
bash

复制
ctr images mount nginx:alpine /mnt/nginx  # 挂载到本地目录 
ctr images unmount /mnt/nginx            # 卸载
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 私有仓库配置</font>

* **<font style="color:rgba(0, 0, 0, 0.9);">非安全仓库</font>**<font style="color:rgba(0, 0, 0, 0.9);">：编辑</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">/etc/containerd/config.toml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">，添加：</font>

```plain
toml

复制
[plugins."io.containerd.grpc.v1.cri".registry] 
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors] 
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."my-registry.com"] 
      endpoint = ["http://my-registry.com:5000"]
```

<font style="color:rgba(0, 0, 0, 0.9);">重启服务：</font><code><font style="color:rgba(0, 0, 0, 0.9);">systemctl restart containerd</font></code><font style="color:rgba(0, 0, 0, 0.9);">。</font>

* **<font style="color:rgba(0, 0, 0, 0.9);">认证配置</font>**<font style="color:rgba(0, 0, 0, 0.9);">：通过</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">ctr auth login</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">登录私有仓库：</font>

```plain
bash

复制
ctr auth login -u <用户名> -p <密码> my-registry.com
```

<font style="color:rgb(0, 0, 0);"></font>

# <font style="color:rgba(0, 0, 0, 0.9);">在 containerd 中，</font><code><font style="color:rgba(0, 0, 0, 0.9);">ctr</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 和 </font><code><font style="color:rgba(0, 0, 0, 0.9);">crictl</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 默认操作不同的命名空间（</font><code><font style="color:rgba(0, 0, 0, 0.9);">crictl</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 管理 </font><code><font style="color:rgba(0, 0, 0, 0.9);">k8s.io</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 命名空间的镜像，而 </font><code><font style="color:rgba(0, 0, 0, 0.9);">ctr</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 默认操作 </font><code><font style="color:rgba(0, 0, 0, 0.9);">default</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 命名空间），因此需通过以下步骤管理 </font><code><font style="color:rgba(0, 0, 0, 0.9);">crictl</font></code><font style="color:rgba(0, 0, 0, 0.9);"> 拉取的镜像并修改标签：</font>

***

### <font style="color:rgba(0, 0, 0, 0.9);">1.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">查看镜像所在的命名空间</font>**

```plain
bash

复制
crictl images                     # 查看 k8s.io  命名空间下的镜像（crictl 默认操作 k8s.io ）
ctr -n k8s.io  images list        # 通过 ctr 查看 k8s.io  命名空间的镜像
```

***

### <font style="color:rgba(0, 0, 0, 0.9);">2.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">修改镜像标签（Tag）</font>**

<font style="color:rgba(0, 0, 0, 0.9);">使用</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">ctr</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">命令时需指定</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">-n k8s.io</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">以操作</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">crictl</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">拉取的镜像，并强制覆盖旧标签（若存在）：</font>

```plain
bash

复制
# 格式：ctr -n k8s.io  images tag <原镜像名> <新镜像名>
ctr -n k8s.io  images tag docker.io/grafana/grafana:11.5.2  my-registry.com/grafana:v11.5.2  --force
```

* **<font style="color:rgba(0, 0, 0, 0.9);">关键参数</font>**<font style="color:rgba(0, 0, 0, 0.9);">：</font>
  * <code><font style="color:rgba(0, 0, 0, 0.9);">-n k8s.io</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">：指定命名空间（必须与</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">crictl</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">的镜像存储空间一致）。</font>
  * <code><font style="color:rgba(0, 0, 0, 0.9);">--force</font></code><font style="color:rgba(0, 0, 0, 0.9);">：若新标签已存在，强制覆盖。</font>

***

### <font style="color:rgba(0, 0, 0, 0.9);">3.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">验证标签修改</font>**

```plain
bash

复制
ctr -n k8s.io  images list | grep grafana  # 检查新标签是否生效
```

***

### <font style="color:rgba(0, 0, 0, 0.9);">4.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">推送镜像到私有仓库（可选）</font>**

```plain
bash

复制
ctr -n k8s.io  images push my-registry.com/grafana:v11.5.2
```


> 更新: 2025-04-03 14:35:05  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xaex0ggcf13i7m4k>