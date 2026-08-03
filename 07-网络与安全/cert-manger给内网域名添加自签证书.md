# cert-manger 给内网域名添加自签证书

# ✅ 零、安装 Cert-Manager（推荐官方 Helm）

<https://cert-manager.k8s.ac.cn/docs/installation/helm/>

### **1. 添加 Helm 仓库**

```plain
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

### <font style="color:rgb(30, 30, 89);">2. 安装 cert-manager</font>

```plain
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.16.1 \
  --set crds.enabled=true
```

# ✅ 一、创建内部 CA（只需部署一次）

如果你已经创建过 CA，可以跳过。

### 1. 创建 Root CA Issuer（自签）

```plain
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-root
  namespace: cert-manager
spec:
  selfSigned: {}
```

### 2. 使用自签 Issuer 生成内部 CA Secret

```plain
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: internal-root-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: internal-root-ca
  secretName: internal-root-ca-secret
  issuerRef:
    name: selfsigned-root
    kind: Issuer
```

### 3. 创建 ClusterIssuer（所有 NS 通用）

```plain
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: internal-ca
spec:
  ca:
    secretName: internal-root-ca-secret
```

***

# ✅ 二、为你的域名创建证书（account-abroad-finance-test）

你提供的 Ingress host 为：

```plain
account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
```

下面这个 Certificate 会自动生成一个 secret：`sp-gateway-core-tls`

并且 Cert-Manager 会自动续期。

### **cert-manager Certificate YAML（放在 account-abroad-finance-test namespace）**

```plain
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: sp-gateway-core-cert
  namespace: account-abroad-finance-test
spec:
  secretName: sp-gateway-core-tls
  duration: 8760h  # 1 年有效期
  renewBefore: 720h  # 30 天提前续期
  commonName: account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
  dnsNames:
    - account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
  issuerRef:
    name: internal-ca
    kind: ClusterIssuer
```

***

# ✅ 三、给你的 Ingress 加上 TLS（自动关联证书）

在你的原始 Ingress YAML 中新增以下两处：

1）Annotations：

```plain
cert-manager.io/cluster-issuer: internal-ca
```

2）TLS Block：

```plain
tls:
- hosts:
  - account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
  secretName: sp-gateway-core-tls
```

***

# 🔧 四、完整 Ingress

<font style="color:#DF2A3F;">公司用的是helmchart values！！</font>

values.yaml如下

```plain
ingress:
  enabled: true
  tls:
    - secretName: sp-gateway-core-tls
  annotations:
    cert-manager.io/cluster-issuer: internal-ca
    kubernetes.io/ingress.class: nginx
  
  hosts:
  - host: account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
    paths: ["/"]
```

下面是 **加上证书的最终 Ingress**：

```plain
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sp-gateway-core
  namespace: account-abroad-finance-test
  annotations:
    cert-manager.io/cluster-issuer: internal-ca
spec:
  tls:
  - hosts:
    - account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
    secretName: sp-gateway-core-tls

  rules:
  - host: account-abroad-finance-test-sp-gateway-core.k8s.wallyt.net
    http:
      paths:
      - path: /
        pathType: ImplementationSpecific
        backend:
          service:
            name: sp-gateway-core
            port:
              number: 8080
```


> 更新: 2025-12-04 15:53:47  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/oqkkaa8skplid5z3>