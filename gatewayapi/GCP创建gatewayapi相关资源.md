# GCP 创建 gateway api相关资源

# 创建自管理证书创建区域外部应用程序负载均衡器网关

```plain
kind: Gateway
  apiVersion: gateway.networking.k8s.io/v1
  metadata:
    name: external-regional-http
  spec:
    # Name of an existing GatewayClass.
    gatewayClassName: gke-l7-regional-external-managed
    # Listen for HTTPS traffic on port 443
    listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        # Terminate the TLS session with the client at the Gateway.
        mode: Terminate
        # Certificates for the Gateway to use to create a new TLS session.
        certificateRefs:
        - name: store-example-com #自定义证书
    # The name of the static IP address of the external load balancer.
    # You can also use the `IPAddress` type to specify the actual IP address.
    addresses:
    - type: NamedAddress
      value: IP_ADDRESS_NAME #自定义ip
```

# 创建外部https网关，certmap证书

```plain
kind: Gateway
apiVersion: gateway.networking.k8s.io/v1
metadata:
  name: external-http
  annotations:
    networking.gke.io/certmap: store-example-com-map
spec:
  # This GatewayClass uses a global external Application Load Balancer.
  gatewayClassName: gke-l7-global-external-managed
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
```

# 创建内部https网关（自管理的ssl证书）

<https://cloud.google.com/kubernetes-engine/docs/how-to/gatewayclass-capabilities>

<font style="color:rgb(17, 17, 51);">根据文档，</font><code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">gke-l7-rilb</font></code>**<font style="color:rgb(17, 17, 51);">不支持</font>**<font style="color:rgb(17, 17, 51);">通过 </font><code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">certificateRefs</font></code><font style="color:rgb(17, 17, 51);"> 引用 Kubernetes Secret：</font>networking.gke.io/certmap: store-example-com-map

### 方法 A：使用 Compute Engine 自行管理的 SSL 证书

```plain
```

```plain
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: internal-https-gateway
  namespace: default
spec:
  gatewayClassName: gke-l7-rilb  # 内部区域级 HTTPS 网关
  listeners:
  - name: https
    protocol: HTTPS
    port: 443
    tls:
      mode: Terminate
      options:
        networking.gke.io/pre-shared-certs: "my-internal-cert"  # 引用上一步创建的证书
```

# 创建http route

```plain
kind: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1
metadata:
  name: store-external
spec:
  parentRefs:
  # Bind the route to the 'external-http' Gateway.
  - kind: Gateway
    name: external-http
  hostnames:
  - "store.example.com"
  rules:
  # Default rule for store.example.com that sends traffic to the store-v1 service.
  - backendRefs:
    - name: store-v1
      port: 8080
  # Match requests with the "env: canary" header and send them to the store-v2 service.
  - matches:
    - headers:
      - name: env
        value: canary
    backendRefs:
    - name: store-v2
      port: 8080
  # Match requests with the path "/de" and sends them to the store-german service.
  - matches:
    - path:
        value: /de
    backendRefs:
    - name: store-german
      port: 8080
```

# 匹配接收所有流量的httproute

```plain
kind: HTTPRoute
apiVersion: gateway.networking.k8s.io/v1
metadata:
  name: site-internal
spec:
  # Attach the HTTPRoute to the `internal-http` Gateway.
  parentRefs:
  - kind: Gateway
    name: internal-http
  # Route requests that have `site.example.com` in the Host header.
  hostnames:
  - "site.example.com"
  # Send all requests to the `site-v1` Service.
  rules:
  - backendRefs:
    - name: site-v1
      port: 8080
```

```plain
kind: Gateway
apiVersion: gateway.networking.k8s.io/v1
metadata:
   name: internal-http
spec:
  # Specify an existing GatewayClass.
  gatewayClassName: gke-l7-rilb
  listeners:
  # Listen for HTTP traffic on port 80.
  - name: http
    protocol: HTTP
    port: 80
```


> 更新: 2025-11-30 23:44:06  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rxptwqxgaq68zym5>