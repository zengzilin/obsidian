# GCP 方式部署的rabbitmq集群启用tls

# 1) 生成证书（示例 — 在本地或 bastion 上执行）

下面示例用自签 CA 来演示：生产环境请使用受信任 CA（或使用 cert-manager + Google CA）。注意 SAN 要包含外部访问域名 / LoadBalancer IP、以及 Kubernetes 服务 DNS 名称（如 `rabbitmq.rabbitmq.svc.cluster.local`）以免证书校验失败。

```plain
  openssl genrsa -out ca.key 4096
  openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650   -out ca.crt -subj "/CN=MyRabbitCA"
  openssl genrsa -out tls.key 4096
  openssl genrsa -out server.key 2048
  openssl req -new -key server.key -out server.csr -subj "/CN=rabbitmq"
  openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key   -CAcreateserial -out server.crt -days 365 -sha256 

```

**客户端证书（示例）**（每个客户端真机/应用分发独立 client cert）：

```plain
openssl genrsa -out client.key 2048
openssl req -new -key client.key -subj "/CN=my-app-client" -out client.csr
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out client.crt -days 365 -sha256
# 将 client.crt + client.key 发给客户端（安全传递）
```

***

# 2) 在 Kubernetes 中创建 tls Secrets

把 server.crt、server.key、ca.crt 上载为 Secret（namespace `rabbitmq`）：

```plain
kubectl create secret generic rabbitmq-tls --from-file=ca.crt=./ca.crt --from-file=tls.crt=./server.crt  --from-file=tls.key=./server.key
kubectl create secret tls rabbitmq-tls   --cert=./server.crt   --key=./server.key
kubectl patch secret rabbitmq-tls   --type=json   -p='[{"op": "add", "path": "/data/ca.crt", "value": "'$(base64 -w0 ca.crt)'"}]'
```

只有tls类型的secret才能被x509 exporter监控

***

# 3) 创建 rabbitmq.conf（ConfigMap）：启用 TLS 并强制客户端证书验证

这是 `rabbitmq.conf` 的关键段（在 Pod 内会挂载到 `/etc/rabbitmq/rabbitmq.conf`）：

```plain
apiVersion: v1
kind: ConfigMap
metadata:
  name: rabbitmq-config
  namespace: rabbitmq
data:
  rabbitmq.conf: |
    ## AMQP over TLS
    listeners.ssl.default = 5671

    # 指向挂载后的证书路径（pod 内）
    ssl_options.cacertfile = /etc/rabbitmq/ssl/ca.crt
    ssl_options.certfile   = /etc/rabbitmq/ssl/server.crt
    ssl_options.keyfile    = /etc/rabbitmq/ssl/server.key

    # 要求对等端（客户端）证书验证
    ssl_options.verify = verify_peer
    ssl_options.fail_if_no_peer_cert = true

    # 如需禁用非 TLS 监听（强制仅 TLS）
    listeners.tcp = none

    # 管理插件（HTTP 管理 UI）若也需要 TLS，可类似配置管理插件的 ssl 端口
    management.tls.port = 15671
    management.tls.cacertfile = /etc/rabbitmq/ssl/ca.crt
    management.tls.certfile   = /etc/rabbitmq/ssl/server.crt
    management.tls.keyfile    = /etc/rabbitmq/ssl/server.key
    management.tls.verify = verify_peer
    management.tls.fail_if_no_peer_cert = true
```

<font style="color:#DF2A3F;">更新config报错 kubectl replace -f configmap.yaml</font>

<font style="color:#DF2A3F;">The ConfigMap "rabbitmq-1-rabbitmq-config" is invalid: metadata.ownerReferences.uid: Invalid value: "": uid must not be empty</font>

**<font style="color:#DF2A3F;">解决方案：</font>**

你可以把 export 的 configmap.yaml 里面整个 ownerReferences 删掉：

```plain
metadata:
  name: rabbitmq-1-rabbitmq-config
  namespace: default
  # 删除整个 ownerReferences:
  # ownerReferences: []
```

删掉之后再 apply：

```plain
kubectl apply -f configmap.yaml
```

***

# 4) 把 Secret 挂载进 Pod（示例：StatefulSet / Deployment patch）

下面示例展示通过打补丁的方式添加secret挂载，

```plain
kubectl patch sts rabbitmq-1-rabbitmq --type=json --patch-file=mq-tls.json
```

```plain
[
  {
    "op": "add",
    "path": "/spec/template/spec/volumes/-",
    "value": {
      "name": "rabbitmq-tls",
      "secret": {
        "secretName": "rabbitmq-tls"
      }
    }
  },
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/volumeMounts/-",
    "value": {
      "name": "rabbitmq-tls",
      "mountPath": "/etc/rabbitmq/certs",
      "readOnly": true
    }
  }
]

```

如果你使用 Click-to-Deploy 的 manifest（通常是 `deployment.yaml` / `statefulset.yaml`），直接把上面 `volumes` / `volumeMounts` 加入对应 container 即可。注意：`secret` 里默认 key 名为 `tls.crt` / `tls.key` / `ca.crt`，挂载后就可以按上面 `rabbitmq.conf` 指定路径使用。

***

# 5）登录 mq console，查看5671端口是否生效

***

![1763634078218-6bd495b2-cd20-43e4-8899-40638b57fe9b.png](./img/ZnD53yzXZfVyb_Nb/1763634078218-6bd495b2-cd20-43e4-8899-40638b57fe9b-371359.png)

# 6) 客户端连接测试（示例）

1. 使用 `openssl s_client` 检查 TLS 握手（客户端证书）：

```plain
openssl s_client -connect <LB_IP_OR_HOSTNAME>:5671 \
  -cert client.crt -key client.key -CAfile ca.crt -showcerts
```

预期：握手成功并可看到服务器证书链；若服务端要求客户端证书且你没提供或证书不被 CA 签名，会被拒绝。

1. 使用 `rabbitmqadmin` 或 AMQP 客户端（例如 Python pika）配置 TLS 连接示例（Python pika）：

```plain
import pika, ssl

ssl_context = ssl.create_default_context(cafile="ca.crt")
ssl_context.load_cert_chain(certfile="client.crt", keyfile="client.key")
ssl_context.check_hostname = True

params = pika.ConnectionParameters(
    host="your.lb.domain",
    port=5671,
    ssl_options=pika.SSLOptions(context=ssl_context, server_hostname="your.lb.domain")
)

conn = pika.BlockingConnection(params)
chan = conn.channel()
print("OK", conn.is_open)
conn.close()
```

如果管理 UI 也启用了 mTLS，你需要类似方式在浏览器或 curl 中提供 client certs（浏览器通常可导入 client cert）。curl 示例：

```plain
curl --cert client.crt --key client.key --cacert ca.crt https://your.lb.domain:15671/
```

***

# 8) 常见问题 & 排错要点

* **证书 SAN 不包含访问域名 / IP** → 握手或 hostname 验证失败（最常见）。务必把 LoadBalancer 域名/IP 与 k8s 服务 DNS 名放到 SAN。[RabbitMQ](https://www.rabbitmq.com/docs/ssl?utm_source=chatgpt.com)
* **RabbitMQ 未加载 rabbitmq.conf** → 检查容器内 `/etc/rabbitmq/rabbitmq.conf` 是否存在并且路径正确（有时 Click-to-Deploy 用不同路径或 env 覆盖）。
* **权限问题** → Secret 挂载到 Pod 后，证书文件权限需让 RabbitMQ 进程可读（容器内确认权限）。
* **Operator vs 手工 StatefulSet**：如果你使用 RabbitMQ Cluster Operator，建议使用 CR 的 `spec.tls.secretName` / `spec.tls.caSecretName` 字段来开启 TLS（Operator 会做一些自动配置）。我参考了 Operator 的 TLS 配置说明。[RabbitMQ](https://www.rabbitmq.com/kubernetes/operator/using-operator?utm_source=chatgpt.com)
* **LoadBalancer 外部 IP 与证书**：若你用外部 IP（而非域名），证书必须把 IP 加入 SAN（`IP.1 = x.x.x.x`）。
* **管理面板（15672/15671）**：HTTP 管理界面与 AMQP TLS 是两套端口/设置，均需分别配置证书路径。


> 更新: 2025-11-30 21:03:04  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/zrs9cvr2rubpfwil>