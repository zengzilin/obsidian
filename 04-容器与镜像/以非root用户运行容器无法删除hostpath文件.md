# 以非root用户运行容器无法删除hostpath文件

## **<font style="color:rgb(6, 10, 38);">1. 问题背景</font>**

<font style="color:rgb(6, 10, 38);">在 Kubernetes (GKE) 环境中，部署了一个以非 Root 用户 (</font><code><font style="color:rgb(6, 10, 38);">runAsUser: 1001</font></code><font style="color:rgb(6, 10, 38);">) 运行的应用容器。该容器需要删除hostpath的日志文件，但是k8s节点默认是root，导致无法删除</font>

**<font style="color:rgb(6, 10, 38);">核心现象：</font>**

* <font style="color:rgb(6, 10, 38);">当容器以 </font><code><font style="color:rgb(6, 10, 38);">root</font></code><font style="color:rgb(6, 10, 38);"> (UID 0) 运行时，删除文件正常</font>
* <font style="color:rgb(6, 10, 38);">当容器切换到普通用户 (</font><code><font style="color:rgb(6, 10, 38);">UID 1001</font></code><font style="color:rgb(6, 10, 38);">) 运行时，</font><code><font style="color:rgb(6, 10, 38);">不允许删除，因为节点上的文件默认是root属主</font></code>

## 2.解决方案

### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">🚀</font>****<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 路径一：利用</font>****<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font>**<code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">initContainer</font></code>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">以 Root 身份预清理 (最推荐，无需改宿主机)</font>**

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">这是 Kubernetes 的标准做法。我们可以启动一个</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">临时的、拥有 Root 权限的容器</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，在主业务容器启动</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">之前</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">运行，专门用来把权限修好，或者直接删掉文件。</font>

**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">原理</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：Init Container 可以配置为</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">runAsUser: 0</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">(Root)，它有权限修改任何文件。它修完权限后，主容器 (UID 1001) 就能正常删除了。</font>

**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">操作步骤</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：</font><font style="color:rgb(6, 10, 38) !important;background-color:rgba(0, 0, 0, 0);">\ </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">在你的 Deployment YAML 中，添加一个</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">initContainers</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">部分：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dockermanagement
spec:
  template:
    spec:
      # 【新增】初始化容器，用 root 身份运行
      initContainers:
      - name: permission-fixer
        image: busybox # 或者 alpine，任何包含 chmod/chown 的小镜像
        command: ["sh", "-c", "chgrp -R 1001 /tiqmo_logs && chmod -R g+w /tiqmo_logs"]
        securityContext:
          runAsUser: 0       # <--- 关键：强制使用 root
          runAsGroup: 0
          allowPrivilegeEscalation: true # init container 通常允许提权来做初始化工作
        volumeMounts:
        - name: tiqmo-logs-volume # <--- 确保名字和你主容器里的 volumeMounts name 一致
          mountPath: /tiqmo_logs

      containers:
      - name: dockermanagement
        # ... 你的主容器配置 ...
        securityContext:
          runAsUser: 1001
          fsGroup: 1001 # 保留这个，双重保险
        # ...
```

**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">为什么这能行？</font>**

1. <font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">K8s 先启动</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">permission-fixer</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>
2. <font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">它是</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">root</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，所以</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">chgrp</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">和</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">chmod</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">一定会成功</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，无视宿主机的普通用户限制（只要宿主机没锁死 root）。</font>
3. <font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">它把所有文件的组改成</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">1001</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，并赋予组写权限 (</font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">g+w</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">)。</font>
4. <code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">permission-fixer</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">退出。</font>
5. <font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">主容器</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">dockermanagement</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">(UID 1001) 启动。此时文件属于组 1001 且有写权限，你的脚本就能顺利</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">rm</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">了。</font>

**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">⚠️</font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 注意</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：如果集群有严格的 PSP/PSA 策略禁止</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">runAsUser: 0</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，这一步会失败。但大多数内部集群允许 init container 提权。</font>

***

### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">🚀</font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 路径二：直接在宿主机执行删除 (如果你有节点权限)</font>**

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">如果你能登录到 Pod 运行的节点，这是最快的一劳永逸方法。</font>

1. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">找到节点</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
kubectl get pod <pod-name> -o jsonpath='{.spec.nodeName}'
```

2. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">登录该节点</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>
3. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">找到宿主机映射目录</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">\ </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">如果是</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">hostPath</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，找到你挂载的宿主机真实路径（例如</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">/data/tiqmo_logs</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">或</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">/var/lib/kubelet/...</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">）。</font>
4. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">执行删除</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
# 直接删除所有符合条件的 gz 文件
find /path/to/host/tiqmo_logs -name "*.log.gz" -mtime +4 -delete

# 或者修复权限让容器以后能自己删
chgrp -R 1001 /path/to/host/tiqmo_logs
chmod -R g+w /path/to/host/tiqmo_logs
```

5. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">重启 Pod</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>

***

### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">🚀</font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 路径三：侧边栏模式 (Sidecar) 清理 (如果不能用 initContainer)</font>**

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">如果不能改 Deployment 加 initContainer，也不能登宿主机，那就只能</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">再开一个特权 Pod</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">来干脏活。</font>

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">创建一个临时的 Job 或 Pod，配置如下：</font>

* <font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">挂载同样的</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">hostPath</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">(或 PVC)。</font>
* <code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">securityContext.runAsUser: 0</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>
* <font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">命令直接执行</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">find ... -delete</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
apiVersion: batch/v1
kind: Job
metadata:
  name: log-cleaner-root
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: cleaner
        image: busybox
        command: ["sh", "-c", "find /tiqmo_logs -name '*.log.gz' -mtime +4 -delete"]
        securityContext:
          runAsUser: 0 # Root 权限
          allowPrivilegeEscalation: true
        volumeMounts:
        - name: logs
          mountPath: /tiqmo_logs
      volumes:
      - name: logs
        hostPath: 
          path: /tiqmo_logs在宿主机上的真实路径 # <--- 必须填宿主机绝对路径
          type: Directory
```

<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">应用这个 Job (</font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">kubectl apply -f job.yaml</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">)，它会以 Root 身份瞬间删掉所有旧文件，然后退出。之后你的主业务容器虽然还是删不了</font>*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">新生成</font>*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">的文件（除非配合路径一修复权限），但至少当前的积压文件清掉了。</font>

### **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">💡</font>\*\*\*\*<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> 总结建议</font>**

1. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">首选【路径一】(Init Container)</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">\ </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">这是最云原生、最安全的做法。它不依赖宿主机人工操作，且能</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">永久解决</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">未来新文件无法删除的问题。</font>
   * **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">动作</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：修改 Deployment YAML，加入</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">initContainers</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">，用</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">root</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">执行</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">chgrp/chmod</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">。</font>
   * **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">结果</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：主容器启动时，文件权限已修正，脚本中的</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">rm</font></code><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);"> </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">命令将成功执行。</font>
2. **<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">如果路径一被策略拦截</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">：</font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">\ </font><font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">说明集群禁止任何 Root 行为。那你只能走</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">路径二</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">（找运维登宿主机修权限）或</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">路径三</font>**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">（看是否有其他高权限账号能跑 Job）。</font>

**<font style="color:rgb(6, 10, 38);background-color:rgba(0, 0, 0, 0);">请尝试修改 YAML 加入 Init Container，这是解决“我想删文件但我权限不够”的标准架构方案。</font>**

<font style="color:rgb(6, 10, 38);">  
</font>


> 更新: 2026-03-07 04:14:27  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/wgg5gtftkvp8ykzl>