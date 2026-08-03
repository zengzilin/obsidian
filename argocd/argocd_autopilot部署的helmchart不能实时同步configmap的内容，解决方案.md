# argocd/autopilot 部署的helmchart 不能实时同步configmap的内容，解决方案

## **<font style="color:rgb(6, 10, 38);">✅</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 解决方案（任选其一）</font>**

***

### **<font style="color:rgb(6, 10, 38);">✅</font>****<font style="color:rgb(6, 10, 38);"> 方案 1：在 Helm Chart 中启用</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">helm.sh/hook: refresh</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">或使用</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">checksum</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">注解</font>****<font style="color:rgb(6, 10, 38);">（推荐）</font>**

<font style="color:rgb(6, 10, 38);">这是</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">最标准、最可靠</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">的做法，适用于所有 Helm 应用（包括 Nacos）。</font>

#### **<font style="color:rgb(6, 10, 38);">步骤：</font>**

1. **<font style="color:rgb(6, 10, 38);">确保你的 Nacos Helm Chart 在 Deployment/StatefulSet 的 Pod 模板中包含 ConfigMap 的 checksum 注解</font>**<font style="color:rgb(6, 10, 38);">：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "nacos.fullname" . }}
  namespace: {{ .Values.namespace }}
  annotations:
  {{- toYaml .Values.annotations | indent 4 }}
spec:
  {{- if eq .Values.global.mode "cluster" }}
  serviceName: nacos-hs
  {{- else }}
  serviceName: nacos-cs
  {{- end }}
  replicas: {{ .Values.nacos.replicaCount }}
  {{- if .Values.nacos.podManagementPolicy }}
  podManagementPolicy: {{ .Values.nacos.podManagementPolicy }}
  {{- else}}
  podManagementPolicy: OrderedReady
  {{- end }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "nacos.name" . }}
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "nacos.name" . }}
        app.kubernetes.io/instance: {{ .Release.Name }}
      annotations:
        # 👇 为 application.properties ConfigMap 生成 checksum
        checksum/application-properties: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        # 👇 为 nacos-cm ConfigMap 生成 checksum
        checksum/nacos-cm: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
    spec:
      {{- with .Values.nodeSelector }}
      nodeSelector:
      {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
      {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
      {{- toYaml . | nindent 8 }}
      {{- end }}

          # ...
```

1. **<font style="color:rgb(6, 10, 38);">这样，只要 ConfigMap 内容变化 → checksum 变化 → Pod 重启 → 加载新配置</font>**

<font style="color:rgba(6, 10, 38, 0.7) !important;">💡</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 大多数官方 Helm Chart（如 Bitnami）都已内置此逻辑。如果你用的是自研或旧版 Nacos Chart，可能需要手动添加。</font>


> 更新: 2026-01-22 20:19:46  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/qp6ou73oqa691000>