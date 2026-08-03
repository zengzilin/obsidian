# RabbitMQ Helm 升级密码报错与 Secret 误删恢复

## 现象
执行 Helm 升级时出现以下报错：

```bash
helm upgrade rabbitmq-cluster-msg ./ -f values-rabbitmq-cluster-msg.yaml -n middleware
```

报错示例：

```text
Error: UPGRADE FAILED: execution error at (rabbitmq/templates/statefulset.yaml:43:28):
PASSWORDS ERROR: You must provide your current passwords when upgrading the release.
                 Note that even after reinstallation, old credentials may be needed as they may be kept in persistent volume claims.

    'auth.erlangCookie' must not be empty, please add '--set auth.erlangCookie=$RABBITMQ_ERLANG_COOKIE' to the command.
```

## 原因
Bitnami RabbitMQ Helm Chart 在升级时会校验当前集群正在使用的历史凭据。
即使使用了 `--reuse-values` 或 `-f values.yaml`，也不会自动把 Kubernetes Secret 中的旧密码和 Erlang Cookie 重新注入到升级流程中。

如果底层 PVC 还在，升级时必须继续提供当前实际使用的：

- `auth.password`
- `auth.erlangCookie`
- 必要时还包括 `auth.username`

## 正常升级处理方式
如果原 Secret 还在，可以先从 Secret 里取出当前值，再执行升级。

### 1. 提取当前凭据

```bash
export RABBITMQ_PASSWORD=$(kubectl get secret -n middleware rabbitmq-cluster-msg -o jsonpath="{.data.rabbitmq-password}" | base64 -d)
export RABBITMQ_ERLANG_COOKIE=$(kubectl get secret -n middleware rabbitmq-cluster-msg -o jsonpath="{.data.rabbitmq-erlang-cookie}" | base64 -d)
```

如需用户名，也可以一起取：

```bash
export RABBITMQ_USERNAME=$(kubectl get secret -n middleware rabbitmq-cluster-msg -o jsonpath="{.data.rabbitmq-username}" | base64 -d)
```

### 2. 带旧凭据执行升级

```bash
helm upgrade rabbitmq-cluster-msg ./ \
  -f values-rabbitmq-cluster-msg.yaml \
  -n middleware \
  --set-string auth.password="$RABBITMQ_PASSWORD" \
  --set-string auth.erlangCookie="$RABBITMQ_ERLANG_COOKIE"
```

如果 Chart 中也校验用户名，则使用：

```bash
helm upgrade rabbitmq-cluster-msg ./ \
  -f values-rabbitmq-cluster-msg.yaml \
  -n middleware \
  --set-string auth.username="$RABBITMQ_USERNAME" \
  --set-string auth.password="$RABBITMQ_PASSWORD" \
  --set-string auth.erlangCookie="$RABBITMQ_ERLANG_COOKIE"
```

## Secret 被误删时的恢复方法
本次问题的关键是：

- Helm 升级要求提供当前旧凭据
- `rabbitmq-cluster-msg` Secret 被误删
- 需要先恢复 Secret，再继续升级

### 处理原则

1. 不要立刻重启 RabbitMQ Pod
2. 不要继续盲目执行 Helm upgrade
3. 优先从正在运行的 Pod 中取回旧凭据

### 1. 找到当前运行中的 RabbitMQ Pod

```bash
POD=$(kubectl get pod -n middleware -l app.kubernetes.io/instance=rabbitmq-cluster-msg -o jsonpath='{.items[0].metadata.name}')
```

### 2. 从运行中 Pod 提取凭据

```bash
export RABBITMQ_USERNAME=$(kubectl exec -n middleware "$POD" -- sh -lc 'printf %s "$RABBITMQ_USERNAME"')
export RABBITMQ_PASSWORD=$(kubectl exec -n middleware "$POD" -- sh -lc 'printf %s "$RABBITMQ_PASSWORD"')
export RABBITMQ_ERLANG_COOKIE=$(kubectl exec -n middleware "$POD" -- sh -lc 'printf %s "$RABBITMQ_ERL_COOKIE"')
```

### 3. 校验是否成功取到值

```bash
printf 'USER=%s\nPASS_LEN=%s\nCOOKIE_LEN=%s\n' \
  "$RABBITMQ_USERNAME" "${#RABBITMQ_PASSWORD}" "${#RABBITMQ_ERLANG_COOKIE}"
```

只要长度不为 0，通常说明已经成功取到。

### 4. 重建被删掉的 Secret

```bash
kubectl create secret generic rabbitmq-cluster-msg \
  -n middleware \
  --from-literal=rabbitmq-username="$RABBITMQ_USERNAME" \
  --from-literal=rabbitmq-password="$RABBITMQ_PASSWORD" \
  --from-literal=rabbitmq-erlang-cookie="$RABBITMQ_ERLANG_COOKIE"
```

### 5. 补上 Helm 管理元数据

```bash
kubectl label secret -n middleware rabbitmq-cluster-msg app.kubernetes.io/managed-by=Helm --overwrite

kubectl annotate secret -n middleware rabbitmq-cluster-msg \
  meta.helm.sh/release-name=rabbitmq-cluster-msg \
  meta.helm.sh/release-namespace=middleware \
  --overwrite
```

### 6. 再次执行升级

```bash
helm upgrade rabbitmq-cluster-msg ./ \
  -f values-rabbitmq-cluster-msg.yaml \
  -n middleware \
  --set-string auth.username="$RABBITMQ_USERNAME" \
  --set-string auth.password="$RABBITMQ_PASSWORD" \
  --set-string auth.erlangCookie="$RABBITMQ_ERLANG_COOKIE"
```

## 如果 Pod 环境变量里取不到
先查看 RabbitMQ 相关环境变量：

```bash
kubectl exec -n middleware "$POD" -- sh -lc 'env | grep RABBITMQ'
```

Erlang Cookie 还可以尝试直接从文件读取：

```bash
kubectl exec -n middleware "$POD" -- sh -lc 'cat /opt/bitnami/rabbitmq/.erlang.cookie'
```

说明：

- `RABBITMQ_ERL_COOKIE` 常常还能从文件取回
- `RABBITMQ_PASSWORD` 如果 Pod 已经重建过，未必还能拿到原始明文
- 如果旧密码彻底丢失，而 PVC 还保留，后续恢复会更麻烦

## 排查命令补充

### 查看 Release 当前 values

```bash
helm get values rabbitmq-cluster-msg -n middleware
```

### 查看相关 Secret

```bash
kubectl get secret -n middleware | grep rabbitmq-cluster-msg
kubectl get secret -n middleware rabbitmq-cluster-msg -o yaml
```

### 查看升级后状态

```bash
kubectl get pods -n middleware | grep rabbitmq-cluster-msg
kubectl rollout status sts/rabbitmq-cluster-msg -n middleware
kubectl logs -n middleware rabbitmq-cluster-msg-0
```

## 经验总结

1. `--reuse-values` 不会自动复用 Secret 中的密码
2. Bitnami RabbitMQ 升级时，旧凭据必须显式传入
3. Secret 被误删后，最优先的恢复来源是正在运行的 Pod
4. 在 Secret 未恢复前，不要轻易重启 Pod
5. 对使用 PVC 的 RabbitMQ 来说，凭据和磁盘数据是绑定关系，不能随意改密码硬顶升级

## 建议

- 对关键中间件的 Secret 做备份
- 升级前先导出当前 Secret
- Helm 升级命令固定保留旧凭据传参模板
- 涉及 RabbitMQ、MySQL、Redis、PostgreSQL 这类有状态组件时，先确认 Secret、PVC、StatefulSet 三者关系再操作
