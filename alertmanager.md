# alertmanager

### <font style="color:rgb(0, 0, 0);">1. 确保 Alertmanager 启用并配置服务</font>

<font style="color:rgb(0, 0, 0);">首先确认 Alertmanager 已启用（默认启用），其服务会暴露地址供 Prometheus 访问。</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">values-kube-prometheus-stack.yaml</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">中相关配置（通常无需修改默认值即可满足关联需求）：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">yaml</font>**

```yaml
alertmanager:
  enabled: true  # 确保 Alertmanager 启用
  service:
    enabled: true
    port: 9093  # Alertmanager 服务端口，默认9093
    type: ClusterIP  # 集群内可访问的服务类型
  alertmanagerSpec:
    replicas: 1  # 副本数，默认1
```

### <font style="color:rgb(0, 0, 0);">2. 配置 Prometheus 关联 Alertmanager</font>

<font style="color:rgb(0, 0, 0);">在 Prometheus 配置中，通过</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">prometheus.prometheusSpec.alerting.endpoints</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">指定 Alertmanager 的服务地址。在</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">values</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">文件中添加或修改 Prometheus 配置：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">yaml</font>**

```yaml
prometheus:
  prometheusSpec:
    # 配置 Alertmanager 地址，让 Prometheus 发送警报
    alerting:
      endpoints:
        - name: alertmanager  # 自定义名称
          namespace: monitoring  # Alertmanager 部署的命名空间（需与实际一致）
          port: web  # 对应 Alertmanager 服务的端口名称（默认服务端口名为web）
          path: /api/v2/alerts  # Alertmanager 接收警报的API路径（v2版本固定）
    
    # 可选：配置警报规则（默认规则已包含，可自定义）
    ruleSelector: {}  # 选择所有规则（默认）
    ruleNamespaceSelector: {}  # 选择所有命名空间的规则（默认）
```

### <font style="color:rgb(0, 0, 0);">3. 关键配置说明</font>

* **<font style="color:rgb(0, 0, 0) !important;">Alertmanager 服务地址</font>**<font style="color:rgb(0, 0, 0);">：Prometheus 通过 Kubernetes Service 访问 Alertmanager，地址格式为</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">{service-name}.{namespace}:{port}</font></code><font style="color:rgb(0, 0, 0);">。若未自定义名称，默认 Service 名称为</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">{{ .Release.Name }}-alertmanager</font></code><font style="color:rgb(0, 0, 0);">（例如</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kube-prometheus-stack-alertmanager</font></code><font style="color:rgb(0, 0, 0);">），命名空间为部署时指定的 namespace（如</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">monitoring</font></code><font style="color:rgb(0, 0, 0);">）。</font>
* **<font style="color:rgb(0, 0, 0) !important;">端口映射</font>**<font style="color:rgb(0, 0, 0);">：Alertmanager 服务的</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">port: 9093</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">对应端口名称</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">web</font></code><font style="color:rgb(0, 0, 0);">，因此在 Prometheus 配置中用</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">port: web</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">引用。</font>
* **<font style="color:rgb(0, 0, 0) !important;">默认规则</font>**<font style="color:rgb(0, 0, 0);">：若</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">defaultRules.create: true</font></code><font style="color:rgb(0, 0, 0);">（默认启用），会自动创建基础警报规则，Prometheus 加载这些规则后会将触发的警报发送到配置的 Alertmanager。</font>

### <font style="color:rgb(0, 0, 0);">4. 完整示例（合并关键配置）</font>

**<font style="color:rgba(0, 0, 0, 0.85);">yaml</font>**

```yaml
# values-kube-prometheus-stack.yaml 中需添加/修改的部分
alertmanager:
  enabled: true
  service:
    port: 9093
    type: ClusterIP

prometheus:
  prometheusSpec:
    alerting:
      endpoints:
        - name: alertmanager
          namespace: monitoring  # 替换为实际部署的命名空间
          port: web
          path: /api/v2/alerts

defaultRules:
  create: true  # 启用默认警报规则（可选，根据需求调整）
```


> 更新: 2025-10-16 20:47:48  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/qabdss7037ba0ifx>