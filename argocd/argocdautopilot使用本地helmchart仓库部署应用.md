# argocd autopilot使用本地helmchart仓库部署应用

完整的project appset模板

```plain
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  annotations:
    argocd-autopilot.argoproj-labs.io/default-dest-server: https://kubernetes.default.svc
    argocd.argoproj.io/sync-options: PruneLast=true
    argocd.argoproj.io/sync-wave: "-2"
  creationTimestamp: null
  name: dam-preprod
  namespace: argocd
spec:
  clusterResourceWhitelist:
  - group: '*'
    kind: '*'
  description: dam-preprod project
  destinations:
  - namespace: '*'
    server: '*'
  namespaceResourceWhitelist:
  - group: '*'
    kind: '*'
  sourceRepos:
  - '*'
status: {}

---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: dam-preprod-localhelmrele
spec:
  generators:
  - git:
      files:
      - path: local-helmrepo/**/dam-preprod/config_dir.yaml
      repoURL: https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git
      requeueAfterSeconds: 20
      revision: ""
      

  template:
    metadata:
      labels:
        app.kubernetes.io/managed-by: argocd-autopilot
        app.kubernetes.io/name: '{{ appName }}'
      name: dam-preprod-{{ userGivenName }}
      namespace: argocd
    spec:
      project: dam-preprod
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{ destNamespace }}'
      source:
        repoURL: '{{ srcRepoURL }}'
        path: '{{ chartPath }}'
        targetRevision: '{{ srcTargetRevision }}'
        helm:
          releaseName: '{{ userGivenName }}'
          valueFiles:
            - values.yaml
      syncPolicy:
        automated:
          allowEmpty: true
          prune: true
          selfHeal: true
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "0"
  creationTimestamp: null
  name: dam-preprod-3rd-paries
  namespace: argocd
spec:
  generators:
  - git:
      files:
      - path: 3rd-parties/**/dam-preprod/config_dir.yaml
      repoURL: https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git
      requeueAfterSeconds: 20
      revision: ""
      template:
        metadata: {}
        spec:
          destination: {}
          project: ""
          source:
            repoURL: ""
  syncPolicy: {}
  template:
    metadata:
      labels:
        app.kubernetes.io/managed-by: argocd-autopilot
        app.kubernetes.io/name: '{{ appName }}'
      name: dam-preprod-{{ userGivenName }}
      namespace: argocd
    spec:
      destination:
        namespace: '{{ destNamespace }}'
        server: https://kubernetes.default.svc
      ignoreDifferences:
      - group: argoproj.io
        jsonPointers:
        - /status
        kind: Application
      project: dam-preprod
      source:
        chart: '{{ chart }}'
        helm:
          releaseName: '{{ userGivenName }}'
          values: |
            {{app_values}}
        repoURL: '{{ srcRepoURL }}'
        targetRevision: '{{ srcTargetRevision }}'
      syncPolicy:
        automated:
          allowEmpty: true
          prune: true
          selfHeal: true
status: {}
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "0"
  creationTimestamp: null
  name: dam-preprod
  namespace: argocd
spec:
  generators:
  - git:
      files:
      - path: apps/**/dam-preprod/config.json
      repoURL: https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git
      requeueAfterSeconds: 20
      revision: ""
      template:
        metadata: {}
        spec:
          destination: {}
          project: ""
  - git:
      files:
      - path: apps/**/dam-preprod/config_dir.json
      repoURL: https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git
      requeueAfterSeconds: 20
      revision: ""
      template:
        metadata: {}
        spec:
          destination: {}
          project: ""
          source:
            directory:
              exclude: '{{ exclude }}'
              include: '{{ include }}'
              jsonnet: {}
              recurse: true
            repoURL: ""
  syncPolicy: {}
  template:
    metadata:
      labels:
        app.kubernetes.io/managed-by: argocd-autopilot
        app.kubernetes.io/name: '{{ appName }}'
      name: dam-preprod-{{ userGivenName }}
      namespace: argocd
    spec:
      destination:
        namespace: '{{ destNamespace }}'
        server: '{{ destServer }}'
      ignoreDifferences:
      - group: argoproj.io
        jsonPointers:
        - /status
        kind: Application
      project: dam-preprod
      source:
        path: '{{ srcPath }}'
        repoURL: '{{ srcRepoURL }}'
        targetRevision: '{{ srcTargetRevision }}'
      syncPolicy:
        automated:
          allowEmpty: true
          prune: true
          selfHeal: true
status: {}
```

# 创建能够读取本地helmchart仓库的applicationset 模板

```plain
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: dam-preprod-localhelmrele
spec:
  generators:
  - git:
      files:
      - path: local-helmrepo/**/dam-preprod/config_dir.yaml
      repoURL: https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git
      requeueAfterSeconds: 20
      revision: ""
      

  template:
    metadata:
      labels:
        app.kubernetes.io/managed-by: argocd-autopilot
        app.kubernetes.io/name: '{{ appName }}'
      name: dam-preprod-{{ userGivenName }}
      namespace: argocd
    spec:
      project: dam-preprod
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{ destNamespace }}'
      source:
        repoURL: '{{ srcRepoURL }}'
        path: '{{ chartPath }}'
        targetRevision: '{{ srcTargetRevision }}'
        helm:
          releaseName: '{{ userGivenName }}'
          valueFiles:
            - values.yaml
      syncPolicy:
        automated:
          allowEmpty: true
          prune: true
          selfHeal: true
```

# <font style="color:rgb(6, 10, 38);">argocd autopilot的 config\_dir.yaml文件，不能识别application的配置</font>

<font style="color:rgb(6, 10, 38);">你现在的 </font><code><font style="color:rgb(6, 10, 38);">config_dir.yaml</font></code><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">是一个完整的 </font>**<code>**<font style="color:rgb(6, 10, 38);">Application</font>**</code>**<font style="color:rgb(6, 10, 38);"> 对象</font>**<font style="color:rgb(6, 10, 38);">，而不是 Argo CD ApplicationSet 的 </font><code><font style="color:rgb(6, 10, 38);">git.files</font></code><font style="color:rgb(6, 10, 38);"> generator 所期望的 </font>**<font style="color:rgb(6, 10, 38);">纯参数字典（plain key-value YAML）</font>**<font style="color:rgb(6, 10, 38);">。</font>

<font style="color:rgb(6, 10, 38);">这就是问题的根本原因！</font>

***

## **<font style="color:rgb(6, 10, 38);">❌</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 为什么当前配置不工作？</font>**

<font style="color:rgb(6, 10, 38);">Argo CD 的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">git</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">generator +</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">files</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">模式要求：</font>

**<font style="color:rgb(6, 10, 38);">每个匹配的文件必须是一个扁平的 key-value YAML（即参数字典），不能是 Kubernetes 资源对象。</font>**

<font style="color:rgb(6, 10, 38);">但你的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">config_dir.yaml</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">是：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
apiVersion: argoproj.io/v1alpha1
kind: Application   # ← 这是 Kubernetes 资源！
metadata:
  name: nacos-helm
spec:
  ...
```

<font style="color:rgb(6, 10, 38);">→ Argo CD 会尝试把这个整个对象当作“参数”来解析，结果：</font>

* <font style="color:rgb(6, 10, 38);">它找不到</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">name</font></code><font style="color:rgb(6, 10, 38);">、</font><code><font style="color:rgb(6, 10, 38);">userGivenName</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">等字段（因为它们在</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">metadata.name</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">和</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">spec.source.helm.releaseName</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">里）</font>
* <font style="color:rgb(6, 10, 38);">模板中的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">{{ name }}</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">无法被替换 → 字面量</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">{{ name }}</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">被写入资源名 →</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">报错</font>**

***

## **<font style="color:rgb(6, 10, 38);">✅</font>****<font style="color:rgb(6, 10, 38);"> 正确做法：将</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">Application</font></code>**<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">转换为</font>****<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">参数字典</font>**

<font style="color:rgb(6, 10, 38);">你需要把</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">config_dir.yaml</font></code><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">重构成一个纯参数文件</font>**<font style="color:rgb(6, 10, 38);">，只保留模板需要的变量。</font>

### **<font style="color:rgb(6, 10, 38);">🔧</font>****<font style="color:rgb(6, 10, 38);"> 步骤 1：从原</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">Application</font></code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">中提取关键参数</font>**

**<font style="color:rgb(6, 10, 38);background-color:rgba(6, 10, 38, 0.06);">表格</font>**

| **<font style="color:rgb(6, 10, 38);">模板变量</font>** | **<font style="color:rgb(6, 10, 38);">来源（原 Application）</font>** | **<font style="color:rgb(6, 10, 38);">示例值</font>** |
| :--- | :--- | :--- |
| <code><font style="color:rgb(6, 10, 38);">name</font></code> | <code><font style="color:rgb(6, 10, 38);">metadata.name</font></code><br/><font style="color:rgb(6, 10, 38);">（但需简化）</font> | <code><font style="color:rgb(6, 10, 38);">nacos</font></code> |
| <code><font style="color:rgb(6, 10, 38);">userGivenName</font></code> | <code><font style="color:rgb(6, 10, 38);">spec.source.helm.releaseName</font></code><br/><font style="color:rgb(6, 10, 38);">（去掉</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">-release</font></code><br/><font style="color:rgb(6, 10, 38);">）</font> | <code><font style="color:rgb(6, 10, 38);">nacos</font></code> |
| <code><font style="color:rgb(6, 10, 38);">srcRepoURL</font></code> | <code><font style="color:rgb(6, 10, 38);">spec.source.repoURL</font></code> | <code><font style="color:rgb(6, 10, 38);">http://git.xxx.com/.../repo.git</font></code> |
| <code><font style="color:rgb(6, 10, 38);">srcTargetRevision</font></code> | <code><font style="color:rgb(6, 10, 38);">spec.source.targetRevision</font></code> | <code><font style="color:rgb(6, 10, 38);">HEAD</font></code> |
| <code><font style="color:rgb(6, 10, 38);">chartPath</font></code> | <code><font style="color:rgb(6, 10, 38);">spec.source.path</font></code> | <code><font style="color:rgb(6, 10, 38);">jed-middleware/nacos-helm-2.5.1</font></code> |
| <code><font style="color:rgb(6, 10, 38);">destNamespace</font></code> | <code><font style="color:rgb(6, 10, 38);">spec.destination.namespace</font></code> | <code><font style="color:rgb(6, 10, 38);">default</font></code> |

<font style="color:rgba(6, 10, 38, 0.7) !important;">💡</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 建议</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">name</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">使用简短、合法的标识符（如</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">nacos</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">），不要用</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">nacos-helm</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">（含</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">-</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">虽然合法，但冗余）。</font>

***

### **<font style="color:rgb(6, 10, 38);">✅</font>****<font style="color:rgb(6, 10, 38);"> 步骤 2：重写</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">config_dir.yaml</font></code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">为参数字典</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
# local-helmrepo/nacos/dam-preprod/config_dir.yaml
name: nacos
userGivenName: nacos
srcRepoURL: "http://git.txxxx.com/sysops/jed-main-infrastructure-repo.git"
srcTargetRevision: HEAD
chartPath: jed-middleware/nacos-helm-2.5.1
destNamespace: default
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">⚠️</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> 注意：</font>

* **<font style="color:rgb(6, 10, 38);">没有</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">apiVersion</font>**</code>**<font style="color:rgb(6, 10, 38);">、</font>**<code>**<font style="color:rgb(6, 10, 38);">kind</font>**</code>**<font style="color:rgb(6, 10, 38);">、</font>**<code>**<font style="color:rgb(6, 10, 38);">metadata</font>**</code>**<font style="color:rgb(6, 10, 38);">、</font>**<code>**<font style="color:rgb(6, 10, 38);">spec</font>**</code>
* **<font style="color:rgb(6, 10, 38);">只有扁平的 key-value</font>**
* <font style="color:rgba(6, 10, 38, 0.7) !important;">所有 key 必须和</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">template</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">中的</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">{{ xxx }}</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">完全一致</font>

***

### **<font style="color:rgb(6, 10, 38);">✅</font>****<font style="color:rgb(6, 10, 38);"> 步骤 3：确保目录结构匹配</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code><font style="color:rgb(6, 10, 38);">files.path</font></code>

<font style="color:rgb(6, 10, 38);">你的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">ApplicationSet</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">中写的是：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
files:
- path: local-helmrepo/**/dam-preprod/config_dir.yaml
```

<font style="color:rgb(6, 10, 38);">所以 Git 中路径必须是：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">text</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
local-helmrepo/
└── nacos/                  # ← 任意子目录名（会被忽略，参数来自 config_dir.yaml）
    └── dam-preprod/
        └── config_dir.yaml   # ← 上面的参数字典
```

<font style="color:rgba(6, 10, 38, 0.7) !important;">📌</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">**</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">表示任意层级，所以</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">local-helmrepo/teamA/nacos/dam-preprod/config_dir.yaml</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">也可以。</font>

***

## **<font style="color:rgb(6, 10, 38);">🔄</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 最终效果</font>**

<font style="color:rgb(6, 10, 38);">当 Argo CD 扫描到这个</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">config_dir.yaml</font></code><font style="color:rgb(6, 10, 38);">，它会生成一个 Application，等效于：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dam-preprod-nacos          # ← 来自 template + name=nacos
  labels:
    app.kubernetes.io/name: nacos  # ← 来自 userGivenName
spec:
  project: dam-preprod
  source:
    repoURL: "http://git.txxxx.com/.../repo.git"
    targetRevision: HEAD
    path: jed-middleware/nacos-helm-2.5.1
    helm:
      releaseName: nacos           # ← userGivenName
      valueFiles:
        - values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: default             # ← destNamespace
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```


> 更新: 2026-01-22 20:12:52  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/tthipp90nxcpd42h>