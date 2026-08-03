# 服务pod获取shell权限，用于安装想要的命令

# 安装开启hostnetwork权限的pod
:::info
apiVersion: v1

kind: Pod

metadata:

  name: shell-demo

spec:

  volumes:

  - name: shared-data

    emptyDir: {}

  containers:

  - name: nginx

    image: nginx

    volumeMounts:

    - name: shared-data

      mountPath: /usr/share/nginx/html

  hostNetwork: true

  dnsPolicy: Default

:::

# 部署pod
```shell
kubectl apply -f https://k8s.io/examples/application/shell-demo.yaml
```

#   
 <font style="color:rgb(34, 34, 34);">Get a shell to the running container:</font>
```shell
kubectl exec --stdin --tty shell-demo -- /bin/bash

```

# **<font style="color:rgb(0, 0, 0);">在shell中，尝试安装使用其他命令  
</font>**<font style="color:rgb(34, 34, 34);">In your shell, experiment with other commands. Here are some examples:</font>
```shell
# You can run these example commands inside the container

ls / 
cat /proc/mounts 
cat /proc/1/maps 
apt-get update 
apt-get install -y tcpdump 
tcpdump 
apt-get install -y lsof 
lsof 
apt-get install -y procps 
ps aux 
ps aux | grep nginx 
```

# 参考文档
[https://kubernetes.io/docs/tasks/debug/debug-application/get-shell-running-container/](https://kubernetes.io/docs/tasks/debug/debug-application/get-shell-running-container/)



> 更新: 2024-07-10 11:14:09  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xcryzobq0zusgfzh>