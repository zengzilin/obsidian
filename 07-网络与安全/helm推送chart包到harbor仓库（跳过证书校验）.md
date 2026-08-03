# helm推送chart包到 harbor仓库（跳过证书校验）

# harbor加了证书校验之后 推送oci helm chart报错
**<font style="color:#DF2A3F;">helm push nginx-svr-1.2.2.tgz oci://harbor-tiqmo.wallyt.net/ksa_check</font>**

Error: failed to do request: Head "[https://harbor-tiqmo.wallyt.net/v2/ksa_check/nginx-svr/blobs/sha256:ab9e7c7cd2d97989153a39cd52e97511cf54920a359544df233e07849ccdaf6f":](https://harbor-tiqmo.wallyt.net/v2/ksa_check/nginx-svr/blobs/sha256:ab9e7c7cd2d97989153a39cd52e97511cf54920a359544df233e07849ccdaf6f":) tls: failed to verify certificate: x509: certificate signed by unknown authority



# helm 3.10执行以下命令报错
helm push nginx-svr-1.2.2.tgz oci://harbor-tiqmo.wallyt.net/ksa_check --insecure-skip-tls-verify

命令报错：没有这个参数，我一直没想到要升级版本！！！！

<font style="color:#DF2A3F;">（helm 11以下版本没有这个参数 --insecure-skip-tls-verify）</font>

<font style="color:#DF2A3F;"></font>

# <font style="color:#DF2A3F;">将helm升级到helm 11或以上版本，重新执行命令</font>
<font style="color:#DF2A3F;">helm push nginx-svr-1.2.2.tgz oci://harbor-tiqmo.wallyt.net/ksa_check --insecure-skip-tls-verify</font>

<font style="color:#DF2A3F;">helm chart包推送成功！</font>

额外小知识

helm registry login -u=admin -p=Harbor12345 [https://harbor-tiqmo.wallyt.net](https://harbor-tiqmo.wallyt.net) --insecure



 push ../nginx-svr-1.2.2.tgz oci://harbor-tiqmo.wallyt.net/ksa_check --kube-insecure-skip-tls-verify

Error: failed to do request: Head "[https://harbor-tiqmo.wallyt.net/v2/ksa_check/nginx-svr/blobs/sha256:99ba34b8d8651fc7d1d47254d4772c0af4e53a2a92c7ce417ee2dd270ebc45f2":](https://harbor-tiqmo.wallyt.net/v2/ksa_check/nginx-svr/blobs/sha256:99ba34b8d8651fc7d1d47254d4772c0af4e53a2a92c7ce417ee2dd270ebc45f2":) x509: certificate signed by unknown authority









> 更新: 2024-09-10 16:49:08  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/wa75xwmockqyo2kr>