# Kubernetes 节点 NFS 孤儿挂载排查与处理

## 适用场景

适用于下面这类问题：

- 某些 Kubernetes 节点存在 NFS 挂载，另一些节点没有。
- `kubectl get nodes` 显示控制平面节点为 `Ready,SchedulingDisabled`，但节点上仍然可能残留挂载。
- 节点执行 `df -h`、`findmnt <挂载点>`、`ls <挂载目录>` 时卡住。
- 需要判断该挂载是否为当前业务在用，还是 kubelet 历史残留的孤儿挂载。

## 本次问题现象

- `node1` 没有看到 NFS 挂载。
- `node2`、`node3` 看到 NFS 挂载。
- `node2` 上执行 `df -h` 卡住。
- `node2`、`node3` 当前运行的 Pod 主要为：
  - `filebeat`
  - `ingress-nginx-controller`
  - `calico-node`
  - `kube-apiserver`
  - `kube-controller-manager`
  - `kube-scheduler`
  - `kube-proxy`
  - `nodelocaldns`
  - `prometheus-node-exporter`
  - `x509-certificate-exporter`
- `nfs-subdir-external-provisioner` 不在 `node2`、`node3`，而是在 `node5`。

## 核心结论

- 节点是否出现 NFS 挂载，不取决于它是不是管理节点，而取决于该节点上是否有 Pod 实际使用了 NFS 卷。
- 本次 `node2` 的 NFS 挂载不是系统 `fstab` 挂载，也不是当前存活 Pod 正在使用的挂载。
- 该挂载是 kubelet 历史遗留的 **孤儿 NFS 挂载**。
- `df -h` 卡住的直接原因是该 NFS 使用了 `hard` 挂载参数，NFS 服务端异常时，对挂载点的访问会阻塞。

## 相关配置定位

本次定位到的挂载源与仓库中的 PV/PVC 配置一致：

- PV/PVC 文件：`clusters/dockermanagement-master/pvc.yaml`
- PV 名称：`tiqmo-logs-pv`
- PVC 名称：`mgr-logs-pvc`
- StorageClass：`tiqmo-log`
- NFS Server：`192.168.4.47`
- NFS Path：`/data/k8s-check-ksa/tiqmo_logs`
- 挂载参数：`hard`、`nfsvers=3`

对应配置片段：

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: tiqmo-logs-pv
spec:
  storageClassName: tiqmo-log
  mountOptions:
    - hard
    - nfsvers=3
  nfs:
    server: 192.168.4.47
    path: /data/k8s-check-ksa/tiqmo_logs
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mgr-logs-pvc
  namespace: mgr
```

## 排查过程

### 1. 先排除 NFS provisioner 自身运行在控制平面节点

```bash
kubectl get pods -A -o wide | egrep 'nfs|provisioner'
```

本次实际结果：

```text
local-path-storage  local-path-provisioner-68cf6f7f8-khvlx               node6
mgr                 nfs-subdir-external-provisioner-new-56d6b4dcc7-jhcm6 node5
```

结论：

- `nfs-subdir-external-provisioner` 不在 `node2`、`node3`
- 因此 `node2`、`node3` 上的 NFS 挂载不是 provisioner Pod 自己带上去的

### 2. 查看 `node2`、`node3` 当前实际运行的 Pod

```bash
for n in node2 node3; do
  echo "===== $n ====="
  kubectl get pods -A --field-selector spec.nodeName=$n -o wide
done
```

本次结果显示 `node2`、`node3` 上没有 `mgr` namespace 的业务 Pod。

结论：

- 当前没有证据表明 `node2`、`node3` 上仍有业务 Pod 正在消费 `mgr-logs-pvc`
- 挂载更可能是历史残留

### 3. 在节点侧查看 NFS 挂载来源

不要先用 `df -h`，优先使用：

```bash
findmnt -rn -t nfs,nfs4 -o TARGET,SOURCE,FSTYPE,OPTIONS
cat /proc/self/mountinfo | grep -E ' nfs | nfs4 '
```

本次在 `node2` 上得到：

```text
/var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv 192.168.4.47:/data/k8s-check-ksa/tiqmo_logs nfs rw,relatime,vers=3,...,hard,...
```

以及：

```text
1706 97 0:188 / /var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv rw,relatime shared:514 - nfs 192.168.4.47:/data/k8s-check-ksa/tiqmo_logs rw,vers=3,...,hard,...
```

结论：

- 挂载点位于 `/var/lib/kubelet/pods/.../volumes/kubernetes.io~nfs/...`
- 这说明它不是 `/etc/fstab` 静态挂载
- 这是 kubelet 为某个 Pod 动态挂上的卷

### 4. 用 Pod UID 反查该挂载是否仍对应活跃 Pod

从挂载路径中提取 Pod UID：

```text
ff285068-7d91-44b2-81d5-9f8d3f1d6614
```

执行：

```bash
kubectl get pods -A \
  -o custom-columns=UID:.metadata.uid,NS:.metadata.namespace,NAME:.metadata.name,NODE:.spec.nodeName \
  --no-headers | grep ff285068-7d91-44b2-81d5-9f8d3f1d6614
```

本次结果：

```text
无输出
```

结论：

- 集群中已经不存在 UID 为 `ff285068-7d91-44b2-81d5-9f8d3f1d6614` 的 Pod
- 该 NFS 挂载属于 **孤儿挂载**

## 为什么 `df -h` 会卡住

本次 NFS PV 使用了以下参数：

```yaml
mountOptions:
  - hard
  - nfsvers=3
```

影响如下：

- `hard` 表示 NFS 请求失败时不会快速返回，而是持续重试。
- 如果 NFS 服务端 `192.168.4.47` 响应慢、网络中断、导出路径异常，访问挂载点的命令就可能卡住。
- 典型会卡住的命令：
  - `df -h`
  - `findmnt <挂载点>`
  - `ls <挂载点>`
  - `stat <挂载点>`
  - `du <挂载点>`

## 安全处理步骤

### 1. 不要直接访问卡死的挂载目录

避免执行：

```bash
findmnt /var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv
ls /var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv
stat /var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv
```

这些命令都可能被 NFS 阻塞。

### 2. 使用 `/proc/self/mountinfo` 做只读确认

```bash
grep 'ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv' /proc/self/mountinfo
grep '192.168.4.47:/data/k8s-check-ksa/tiqmo_logs' /proc/self/mountinfo
```

### 3. 对孤儿挂载执行强制懒卸载

```bash
TARGET='/var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv'
umount -fl "$TARGET"
```

参数说明：

- `-l`：lazy unmount，先从命名空间摘除
- `-f`：对失联 NFS 更适合

如果前台执行卡住，可改后台执行：

```bash
nohup umount -fl "$TARGET" >/tmp/umount-stale-nfs.log 2>&1 &
```

### 4. 卸载后验证

仍然不要先访问挂载路径本身，先看挂载元信息：

```bash
grep 'ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv' /proc/self/mountinfo
grep '192.168.4.47:/data/k8s-check-ksa/tiqmo_logs' /proc/self/mountinfo
```

如果没有输出，说明挂载已经从当前命名空间摘掉。

之后再执行：

```bash
df -h -x nfs -x nfs4
```

说明：

- `df -h -x nfs -x nfs4` 可以临时避开 NFS 挂载，避免再次卡住

## `node3` 的处理方式

对 `node3` 执行相同流程：

```bash
findmnt -rn -t nfs,nfs4 -o TARGET,SOURCE,FSTYPE,OPTIONS
cat /proc/self/mountinfo | grep -E ' nfs | nfs4 '
```

如果 `node3` 也存在类似路径：

```text
/var/lib/kubelet/pods/<UID>/volumes/kubernetes.io~nfs/<volume-name>
```

则继续：

```bash
kubectl get pods -A \
  -o custom-columns=UID:.metadata.uid,NS:.metadata.namespace,NAME:.metadata.name,NODE:.spec.nodeName \
  --no-headers | grep <UID>
```

判断原则：

- 有输出：说明该挂载仍可能被活跃 Pod 使用，不能直接卸载
- 无输出：说明该挂载是孤儿挂载，可按本文件步骤处理

## 处理时的注意事项

- 不要因为 `SchedulingDisabled` 就默认认为控制平面节点没有卷挂载。
- 不要在未确认前直接删除 `/var/lib/kubelet/pods/<UID>` 目录。
- 先确认 Pod UID 是否仍然存在，再决定是否卸载。
- 对失联 NFS，优先用 `grep /proc/self/mountinfo` 排查，少用会触发真实 I/O 的命令。
- 如果存在当前业务 Pod 仍在使用该卷，应该先恢复 NFS 连通性，而不是直接卸载。

## 快速命令清单

### 查看 NFS provisioner 在哪里

```bash
kubectl get pods -A -o wide | egrep 'nfs|provisioner'
```

### 查看某节点上的所有 Pod

```bash
kubectl get pods -A --field-selector spec.nodeName=node2 -o wide
kubectl get pods -A --field-selector spec.nodeName=node3 -o wide
```

### 查看节点上的 NFS 挂载

```bash
findmnt -rn -t nfs,nfs4 -o TARGET,SOURCE,FSTYPE,OPTIONS
cat /proc/self/mountinfo | grep -E ' nfs | nfs4 '
```

### 通过 UID 反查 Pod 是否还存在

```bash
kubectl get pods -A \
  -o custom-columns=UID:.metadata.uid,NS:.metadata.namespace,NAME:.metadata.name,NODE:.spec.nodeName \
  --no-headers | grep <POD_UID>
```

### 卸载孤儿 NFS 挂载

```bash
umount -fl /var/lib/kubelet/pods/<POD_UID>/volumes/kubernetes.io~nfs/<VOLUME_NAME>
```

### 临时避开 NFS 查看磁盘

```bash
df -h -x nfs -x nfs4
```

## 本次案例最终判断

- `node1` 没有 NFS 挂载，不是异常。
- `node2` 的挂载为 kubelet 历史残留的孤儿 NFS 挂载。
- `node2` 挂载来源为：

```text
192.168.4.47:/data/k8s-check-ksa/tiqmo_logs
```

- 对应挂载点为：

```text
/var/lib/kubelet/pods/ff285068-7d91-44b2-81d5-9f8d3f1d6614/volumes/kubernetes.io~nfs/tiqmo-logs-pv
```

- 对应 Pod UID 已不存在于集群中。
- 可以按孤儿挂载方式执行 `umount -fl` 清理。
