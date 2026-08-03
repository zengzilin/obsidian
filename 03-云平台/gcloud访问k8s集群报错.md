# gcloud 访问 k8s集群报错

##  1.第一个报错：”gcloud container clusters get-credentials gke-tiq-kw-damm-u-wallyt-01 --region me-central2 --project prj-tiq-kw-damm-u-wallyt-01
Fetching cluster endpoint and auth data.

ERROR: gcloud crashed (TypeError): string indices must be integers, not 'str'



If you would like to report this issue, please run the following command:

  gcloud feedback“

<font style="color:#DF2A3F;">原因：</font>

**<font style="color:#DF2A3F;">linux用户权限不够，需要用sudo权限</font>**



# 2.使用sudo 执行gcloud 命令也报错
 第二个报错：sudo /usr/bin/gcloud container clusters get-credentials gke-tiq-kw-damm-u-wallyt-01 --region me-central2 --project prj-tiq-kw-damm-u-wallyt-01

ERROR: (gcloud.container.clusters.get-credentials) You do not currently have an active account selected.

Please run:

需要重新鉴权：

  $ gcloud auth login



to obtain new credentials.



If you have already logged in with a different account, run:



  $ gcloud config set account ACCOUNT



**<font style="color:#DF2A3F;">解决方法：</font>**

**<font style="color:#DF2A3F;">执行命令：sudo gcloud auth login --no-launch-browser</font>**

# 3.再次执行sudo /usr/bin/gcloud container clusters get-credentials gke-tiq-kw-damm-u-wallyt-01 --region me-central2 --project prj-tiq-kw-damm-u-wallyt-01
报错：

Fetching cluster endpoint and auth data.

CRITICAL: ACTION REQUIRED: gke-gcloud-auth-plugin, which is needed for continued use of kubectl, was not found or is not executable. Install gke-gcloud-auth-plugin for use with kubectl by following [https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#install_plugin](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#install_plugin)

kubeconfig entry generated for gke-tiq-kw-damm-u-wallyt-01.



解决方法：安装google-cloud-sdk-gke-gcloud-auth-plugin 

sudo   apt-get install google-cloud-sdk-gke-gcloud-auth-plugin 



rocky linux安装命令

sudo yum install google-cloud-sdk-gke-gcloud-auth-plugin



## sudo apt-get update报错
....

Err:3 [https://packages.cloud.google.com/apt](https://packages.cloud.google.com/apt) cloud-sdk InRelease

  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY C0BA5CE6DC6315A3

Get:5 [http://me-central2-a.gce.clouds.archive.ubuntu.com/ubuntu](http://me-central2-a.gce.clouds.archive.ubuntu.com/ubuntu) focal-backports InRelease [128 kB]

Reading package lists... Done

W: GPG error: [https://packages.cloud.google.com/apt](https://packages.cloud.google.com/apt) cloud-sdk InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY C0BA5CE6DC6315A3

## <font style="color:#DF2A3F;">update报错解决办法</font>
```bash
curl -o cloud-google-gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg     
gpg --no-default-keyring --keyring ./cloud.google.gpg --import cloud-google-gpg





sudo mv cloud.google.gpg /usr/share/keyrings     
```

sudo apt-get update



# 4.redhat 系统安装gcp工具报错
cat /etc/redhat-release

Red Hat Enterprise Linux release 9.7 (Plow)

<font style="color:#DF2A3F;">sudo yum update 之后安装还是报错</font>

<font style="color:#DF2A3F;">  dnf install wget -y Updating Subscription Management repositories. Google Cloud CLI 385 B/s | 487 B 00:01 Google Cloud CLI 9.6 kB/s | 975 B 00:00 Google Cloud CLI 388 B/s | 487 B 00:01 Error: Failed to download metadata for repo 'google-cloud-cli': repomd.xml GPG signature verification error: Bad GPG signature  </font>

![1765977087679-55e29e58-4e3a-4cdf-8bc6-46c15aada786.png](./img/-1PGsSzqA_XW7ApI/1765977087679-55e29e58-4e3a-4cdf-8bc6-46c15aada786-293477.png)

```plain
sudo  dnf install -y kubectl google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin  --nogpgcheck -y 
```

系统太新了，所以只有跳过GPG证书验证



# 5.生成kube config
gcloud container clusters get-credentials cluster-1 --location=us-central1-a





# 6.对于非公网的private集群
用root用户

sudo gcloud auth activate-service-account \  
gke-access-sa@prj-tiq-damm-u-wallyt-01.iam.gserviceaccount.com \  
--key-file="/home/wallytjmpadmin/gke-access-sa@prj-tiq-damm-u-wallyt-01.json"

sudo  gcloud config set project prj-tiq-damm-u-wallyt-01

 ---

或者用普通用户

gcloud auth activate-service-account \  
gke-access-sa@prj-tiq-damm-u-wallyt-01.iam.gserviceaccount.com \  
--key-file="/home/wallytjmpadmin/gke-access-sa@prj-tiq-damm-u-wallyt-01.json"

 

gcloud config set project prj-tiq-damm-u-wallyt-01



gcloud container clusters get-credentials gke-tiq-damm-u-wallyt-01 --region me-central2-a --project prj-tiq-damm-u-wallyt-01

 

**<font style="color:#DF2A3F;">公网的集群没有网络限制！！不安全！！1</font>**

通过IAM授权访问之后，而且通过连接认证之后还是不能访问集群。

![1765976282966-79030b80-1217-45d7-ba0b-94b95f0adaf5.png](./img/-1PGsSzqA_XW7ApI/1765976282966-79030b80-1217-45d7-ba0b-94b95f0adaf5-990368.png)

但是网络连通性没问题

![1765976298225-3936dec3-38c5-4e56-a777-6807faf34bf0.png](./img/-1PGsSzqA_XW7ApI/1765976298225-3936dec3-38c5-4e56-a777-6807faf34bf0-631369.png)

原因是私有集群对 第三方客户端网络有网络控制的配置

**<font style="color:#DF2A3F;">需要把第三方客户端（跳板机）网络加到GKE的授权网络中来！！！</font>**

## **授权网络配置的路径**
### **进入集群详情**
![1765976502001-ebe6c795-549d-4934-a421-8c961ea5a822.png](./img/-1PGsSzqA_XW7ApI/1765976502001-ebe6c795-549d-4934-a421-8c961ea5a822-796809.png)



### <font style="color:rgb(32, 33, 36);">进入Control Plane Networking</font>  
 添加授权网络（堡垒机的网段）
![1765976194296-49368e36-c93a-478d-b372-9291e624e3c3.png](./img/-1PGsSzqA_XW7ApI/1765976194296-49368e36-c93a-478d-b372-9291e624e3c3-006532.png)





# 访问k8s 集群成功
sudo /usr/bin/gcloud container clusters get-credentials gke-tiq-kw-damm-u-wallyt-01 --region me-central2 --project prj-tiq-kw-damm-u-wallyt-01

root用户可以访问，普通用户不能访问

将config配置拷贝到普通用户家目录

cp .kube/ /home/kwadmin/ -R

sudo chown kwadmin.kwadmin -R  .kube/

参考官方文档：

[https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#apt_1](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#apt_1)



> 更新: 2025-12-17 21:27:08  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gctpvuol2h7x22cp>