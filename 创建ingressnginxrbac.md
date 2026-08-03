# 创建 ingress nginx rbac

# 示例：只允许特定角色创建 Ingress
```plain
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: your-app-ns
  name: ingress-editor
rules:
- apiGroups: ["networking.k8s.io"]
  resources: ["ingresses"]
  verbs: ["create", "update", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: your-app-ns
  name: dev-team-ingress
subjects:
- kind: Group
  name: "dev-team@example.com"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: ingress-editor
  apiGroup: rbac.authorization.k8s.io
```



> 更新: 2025-12-02 10:59:02  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vv9tgdu8esh8gg1y>