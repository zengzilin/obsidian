# Kubespray 2.20 / Kubernetes 1.24 证书续期与 kubelet.conf 重建

## 适用场景

- 集群由 `kubeadm + Kubespray 2.20` 部署
- Kubernetes 版本为 `1.24.x`
- 需要手动续期 control-plane 证书
- 续期后某个 control-plane 节点出现 `NotReady`
- `journalctl -u kubelet` 中出现 `system:anonymous`、`nodes is forbidden`、`node not found` 等报错

## 一、检查证书有效期

在每个 control-plane 节点执行：

```bash
sudo kubeadm certs check-expiration
```

## 二、手动续期 control-plane 证书

在每个 control-plane 节点逐台执行：

```bash
sudo /usr/local/bin/kubeadm certs renew all
```

通过 Ansible 对单台节点执行也可以：

```bash
ansible -i inventory/<inventory>/inventory.ini kube_control_plane -b -m shell \
  -a "/usr/local/bin/kubeadm certs renew all" -l <node_name>
```

说明：

- 这一步会续期 `apiserver`、`apiserver-kubelet-client`、`admin.conf`、`controller-manager.conf`、`scheduler.conf`、`front-proxy-client`
- 如果输出里有 `MISSING! certificate ... etcd`，不一定是失败
- 对于 Kubespray 集群，etcd 证书很多时候由 Kubespray 的 `etcd-secrets` 任务管理，不完全由 `kubeadm certs renew all` 负责

## 三、续期后重启 control-plane 静态 Pod

续期完成后，需要让组件重新加载新证书。

在对应 control-plane 节点执行：

```bash
sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/
sleep 25
sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/

sudo mv /etc/kubernetes/manifests/kube-controller-manager.yaml /tmp/
sleep 25
sudo mv /tmp/kube-controller-manager.yaml /etc/kubernetes/manifests/

sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/
sleep 25
sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/
```

如果该节点本地运行了 `etcd`，并且 etcd 证书也已更新，再重启 `etcd.yaml`：

```bash
sudo mv /etc/kubernetes/manifests/etcd.yaml /tmp/
sleep 25
sudo mv /tmp/etcd.yaml /etc/kubernetes/manifests/
```

## 四、常见故障：节点变成 NotReady

如果续期后节点状态变成 `NotReady`，例如：

```bash
kubectl get nodes
```

出现：

```text
node1   NotReady   control-plane   ...
```

先查看 `kubelet` 日志：

```bash
sudo journalctl -u kubelet -n 100 --no-pager
```

如果看到以下特征报错：

```text
User "system:anonymous" cannot create resource "nodes"
User "system:anonymous" cannot get resource "leases"
pods ... is forbidden
node "node1" not found
```

说明 `kubelet` 没有正确使用客户端证书访问 apiserver，通常需要手动重建 `/etc/kubernetes/kubelet.conf`。

## 五、手动重建 /etc/kubernetes/kubelet.conf

以下步骤以 `node1` 为例。

### 1. 备份旧文件

```bash
sudo cp -a /etc/kubernetes/kubelet.conf /etc/kubernetes/kubelet.conf.bak.$(date +%F-%H%M%S)
```

### 2. 删除旧的 kubelet 客户端证书

不要直接用 `rm kubelet-client-*`，否则可能触发 `Argument list too long`。

使用：

```bash
sudo find /var/lib/kubelet/pki -maxdepth 1 -type f -name 'kubelet-client-*' -delete
```

可先查看将删除的文件：

```bash
sudo find /var/lib/kubelet/pki -maxdepth 1 -type f -name 'kubelet-client-*'
```

### 3. 导出 kubeadm 配置

在能正常访问集群的 control-plane 节点执行：

```bash
export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl -n kube-system get cm kubeadm-config -o jsonpath='{.data.ClusterConfiguration}' > /tmp/kubeadm-cluster-config.yaml
```

### 4. 重新生成 node1 的 kubelet kubeconfig

```bash
sudo /usr/local/bin/kubeadm kubeconfig user \
  --config /tmp/kubeadm-cluster-config.yaml \
  --org system:nodes \
  --client-name system:node:node1 \
  > /tmp/kubelet.conf
```

检查 apiserver 地址是否正确：

```bash
grep server: /tmp/kubelet.conf
grep server: /etc/kubernetes/admin.conf
```

如果和 `admin.conf` 不一致，需要手工改成一致。

### 5. 覆盖 kubelet.conf

```bash
sudo cp /tmp/kubelet.conf /etc/kubernetes/kubelet.conf
sudo chown root:root /etc/kubernetes/kubelet.conf
sudo chmod 600 /etc/kubernetes/kubelet.conf
```

### 6. 重启 kubelet，让其重新生成轮转证书

```bash
sudo systemctl restart kubelet
sleep 10
```

检查是否已经生成：

```bash
sudo ls -l /var/lib/kubelet/pki/kubelet-client-current.pem
```

### 7. 将 kubelet.conf 改为引用轮转证书文件

编辑 `/etc/kubernetes/kubelet.conf`，把：

```yaml
client-certificate-data: ...
client-key-data: ...
```

改成：

```yaml
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```

如果使用命令替换：

```bash
sudo sed -i '/client-certificate-data:/c\    client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem' /etc/kubernetes/kubelet.conf
sudo sed -i '/client-key-data:/c\    client-key: /var/lib/kubelet/pki/kubelet-client-current.pem' /etc/kubernetes/kubelet.conf
```

### 8. 再次重启 kubelet

```bash
sudo systemctl restart kubelet
```

### 9. 验证恢复结果

```bash
sudo journalctl -u kubelet -n 50 --no-pager
kubectl get nodes
```

预期结果：

- `system:anonymous` 相关报错消失
- 节点从 `NotReady` 恢复为 `Ready`

## 六、如果需要使用 Kubespray 处理 etcd 证书

如果确认问题在 `etcd` 证书，而不是 `kubelet.conf`，可以谨慎对单节点执行：

```bash
ansible-playbook -i inventory/<inventory>/inventory.ini cluster.yml -b \
  --limit <node_name> --tags etcd-secrets,etcd
```

注意：

- 不建议在故障未定位清楚时直接全量执行 `cluster.yml`
- 优先单节点、限标签处理

## 七、排查命令汇总

查看节点状态：

```bash
kubectl get nodes
kubectl describe node <node_name>
```

查看 kubelet 日志：

```bash
sudo journalctl -u kubelet -n 200 --no-pager
```

查看 control-plane 容器：

```bash
sudo /usr/local/bin/crictl ps -a | egrep 'kube-apiserver|etcd|kube-controller-manager|kube-scheduler'
```

查看 kubelet 证书文件：

```bash
sudo ls -l /var/lib/kubelet/pki/
sudo openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem -noout -dates -subject
```

## 八、经验结论

- `kubeadm certs renew all` 主要续期 control-plane 证书
- Kubespray 集群里的 etcd 证书不一定由 `kubeadm certs renew all` 管理
- 如果续期后节点出现 `system:anonymous`，优先检查并重建 `/etc/kubernetes/kubelet.conf`
- 对 control-plane 节点续期后，必须重启对应静态 Pod 才会生效

## 九、如何避免再次出现续期后节点 NotReady

### 1. 优先使用常规升级，而不是“证书到期后再补救”

如果集群能保持定期升级，优先走 `kubeadm upgrade` 或 Kubespray 的升级流程。

原因：

- `kubeadm upgrade apply`
- `kubeadm upgrade node`

会自动续期由 kubeadm 管理的证书，并同时处理控制面静态 Pod 和 kubelet 配置刷新。

建议：

- 至少保持 Kubernetes patch 版本定期升级
- 尽量不要让集群连续超过 1 年不升级
- 对 Kubespray 集群，优先使用 `upgrade-cluster.yml` 或受控的 `cluster.yml` 升级路径，而不是只在证书过期时临时手工处理

### 2. 提前做证书到期巡检和告警

不要等控制面证书已经过期后再处理。

建议至少每周或每月执行一次：

```bash
sudo kubeadm certs check-expiration
```

对于 kubelet 客户端证书，也可以巡检：

```bash
sudo openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem -noout -dates -subject
```

建议结合以下方式提前告警：

- 距离过期 `90` 天告警
- 距离过期 `60` 天升级为高优先级
- 距离过期 `30` 天禁止再拖延

如果环境里已经部署了证书监控组件，也可以直接接入现有告警体系。

### 3. 统一检查所有节点的 kubelet.conf 写法

这次 `node1` 变成 `system:anonymous`，本质上是 kubelet 客户端证书轮转链路没有正常工作。

官方建议 kubelet 使用：

```yaml
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```

而不是长期保留：

```yaml
client-certificate-data: ...
client-key-data: ...
```

建议在所有节点排查一次：

```bash
grep -E 'client-certificate|client-key' /etc/kubernetes/kubelet.conf
```

如果发现仍然是内嵌式 `*-data` 写法，提前修正为引用 `/var/lib/kubelet/pki/kubelet-client-current.pem`，避免未来证书轮转失败时 kubelet 退化成匿名访问。

### 4. 续期时按“单节点、可回退、逐步验证”的方式执行

不要在所有 control-plane 节点同时续期和同时重启。

推荐顺序：

1. 先确认集群当前健康
2. 只处理一个 control-plane 节点
3. 续期证书
4. 重启该节点 control-plane 静态 Pod
5. 验证该节点恢复 `Ready`
6. 再处理下一个 control-plane 节点

每处理一台都要执行：

```bash
kubectl get nodes
kubectl get pod -A -o wide | grep <node_name>
sudo journalctl -u kubelet -n 50 --no-pager
```

### 5. 在变更前备份关键文件

至少备份以下内容：

```bash
sudo tar czf /root/k8s-cert-backup-$(date +%F-%H%M%S).tar.gz \
  /etc/kubernetes \
  /var/lib/kubelet/pki
```

建议额外导出：

```bash
kubectl -n kube-system get cm kubeadm-config -o yaml > /root/kubeadm-config-$(date +%F-%H%M%S).yaml
```

这样即使某台节点续期后异常，也能更快比对和回退。

### 6. 分清 kubeadm 证书和 etcd 证书的边界

对 Kubespray 集群，不要默认认为：

```bash
kubeadm certs renew all
```

一定覆盖所有 etcd 证书。

建议提前确认：

- `etcd` 是否本地静态 Pod 部署
- `etcd` 是否由 Kubespray 的 `etcd-secrets` 管理
- 当前节点是否真的运行 etcd

如果 etcd 是单独管理的，应该单独准备 etcd 证书续期方案，不要等到控制面恢复异常后再排查。

### 7. 最好先在测试环境演练一次

如果生产集群年龄较大，或者长期没有升级，建议先在测试环境完整演练以下流程：

- 证书有效期检查
- 单节点续期
- 静态 Pod 重启
- kubelet.conf 修复演练
- etcd 证书处理演练

这样生产操作时，命令顺序和回退路径都会更清楚。
