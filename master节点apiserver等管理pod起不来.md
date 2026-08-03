# master节点apiserver等管理pod起不来

# kubelet启动报错，所以管理节点apiserver 等pods起不来
![1749381841283-90b0856b-9ba8-4017-9bf6-d5410123176e.png](./img/Rsxs_mhsBjZWQsKD/1749381841283-90b0856b-9ba8-4017-9bf6-d5410123176e-490498.png)

# kubelet起步来的原因
![1749381881632-a2ae0def-c645-422f-903f-2e3aef8ebbc9.png](./img/Rsxs_mhsBjZWQsKD/1749381881632-a2ae0def-c645-422f-903f-2e3aef8ebbc9-652936.png)

## <font style="color:rgb(28, 31, 35);">解决方案</font>
<font style="color:rgb(28, 31, 35);"># 编辑 kubelet 环境配置文件 vi /etc/kubernetes/kubelet.env # 注释掉 bootstrap-kubeconfig 行，修改为： KUBELET_ARGS="--config=/etc/kubernetes/kubelet-config.yaml \ --kubeconfig=/etc/kubernetes/kubelet.conf \ --container-runtime=remote \ --container-runtime-endpoint=unix:////var/run/containerd/containerd.sock \ --runtime-cgroups=/systemd/system.slice \ " # 保存后重启 kubelet systemctl daemon-reload systemctl restart kubelet</font>

![1749381925435-bfc8f72f-eff8-46b7-abe6-310d88d3083d.png](./img/Rsxs_mhsBjZWQsKD/1749381925435-bfc8f72f-eff8-46b7-abe6-310d88d3083d-075651.png)

## 重启kubelet成功
```bash
systemctl daemon-reload
systemctl restart kubelet
```

![1749382195424-066ef520-0993-4d50-8869-93ac655b219f.png](./img/Rsxs_mhsBjZWQsKD/1749382195424-066ef520-0993-4d50-8869-93ac655b219f-134657.png)

# 再次查看apiserver等三个管理pod
![1749382144395-68741cd5-8ee8-4ede-b8d8-c5c1e314282c.png](./img/Rsxs_mhsBjZWQsKD/1749382144395-68741cd5-8ee8-4ede-b8d8-c5c1e314282c-443685.png)

## master节点还是not ready
还有三个calico等容器起不来，尝试重启其他calico、proxy容器

/usr/local/bin/crictl rmp dc0a8554d3849

Removed sandbox dc0a8554d3849

[root@node1 bin]# /usr/local/bin/crictl rmp 807b2d3c22acb

Removed sandbox 807b2d3c22acb

[root@node1 bin]# /usr/local/bin/crictl rmp a80e762ea7155

Removed sandbox a80e762ea7155

<font style="color:#DF2A3F;">没有生效</font>

<font style="color:#DF2A3F;">重启节点也没有生效</font>

# <font style="color:#DF2A3F;">kubespray搭建的集群重启apiserver、scheduler、controller manager pod的方法</font>
 sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/ && sleep 20 && sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests

sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/ && sleep 20 && sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests

sudo mv /etc/kubernetes/manifests/kube-controller-manager.yaml /tmp/ && sleep 20 && sudo mv /tmp/kube-controller-manager.yaml /etc/kubernetes/manifests





> 更新: 2025-06-09 09:53:36  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ahd4ag0vt3lyohsz>