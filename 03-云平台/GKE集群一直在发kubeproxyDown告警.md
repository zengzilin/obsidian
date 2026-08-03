# GKE 集群一直在发kubeproxyDown告警

:::info <font style="color:#DF2A3F;"> FIRING【KubeProxyDown】\ </font><font style="color:#DF2A3F;">alertname:KubeProxyDown\ </font><font style="color:#DF2A3F;">severity:critical\ </font><font style="color:#DF2A3F;">description:KubeProxy has disappeared from Prometheus target discovery.\ </font><font style="color:#DF2A3F;">summary:Target disappeared from Prometheus target discovery.\ </font><font style="color:#DF2A3F;">startsAt:2025-08-26 21:55:29.493 +0000 UTC\ </font><font style="color:#DF2A3F;">endsAt:0001-01-01 00:00:00 +0000 UTC\ </font><font style="color:#DF2A3F;">generatorURL:prometheus-kube-prometheus-prometheus.monitoring:9090  </font>

:::

:::info
kubectl get  pod -n kube-system kube-proxy-gke-gke-tiq-ew1-p-wa-pool-tiq-ew1-p-m-84bcefbe-0snd -o jsonpath='{.metadata.labels}'

<font style="color:#DF2A3F;">{"component":"kube-proxy","tier":"node"}</font>

:::

:::info
kubectl get svc prometheus-kube-prometheus-kube-proxy -o jsonpath='{.spec.selector}'  -n kube-system               {"k8s-app":"kube-proxy"}

:::

<font style="color:rgb(0, 0, 0);">在</font>**<font style="color:rgb(0, 0, 0);"> GKE 中，</font>**<code>**<font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font>**</code>**<font style="color:rgb(0, 0, 0);"> 是由 GKE 托管的组件，其标签、配置等由 GKE 自动管理，直接修改可能会被 GKE 自动覆盖（尤其是在节点升级、集群更新时），因此确实不建议手动修改其原生标签。</font>**

<font style="color:rgb(0, 0, 0);">针对这种情况，更安全的做法是</font><font style="color:rgb(0, 0, 0);"> </font>**<font style="color:rgb(0, 0, 0) !important;">调整 Prometheus 的抓取配置来适配 GKE 原生</font>\*\*\*\*<font style="color:rgb(0, 0, 0) !important;"> </font>**<code>**<font style="color:rgb(0, 0, 0);">kube-proxy</font>**</code>**<font style="color:rgb(0, 0, 0) !important;"> </font>\*\*\*\*<font style="color:rgb(0, 0, 0) !important;">的标签</font>**<font style="color:rgb(0, 0, 0);">，而非修改</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">自身。具体步骤如下：</font>

### **<font style="color:rgb(0, 0, 0) !important;">核心思路</font>**

<font style="color:rgb(0, 0, 0);">GKE 的</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">Pod 标签为</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">component: kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">和</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">tier: node</font></code><font style="color:rgb(0, 0, 0);">（你已确认），我们需要让 Prometheus 的抓取规则（ServiceMonitor 或 scrape\_configs）</font>**<font style="color:rgb(0, 0, 0) !important;">主动适配这些标签</font>**<font style="color:rgb(0, 0, 0);">，而不是要求</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">符合 Prometheus 的默认标签预期。</font>

### **<font style="color:rgb(0, 0, 0) !important;">步骤 1：调整 KubeProxy Service 的选择器（适配 Pod 标签）</font>**

<font style="color:rgb(0, 0, 0);">GKE 可能已自动创建了</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">的 Service（或你之前提到的</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">prometheus-kube-prometheus-kube-proxy</font></code><font style="color:rgb(0, 0, 0);">），需确保其选择器匹配 GKE 原生</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">的标签：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
# 编辑 Service 配置
kubectl edit svc prometheus-kube-prometheus-kube-proxy -n kube-system
```

<font style="color:rgb(0, 0, 0);">修改</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">spec.selector</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">为 GKE</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">的标签：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">yaml</font>**

```yaml
spec:
  selector:
    component: kube-proxy  # 匹配 GKE kube-proxy 的 component 标签
    tier: node             # 匹配 GKE kube-proxy 的 tier 标签
```

<font style="color:rgb(0, 0, 0);">这样 Service 就能正确关联到 GKE 的</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-proxy</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">Pod，无需修改 Pod 本身。</font>

### **<font style="color:rgb(0, 0, 0) !important;">步骤 2：修改 Prometheus 的 ServiceMonitor（适配 Service 标签）</font>**

<font style="color:rgb(0, 0, 0);">若使用</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">ServiceMonitor</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">发现目标，需让其选择器匹配上一步修改后的 Service 标签（而非依赖默认标签）。</font>

1. <font style="color:rgb(0, 0, 0);">先查看 Service 的标签（确保知道要匹配哪些标签）：</font>**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
kubectl get svc prometheus-kube-prometheus-kube-proxy -n kube-system -o jsonpath='{.metadata.labels}'
```

<font style="color:rgb(0, 0, 0);">假设输出类似：</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">{"app":"kube-prometheus-stack-kube-proxy", "release":"prometheus", ...}</font></code>

2. <font style="color:rgb(0, 0, 0);">编辑对应的 ServiceMonitor：</font>**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
kubectl edit servicemonitor prometheus-kube-prometheus-kube-proxy -n monitoring  # 替换为实际名称
```

3. <font style="color:rgb(0, 0, 0);">调整</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">spec.selector.matchLabels</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">以匹配 Service 的标签：</font>**<font style="color:rgba(0, 0, 0, 0.85);">yaml</font>**

kube-prometheus-stack-kube-proxy

```yaml
spec:
  selector:
    matchLabels:
      app: kube-prometheus-stack-kube-proxy  # 匹配 Service 的 app 标签
      release: prometheus                   # 匹配 Service 的 release 标签
  namespaceSelector:
    matchNames:
      - kube-system  # Service 所在的命名空间
  endpoints:
    - port: http-metrics  # 与 Service 中定义的端口名一致（通常是 metrics 端口）
      interval: 15s
```


> 更新: 2025-10-17 10:40:11  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vkw1yyongfl9rlcc>