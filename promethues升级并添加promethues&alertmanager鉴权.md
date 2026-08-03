# promethues 升级 并添加promethues&alertmanager鉴权

### <font style="color:rgba(0, 0, 0, 0.9);">一、基础部署（启用鉴权前）</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1. 添加 Helm Repo 并查看配置</font>

```plain
bash

复制
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts  
helm repo update 
helm show values prometheus-community/kube-prometheus-stack > values.yaml
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 配置核心参数（</font><code><font style="color:rgba(0, 0, 0, 0.9);">values.yaml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">）</font>

```plain
yaml

复制
prometheus:
  enabled: true 
  service:
    type: ClusterIP 
  ingress:
    enabled: true 
    hosts: [prometheus.example.com]
    annotations: 
      nginx.ingress.kubernetes.io/auth-type:  basic 
      nginx.ingress.kubernetes.io/auth-secret:  prometheus-basic-auth 
    tls:
    - secretName: prometheus-tls  # 提前创建 TLS 证书 
 
alertmanager:
  enabled: true 
  ingress:
    enabled: true 
    hosts: [alertmanager.example.com]
    annotations:
      nginx.ingress.kubernetes.io/auth-type:  basic 
      nginx.ingress.kubernetes.io/auth-secret:  alertmanager-basic-auth 
    tls:
    - secretName: alertmanager-tls
```

***

### <font style="color:rgba(0, 0, 0, 0.9);">二、鉴权配置（Basic Auth）</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1. 生成密码文件并创建 Secret</font>

```plain
bash

复制
# 生成 Prometheus 密码 
htpasswd -c auth-prom admin 
kubectl create secret generic prometheus-basic-auth --from-file=auth=auth-prom -n monitoring 
 
# 生成 Alertmanager 密码 
htpasswd -c auth-am admin  
kubectl create secret generic alertmanager-basic-auth --from-file=auth=auth-am -n monitoring
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 创建 TLS 证书（Let's Encrypt 示例）</font>

```plain
bash

复制
certbot certonly --manual --preferred-challenges=dns -d *.example.com  
kubectl create secret tls prometheus-tls --cert=fullchain.pem  --key=privkey.pem  -n monitoring 
kubectl create secret tls alertmanager-tls --cert=fullchain.pem  --key=privkey.pem  -n monitoring
```

***

### <font style="color:rgba(0, 0, 0, 0.9);">三、高级配置（适配鉴权）</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1. 更新探针配置（</font><code><font style="color:rgba(0, 0, 0, 0.9);">values.yaml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">）</font>

```plain
yaml

复制
prometheus:
  prometheusSpec:
    enableAdminAPI: false  # 禁用高危接口 
    retention: 15d 
    containers:
    - name: prometheus 
      livenessProbe:
        httpGet:
          path: /-/healthy 
          port: 9090 
          httpHeaders:
          - name: Authorization 
            value: Basic YWRtaW46cGFzc3dvcmQ=  # base64 编码的 admin:password 
 
alertmanager:
  alertmanagerSpec:
    containers:
    - name: alertmanager 
      readinessProbe:
        httpGet:
          path: /-/ready 
          port: 9093 
          httpHeaders:
          - name: Authorization 
            value: Basic YWRtaW46cGFzc3dvcmQ=
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 配置 Grafana 数据源鉴权</font>

```plain
yaml

复制
grafana:
  env:
    GF_SECURITY_DISABLE_INITIAL_ADMIN_PASSWORD: "true"
  datasources:
    datasources.yaml: 
      apiVersion: 1 
      datasources:
      - name: Prometheus 
        type: prometheus 
        url: http://prometheus-operated:9090 
        basicAuth: true 
        basicAuthUser: admin 
        secureJsonData:
          basicAuthPassword: your_password
```

### <font style="color:rgba(0, 0, 0, 0.9);">四、部署与验证</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1. 执行 Helm 安装</font>

```plain
bash

复制
helm upgrade --install kube-prom-stack prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f values.yaml
```

#### <font style="color:rgba(0, 0, 0, 0.9);">2. 验证命令</font>

```plain
bash

复制
# 检查 Ingress 配置 
kubectl get ingress -n monitoring 
 
# 测试鉴权访问 
curl -u admin:password -k https://prometheus.example.com/-/healthy  
curl -u admin:password -k https://alertmanager.example.com/-/ready
```


> 更新: 2025-03-20 21:50:47  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ok1lmxp7pull4sf1>