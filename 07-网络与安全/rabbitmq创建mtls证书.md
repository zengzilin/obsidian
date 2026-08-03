# rabbitmq创建 mtls证书

手动创建一个适合bitnami mq的公共证书

## **<font style="color:rgb(6, 10, 38);">第一步：准备工具</font>**

<font style="color:rgb(6, 10, 38);">确保你有</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">openssl</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">或</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">cfssl</font></code><font style="color:rgb(6, 10, 38);">。这里使用</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">OpenSSL</font>**<font style="color:rgb(6, 10, 38);">（最通用）。</font>

***

## **<font style="color:rgb(6, 10, 38);">📁</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 第二步：创建工作目录</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
mkdir -p rabbitmq-mtls && cd rabbitmq-mtls
```

***

## **<font style="color:rgb(6, 10, 38);">🔐</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 第三步：生成 CA（证书颁发机构）</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
# 生成 CA 私钥
openssl genrsa -out ca.key 2048

# 生成 CA 证书（有效期 10 年）
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -subj "/CN=RabbitMQ CA" \
  -out ca.crt
```

***

## **<font style="color:rgb(6, 10, 38);">🖥️</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 第四步：生成 RabbitMQ 服务端证书</font>**

### **<font style="color:rgb(6, 10, 38);">1. 创建 CSR 配置文件（支持 SAN）</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
cat > server.conf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
CN = rabbitmq

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.svc.cluster.local
IP.1 = 127.0.0.1
EOF
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">💡</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 根据你的实际部署调整</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">DNS</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">和</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">IP</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">：</font>

* <font style="color:rgba(6, 10, 38, 0.7) !important;">如果 Helm release 名是</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">my-rabbitmq</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">，命名空间是</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">mq</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">，则服务名为</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">my-rabbitmq.mq.svc.cluster.local</font></code>
* <font style="color:rgba(6, 10, 38, 0.7) !important;">建议至少包含：</font><code><font style="color:rgb(6, 10, 38);"><release-name>-headless.<namespace>.svc.cluster.local</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">和</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);"><release-name>.<namespace>.svc.cluster.local</font></code>

### **<font style="color:rgb(6, 10, 38);">2. 生成服务端私钥和 CSR</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config server.conf
```

### **<font style="color:rgb(6, 10, 38);">3. 用 CA 签发服务端证书</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out server.crt -days 365 -sha256 -extensions v3_req -extfile server.conf
```

***

## **<font style="color:rgb(6, 10, 38);">👤</font>\*\*\*\*<font style="color:rgb(6, 10, 38);">（可选）第五步：生成客户端证书（用于测试 mTLS）</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
# 客户端私钥
openssl genrsa -out client.key 2048

# 客户端 CSR
openssl req -new -key client.key -out client.csr -subj "/CN=rabbitmq-client"

# 签发客户端证书（注意：extendedKeyUsage=clientAuth）
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out client.crt -days 365 -sha256 -extfile <(echo "extendedKeyUsage=clientAuth")
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">这个</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">client.crt</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">/</font><code><font style="color:rgb(6, 10, 38);">client.key</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">可用于</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">rabbitmqctl</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">或应用连接测试。</font>

***

## **<font style="color:rgb(6, 10, 38);">📦</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 第六步：创建 Kubernetes Secret（仅服务端 + CA）</font>**

<font style="color:rgb(6, 10, 38);">Bitnami RabbitMQ 要求 Secret 中包含以下</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">固定文件名</font>**<font style="color:rgb(6, 10, 38);">：</font>

* <code><font style="color:rgb(6, 10, 38);">ca_certificate.pem</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">→ CA 证书</font>
* <code><font style="color:rgb(6, 10, 38);">server_certificate.pem</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">→ 服务端证书（可含中间 CA，这里只有根 CA）</font>
* <code><font style="color:rgb(6, 10, 38);">server_key.pem</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">→ 服务端私钥</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
kubectl -n middleware create secret generic rabbitmq-mtls-secret \
  --from-file=ca_certificate.pem=ca.crt \
  --from-file=server_certificate.pem=server.crt \
  --from-file=server_key.pem=server.key
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">✅</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 注意：</font>**<font style="color:rgb(6, 10, 38);">不要</font>**<font style="color:rgba(6, 10, 38, 0.7) !important;">把客户端证书放进去！RabbitMQ 服务端只需要自己的证书和 CA。</font>

***

## **<font style="color:rgb(6, 10, 38);">🛠️</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 第七步：Helm values.yaml 配置</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
tls:
  enabled: true
  autoGenerated: false
  existingSecret: "rabbitmq-mtls-secret"
  existingSecretFullChain: false
  failIfNoPeerCert: true
  sslOptionsVerify: verify_peer
  # 其他留空
  caCertificate: ""
  serverCertificate: ""
  serverKey: ""
  overrideCaCertificate: ""
  sslOptionsPassword:
    enabled: false
```

* <code><font style="color:rgb(6, 10, 38);">failIfNoPeerCert: true</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">+</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">sslOptionsVerify: verify_peer</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">启用</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font>**<font style="color:rgb(6, 10, 38);">强制客户端提供有效证书</font>**
* <font style="color:rgba(6, 10, 38, 0.7) !important;">客户端必须使用由同一 CA 签发的证书才能连接</font>

***

## **<font style="color:rgb(6, 10, 38);">✅</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 验证 Secret 内容</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
kubectl get secret rabbitmq-mtls-secret -o json | jq -r '.data | map_values(@base64d)'
```


> 更新: 2026-01-23 14:52:28  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vagpzrswuaav273a>