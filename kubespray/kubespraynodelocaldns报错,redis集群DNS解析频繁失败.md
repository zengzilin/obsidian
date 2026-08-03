# kubespray nodelocaldns报错,redis集群DNS解析频繁失败

# nodelocaldns pod频繁重启，报错如下

<font style="color:#DF2A3F;background-color:rgb(235, 245, 255);"> node.kubernetes.io/unschedulable:NoSchedule op=Exists Events: Type Reason Age From Message ---- ------ ---- ---- ------- Normal Killing 55m (x287 over 87d) kubelet Container node-cache failed liveness probe, will be restarted Normal Created 55m (x795 over 103d) kubelet Created container: node-cache Normal Started 55m (x795 over 103d) kubelet Started container node-cache Warning Unhealthy 37m (x3155 over 103d) kubelet Readiness probe failed: Get "http://169.254.25.10:9254/health": context deadline exceeded (Client.Timeout exceeded while awaiting headers) Normal Pulled 26m (x804 over 103d) kubelet Container image "docker.repo.swifer.co/dns/k8s-dns-node-cache:1.22.28" already present on machine Warning BackOff 16m (x10658 over 103d) kubelet Back-off restarting failed container node-cache in pod nodelocaldns-8rtjf\_kube-system(ffc370d6-8c5e-4f28-8a6e-535bd040ffd1) Warning Unhealthy 11m (x3114 over 103d) kubelet Liveness probe failed: Get "http://169.254.25.10:9254/health": context deadline exceeded (Client.Timeout exceeded while awaiting headers)</font>

# 获取当前nodelocaldns ConfigMap

kubectl get  configmap nodelocaldns -o yaml -n kube-system

```plain
data:
  Corefile: |
    tiqmo-dev.cluster.local:53 {
        errors
        cache {
            success 9984 30
            denial 9984 5
        }
        reload
        loop
        bind 169.254.25.10
        forward . 100.96.0.3 {
            force_tcp
        }
        prometheus :9253
        health 169.254.25.10:9254
    }
    in-addr.arpa:53 {
        errors
        cache 30
        reload
        loop
        bind 169.254.25.10
        forward . 100.96.0.3 {
            force_tcp
        }
        prometheus :9253
    }
    ip6.arpa:53 {
        errors
        cache 30
        reload
        loop
        bind 169.254.25.10
        forward . 100.96.0.3 {
            force_tcp
        }
        prometheus :9253
    }
    .:53 {
        errors
        cache 30
        reload
        loop
        bind 169.254.25.10
        forward . /etc/resolv.conf
        prometheus :9253
    }
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"Corefile":"tiqmo-dev.cluster.local:53 {\n    errors\n    cache {\n        success 9984 30\n        denial 9984 5\n    }\n    reload\n    loop\n    bind 169.254.25.10\n    forward . 100.96.0.3 {\n        force_tcp\n    }\n    prometheus :9253\n    health 169.254.25.10:9254\n}\nin-addr.arpa:53 {\n    errors\n    cache 30\n    reload\n    loop\n    bind 169.254.25.10\n    forward . 100.96.0.3 {\n        force_tcp\n    }\n    prometheus :9253\n}\nip6.arpa:53 {\n    errors\n    cache 30\n    reload\n    loop\n    bind 169.254.25.10\n    forward . 100.96.0.3 {\n        force_tcp\n    }\n    prometheus :9253\n}\n.:53 {\n    errors\n    cache 30\n    reload\n    loop\n    bind 169.254.25.10\n    forward . /etc/resolv.conf\n    prometheus :9253\n}\n"},"kind":"ConfigMap","metadata":{"annotations":{},"labels":{"addonmanager.kubernetes.io/mode":"EnsureExists"},"name":"nodelocaldns","namespace":"kube-system"}}
  creationTimestamp: "2025-04-23T03:01:50Z"
  labels:
    addonmanager.kubernetes.io/mode: EnsureExists
  name: nodelocaldns
  namespace: kube-system
  resourceVersion: "1593"
  uid: afdc92d8-f6fe-41e3-a1bf-707df62e4e56
```

# ✅ 关键发现：health 插件配置有误！

你在 tiqmo-dev.cluster.local:53 块中配置了：

corefile

health 169.254.25.10:9254

但 health 插件的正确语法是：

corefile

health \[ADDRESS:]PORT

并且 health 插件必须放在一个独立的 server block 中，或者至少确保它监听的地址能被 kubelet 访问。

更重要的是：health 插件只在它所在的 server block 被“激活”时才启动。

而你的配置中，health 只出现在 tiqmo-dev.cluster.local:53 这个 非通配（non-default） 的 server block 中。

这意味着：

只有当 DNS 查询 明确请求 \*.tiqmo-dev.cluster.local 域名 时，这个 server block 才会被使用。

而 kubelet 发起的健康检查是 HTTP 请求（不是 DNS 查询），它不触发任何 DNS server block。

因此，health 插件实际上根本没有启动！

🔥 这就是 /health 接口无法访问的根本原因！

# 📚 CoreDNS / node-cache 的 health 插件工作机制

health 是一个 全局 HTTP 服务，但它 必须被放置在一个始终“活跃”的 server block 中（通常是 .:53 默认块），或者单独定义。

更常见的做法是：在任意一个 block 中声明 health，它就会启动 HTTP 服务 —— 但前提是该 block 被加载。

然而，在你当前的配置中，由于 health 只绑定在 tiqmo-dev.cluster.local 块，而该块可能未被正确激活为“HTTP 服务载体”，导致健康接口未监听。

💡 实际上，官方推荐将 health 放在 .:53 块中，或至少确保其监听地址可被本地访问。

# ✅ 正确修复方法

✨ 方案一（推荐）：将 health 移到 .:53 块中

修改 nodelocaldns ConfigMap，将 health :9254（注意：不要带 IP）放入默认 server block：

yaml

data:

Corefile: |

```
tiqmo-dev.cluster.local:53 {

    errors

    cache {

        success 9984 30

        denial 9984 5

    }

    reload

    loop

    bind 169.254.25.10

    forward . 100.96.0.3 {

        force_tcp

    }

    prometheus :9253

    # ❌ 移除这里的 health

}

in-addr.arpa:53 {

    errors

    cache 30

    reload

    loop

    bind 169.254.25.10

    forward . 100.96.0.3 {

        force_tcp

    }

    prometheus :9253

}

ip6.arpa:53 {

    errors

    cache 30

    reload

    loop

    bind 169.254.25.10

    forward . 100.96.0.3 {

        force_tcp

    }

    prometheus :9253

}

.:53 {

    errors

    cache 30

    reload

    loop

    bind 169.254.25.10

    forward . /etc/resolv.conf

    prometheus :9253

    health :9254   # ✅ 正确位置：默认块中，监听所有接口的 9254

}
```

📌 注意：

使用 health :9254 而不是 health 169.254.25.10:9254

:9254 表示监听 所有本地接口的 9254 端口（包括 localhost 和 169.254.25.10）

这样 kubelet 通过 <http://169.254.25.10:9254/health> 就能访问到

### **<font style="color:rgb(6, 10, 38);">✅</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 临时方案：直接编辑 Kubernetes 中的 ConfigMap</font>**

<font style="color:rgb(6, 10, 38);">这个操作</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">不会影响业务 Pod</font>**<font style="color:rgb(6, 10, 38);">，且</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">nodelocaldns</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">会自动 reload 配置（因为启用了</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">reload</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">插件）。</font>

***

### **<font style="color:rgb(6, 10, 38);">🔧</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 操作步骤</font>**

#### **<font style="color:rgb(6, 10, 38);">1.</font>****<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">编辑 ConfigMap</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
kubectl edit configmap nodelocaldns -n kube-system
```

#### **<font style="color:rgb(6, 10, 38);">2.</font>****<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">修改 Corefile 内容</font>**

<font style="color:rgb(6, 10, 38);">找到</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">tiqmo-dev.cluster.local:53</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">块，</font>**<font style="color:rgb(6, 10, 38);">删除或注释掉</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">health</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">行</font>**<font style="color:rgb(6, 10, 38);">：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">diff</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
tiqmo-dev.cluster.local:53 {
    errors
    cache {
        success 9984 30
        denial 9984 5
    }
    reload
    loop
    bind 169.254.25.10
    forward . 100.96.0.3 {
        force_tcp
    }
    prometheus :9253
-   health 169.254.25.10:9254
}
```

<font style="color:rgb(6, 10, 38);">然后在</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">.:53</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">块末尾</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">添加</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">health :9254</font>**</code><font style="color:rgb(6, 10, 38);">：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">diff</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
.:53 {
    errors
    cache 30
    reload
    loop
    bind 169.254.25.10
    forward . /etc/resolv.conf
    prometheus :9253
+   health :9254
}
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">✅</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 注意：</font>

* <font style="color:rgba(6, 10, 38, 0.7) !important;">使用</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">health :9254</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">（冒号开头，不带 IP）</font>
* <font style="color:rgba(6, 10, 38, 0.7) !important;">保存退出（</font><code><font style="color:rgb(6, 10, 38);">:wq</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">）</font>

#### **<font style="color:rgb(6, 10, 38);">3.</font>****<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">等待自动 reload（约 10～30 秒）</font>**

<font style="color:rgb(6, 10, 38);">由于 Corefile 中有</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">reload</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">插件，</font><code><font style="color:rgb(6, 10, 38);">nodelocaldns</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">会自动检测 ConfigMap 变化并重载配置，</font>**<font style="color:rgb(6, 10, 38);">无需重启 Pod</font>**<font style="color:rgb(6, 10, 38);">。</font>

***

### **<font style="color:rgb(6, 10, 38);">✅</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 验证临时修复是否生效</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
# 1. 测试健康接口（应在几秒内恢复）
curl http://169.254.25.10:9254/health
# 正常应返回：OK

# 2. 观察 Pod 是否停止重启
kubectl get pod -n kube-system -l k8s-app=nodelocaldns -w

# 3. 在业务 Pod 中测试 Redis 解析
kubectl run -it --rm debug --image=docker.repo.swifer.co/busybox:1.28 --restart=Never -- \
  nslookup redis-redis-cluster-headless.uat-ksa-middleware
```


> 更新: 2026-01-20 17:06:01  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/uge3i52ln39ihvbf>