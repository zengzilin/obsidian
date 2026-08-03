# containerd拉取私有仓库镜像报错x509: certificate signed by unknown authority



当使用crictl尝试从使用HTTPS的私有Harbor仓库拉取镜像时，由于默认缺少证书，操作会失败。解决方法包括下载证书到指定目录，修改containerd配置文件添加endpoint、ca_file、用户名和密码，然后重启containerd服务。完成这些步骤后，可以成功拉取镜像。

![1725355348686-39b1ab10-0f10-48f7-b685-5a84effb5b04.png](./img/L2Hz-pDQxaREAeAm/1725355348686-39b1ab10-0f10-48f7-b685-5a84effb5b04-891126.png)

# 1.修改containerd配置，添加harbor仓库地址和鉴权相关配置（密码和证书）
[root@node9 containerd]# cat config.toml

:::info
version = 2

root = "/var/lib/containerd"

state = "/run/containerd"

oom_score = 0



[grpc]

  max_recv_message_size = 16777216

  max_send_message_size = 16777216



[debug]

  level = "info"



[metrics]

  address = ""

  grpc_histogram = false



[plugins]

  [plugins."io.containerd.grpc.v1.cri"]

    sandbox_image = "docker.repo.swifer.co/pause:3.6"

    max_container_log_line_size = -1

    [plugins."io.containerd.grpc.v1.cri".containerd]

      default_runtime_name = "runc"

      snapshotter = "overlayfs"

      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]

        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]

          runtime_type = "io.containerd.runc.v2"

          runtime_engine = ""

          runtime_root = ""



          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]

            systemdCgroup = true

    [plugins."io.containerd.grpc.v1.cri".registry]

      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]

        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]

          endpoint = ["https://registry-1.docker.io"]

       # 新增harbor仓库

        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."harbor-tiqmo.wallyt.net"]

          endpoint = ["https://harbor-tiqmo.wallyt.net"]

        # 新增配置文件路径

        [plugins."io.containerd.grpc.v1.cri".registry.configs]

          [plugins."io.containerd.grpc.v1.cri".registry.configs."harbor-tiqmo.wallyt.net".tls]

            ca_file = "/etc/containerd/certs.d/harbor-tiqmo.wallyt.net/ca.crt"

        [plugins."io.containerd.grpc.v1.cri".registry.configs."harbor-tiqmo.wallyt.net".auth]

           username = "admin"

            password = "Harbor12345"



:::





在/etc/containerd/certs.d/

新建域名文件夹，用来存放域名证书，和hosts.toml配置

![1745310560934-8b9dbd18-900d-483c-ac86-81b09e3c9e78.png](./img/L2Hz-pDQxaREAeAm/1745310560934-8b9dbd18-900d-483c-ac86-81b09e3c9e78-011298.png)

![1745310393759-fffb91c0-827c-4350-875c-e51b77532f11.png](./img/L2Hz-pDQxaREAeAm/1745310393759-fffb91c0-827c-4350-875c-e51b77532f11-224147.png)



# 2.重启contianerd服务
 systemctl restart containerd.service && systemctl status containerd.service

sh batchRestart.sh restartAll wallet



# 3.2025年更新说明
新版的k8s 1.31 containerd 默认有证书路径相关的配置，而且按上述配置有报错，不生效。另外节点太多，所以直接配置host.:wq

跳过证书鉴权算了

![1745749953677-ddc15bf6-0c1c-4868-818f-83d29d4a48f6.png](./img/L2Hz-pDQxaREAeAm/1745749953677-ddc15bf6-0c1c-4868-818f-83d29d4a48f6-779612.png)

vi /etc/containerd/certs.d/harbor-tiqmo.wallyt.net/hosts.toml

![1745749201479-eb2d4e4f-80ad-49e5-8466-6147894bca6d.png](./img/L2Hz-pDQxaREAeAm/1745749201479-eb2d4e4f-80ad-49e5-8466-6147894bca6d-646076.png)



> 更新: 2025-04-27 18:35:15  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/zk8gs1r9hbiume63>