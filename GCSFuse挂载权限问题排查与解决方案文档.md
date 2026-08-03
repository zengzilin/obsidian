# GCS Fuse 挂载权限问题排查与解决方案文档

# **<font style="color:rgb(6, 10, 38);"></font>**

## **<font style="color:rgb(6, 10, 38);">1. 问题背景</font>**

<font style="color:rgb(6, 10, 38);">在 Kubernetes (GKE) 环境中，部署了一个以非 Root 用户 (</font><code><font style="color:rgb(6, 10, 38);">runAsUser: 1001</font></code><font style="color:rgb(6, 10, 38);">) 运行的应用容器。该容器需要通过 GCS Fuse 挂载 Google Cloud Storage (GCS) Bucket 到本地路径 (</font><code><font style="color:rgb(6, 10, 38);">/mnt/gcs-bucket</font></code><font style="color:rgb(6, 10, 38);">)，并使用</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">rsync</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">同步日志文件。</font>

**<font style="color:rgb(6, 10, 38);">核心现象：</font>**

* <font style="color:rgb(6, 10, 38);">当容器以</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">root</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(UID 0) 运行时，挂载和写入操作正常。</font>
* <font style="color:rgb(6, 10, 38);">当容器切换到普通用户 (</font><code><font style="color:rgb(6, 10, 38);">UID 1001</font></code><font style="color:rgb(6, 10, 38);">) 运行时，</font><code><font style="color:rgb(6, 10, 38);">rsync</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">报错：</font><code><font style="color:rgb(6, 10, 38);">mkstemp failed: Operation not permitted</font></code><font style="color:rgb(6, 10, 38);">，无法创建临时文件。</font>

***

## **<font style="color:rgb(6, 10, 38);">2. 根本原因分析</font>**

### **<font style="color:rgb(6, 10, 38);">2.1 权限不匹配机制</font>**

* **<font style="color:rgb(6, 10, 38);">Root 用户的特权</font>**<font style="color:rgb(6, 10, 38);">：Linux 中 Root 用户通常可以绕过文件所有权检查。当 GCS Fuse 默认以 Root 身份挂载时（或 Sidecar 为 Root），Root 用户可以直接在挂载点写入数据。</font>
* **<font style="color:rgb(6, 10, 38);">普通用户的限制</font>**<font style="color:rgb(6, 10, 38);">：</font>
  * <font style="color:rgb(6, 10, 38);">GCS Fuse 在未指定</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">uid/gid</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">参数时，默认将挂载点内的所有文件所有权设为</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">Root (0:0)</font>**<font style="color:rgb(6, 10, 38);">。</font>
  * <font style="color:rgb(6, 10, 38);">应用容器以</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">UID 1001</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">运行，对于它来说，挂载点</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/mnt/gcs-bucket</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">属于“其他人”(Others)。</font>
  * <font style="color:rgb(6, 10, 38);">若默认挂载权限为</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">755</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(其他人只读)，</font><code><font style="color:rgb(6, 10, 38);">UID 1001</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">既不是所有者也不是组成员，因此</font>**<font style="color:rgb(6, 10, 38);">没有写权限</font>**<font style="color:rgb(6, 10, 38);">。</font>
  * <code><font style="color:rgb(6, 10, 38);">rsync</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">默认策略是先创建临时文件 (</font><code><font style="color:rgb(6, 10, 38);">.filename.xxxxx</font></code><font style="color:rgb(6, 10, 38);">) 再重命名，由于缺乏写权限，</font><code><font style="color:rgb(6, 10, 38);">mkstemp</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">系统调用失败。</font>

### **<font style="color:rgb(6, 10, 38);">2.2 结论</font>**

<font style="color:rgb(6, 10, 38);">这不是 IAM (云资源) 权限问题（因为 Root 能成功），而是</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">Linux 文件系统权限 (UID/GID) 与 GCS Fuse 挂载参数不匹配</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">导致的。</font>

***

## **<font style="color:rgb(6, 10, 38);">3. 解决方案 (Kubernetes 环境)</font>**

### **<font style="color:rgb(6, 10, 38);">Pod使用了pvc的解决方案：在 PVC 中添加 </font>**<code><font style="color:rgb(6, 10, 38);">mountOptions</font></code>

<font style="color:rgb(6, 10, 38);">由于你使用的是</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">persistentVolumeClaim</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">引用方式，你需要修改</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">PVC (PersistentVolumeClaim)</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">或者其对应的</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">PV (PersistentVolume)</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">定义，在其中加入</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">mountOptions</font></code><font style="color:rgb(6, 10, 38);">。</font>

<font style="color:rgb(6, 10, 38);">但是，GKE 的自动注入模式有时允许直接在</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">Pod 的 annotation</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">中传递特定配置，或者更稳妥的方式是：</font>**<font style="color:rgb(6, 10, 38);">直接修改 PVC 的定义</font>**<font style="color:rgb(6, 10, 38);">。</font>

#### **<font style="color:rgb(6, 10, 38);">🚀</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 方法一：修改 PVC (推荐，最稳妥)</font>**

<font style="color:rgb(6, 10, 38);">找到你的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">gcs-wallyt-logs-pvc-performance</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">这个 PVC 的 YAML 定义，添加</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">mountOptions</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">字段。</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: gcs-wallyt-logs-pvc-performance
spec:
  accessModes:
    - ReadWriteMany # GCS Fuse 通常支持 RWX
  resources:
    requests:
      storage: 5Gi # 这里的 size 对 GCS 没实际意义，只是占位
  storageClassName: standard # 或者你的 gcsfuse storage class
  # 👇 关键：在这里添加 mountOptions
  mountOptions:
    - implicit-dirs
    - uid=1001
    - gid=1001
    - file-mode=664
    - dir-mode=775
  selector:
    matchLabels:
      # 如果有特定的 PV 标签选择器
      bucket: your-bucket-name
```

### Pod不使用pvc的方案

### **<font style="color:rgb(6, 10, 38);">方案 A：显式指定 UID/GID 挂载参数 (推荐)</font>**

<font style="color:rgb(6, 10, 38);">通过修改 Kubernetes 资源配置，强制 GCS Fuse 将挂载点文件所有权映射为应用用户 (</font><code><font style="color:rgb(6, 10, 38);">1001</font></code><font style="color:rgb(6, 10, 38);">)。</font>

#### **<font style="color:rgb(6, 10, 38);">实施步骤</font>**

<font style="color:rgb(6, 10, 38);">由于使用了 GKE 的自动注入注解 (</font><code><font style="color:rgb(6, 10, 38);">gke-gcsfuse/volumes: "true"</font></code><font style="color:rgb(6, 10, 38);">) 且引用了 PVC，最灵活的方法是</font>**<font style="color:rgb(6, 10, 38);">直接在 Deployment 中使用 CSI Volume 定义</font>**<font style="color:rgb(6, 10, 38);">，绕过 PVC 的限制。</font>

**<font style="color:rgb(6, 10, 38);">修改</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">daemonset.yaml</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>****<font style="color:rgb(6, 10, 38);">(或 deployment.yaml) 的</font>****<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">volumes</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">部分：</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">yaml</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
volumes:
  - name: k8slogs
    hostPath:
      path: /tiqmo_logs
      type: ''
  
  # 修改前：引用 PVC
  # - name: gcs-volume
  #   persistentVolumeClaim:
  #     claimName: gcs-wallyt-logs-pvc-performance

  # 修改后：直接使用 CSI 驱动并配置 mountOptions
  - name: gcs-volume
    csi:
      driver: gcsfuse.csi.storage.gke.io
      volumeAttributes:
        bucketName: "YOUR_BUCKET_NAME"  # 替换为实际 Bucket 名称
        # 关键配置：指定 uid, gid 及权限模式
        mountOptions: "implicit-dirs,uid=1001,gid=1001,file-mode=664,dir-mode=775,temp-dir=/tmp"
```

**<font style="color:rgb(6, 10, 38);">参数解释：</font>**

* <code><font style="color:rgb(6, 10, 38);">uid=1001,gid=1001</font></code><font style="color:rgb(6, 10, 38);">: 将挂载点内所有文件伪装成属于用户 1001。</font>
* <code><font style="color:rgb(6, 10, 38);">file-mode=664,dir-mode=775</font></code><font style="color:rgb(6, 10, 38);">: 设置默认文件和目录权限，确保组可写。</font>
* <code><font style="color:rgb(6, 10, 38);">temp-dir=/tmp</font></code><font style="color:rgb(6, 10, 38);">: 指定临时文件目录为容器内可写的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/tmp</font></code><font style="color:rgb(6, 10, 38);">。</font>

### **<font style="color:rgb(6, 10, 38);">方案 B：优化 Rsync 命令 (双重保险)</font>**

<font style="color:rgb(6, 10, 38);">即使修复了权限，建议在</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">rsync</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">命令中加入特定参数以适应对象存储特性。</font>

**<font style="color:rgb(6, 10, 38);">推荐命令：</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
rsync -avz --inplace --no-perms --no-owner --no-group /source/ /mnt/gcs-bucket/dest/
```

* <code><font style="color:rgb(6, 10, 38);">--inplace</font></code><font style="color:rgb(6, 10, 38);">: 直接更新目标文件，避免创建临时文件 (彻底规避</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">mkstemp</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">问题)。</font>
* <code><font style="color:rgb(6, 10, 38);">--no-perms --no-owner --no-group</font></code><font style="color:rgb(6, 10, 38);">: 忽略 Unix 权限同步，防止 GCS 不支持的属性导致错误。</font>


> 更新: 2026-03-07 04:07:35  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rnp9qh205byu1nfi>