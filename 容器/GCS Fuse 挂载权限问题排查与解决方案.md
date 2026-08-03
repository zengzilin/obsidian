## **问题背景**

在 Kubernetes (GKE) 环境中，部署了一个以非 Root 用户 (`runAsUser: 1001`) 运行的应用容器。该容器需要通过 GCS Fuse 挂载 Google Cloud Storage (GCS) Bucket 到本地路径 (`/mnt/gcs-bucket`)，并使用 `rsync` 同步日志文件。

**核心现象：**

- 当容器以 `root` (UID 0) 运行时，挂载和写入操作正常。
- 当容器切换到普通用户 (`UID 1001`) 运行时，`rsync` 报错：`mkstemp failed: Operation not permitted`，无法创建临时文件。

---

## **2. 根本原因分析**

### **2.1 权限不匹配机制**

- **Root 用户的特权**：Linux 中 Root 用户通常可以绕过文件所有权检查。当 GCS Fuse 默认以 Root 身份挂载时（或 Sidecar 为 Root），Root 用户可以直接在挂载点写入数据。
- **普通用户的限制**：

- GCS Fuse 在未指定 `uid/gid` 参数时，默认将挂载点内的所有文件所有权设为 **Root (0:0)**。
- 应用容器以 `UID 1001` 运行，对于它来说，挂载点 `/mnt/gcs-bucket` 属于“其他人”(Others)。
- 若默认挂载权限为 `755` (其他人只读)，`UID 1001` 既不是所有者也不是组成员，因此**没有写权限**。
- `rsync` 默认策略是先创建临时文件 (`.filename.xxxxx`) 再重命名，由于缺乏写权限，`mkstemp` 系统调用失败。
这不是 IAM (云资源) 权限问题（因为 Root 能成功），而是 **Linux 文件系统权限 (UID/GID) 与 GCS Fuse 挂载参数不匹配** 导致的。

---

## **3. 解决方案 (Kubernetes 环境)**

### **Pod使用了pvc的解决方案：在 PVC 中添加** `mountOptions`

由于你使用的是 `persistentVolumeClaim` 引用方式，你需要修改 **PVC (PersistentVolumeClaim)** 或者其对应的 **PV (PersistentVolume)** 定义，在其中加入 `mountOptions`。

但是，GKE 的自动注入模式有时允许直接在 **Pod 的 annotation** 中传递特定配置，或者更稳妥的方式是：**直接修改 PVC 的定义**。

#### **🚀** **方法一：修改 PVC (推荐，最稳妥)**

找到你的 `gcs-wallyt-logs-pvc-performance` 这个 PVC 的 YAML 定义，添加 `mountOptions` 字段。

**yaml**

编辑

```
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

### **方案 A：显式指定 UID/GID 挂载参数 (推荐)**

通过修改 Kubernetes 资源配置，强制 GCS Fuse 将挂载点文件所有权映射为应用用户 (`1001`)。

#### **实施步骤**

由于使用了 GKE 的自动注入注解 (`gke-gcsfuse/volumes: "true"`) 且引用了 PVC，最灵活的方法是**直接在 Deployment 中使用 CSI Volume 定义**，绕过 PVC 的限制。

**修改** `**daemonset.yaml**` **(或 deployment.yaml) 的** `**volumes**` **部分：**

**yaml**

编辑

```
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

**参数解释：**

- `uid=1001,gid=1001`: 将挂载点内所有文件伪装成属于用户 1001。
- `file-mode=664,dir-mode=775`: 设置默认文件和目录权限，确保组可写。
- `temp-dir=/tmp`: 指定临时文件目录为容器内可写的 `/tmp`。

### **方案 B：优化 Rsync 命令 (双重保险)**

即使修复了权限，建议在 `rsync` 命令中加入特定参数以适应对象存储特性。

**推荐命令：**

**bash**

编辑

```
rsync -avz --inplace --no-perms --no-owner --no-group /source/ /mnt/gcs-bucket/dest/
```

- `--inplace`: 直接更新目标文件，避免创建临时文件 (彻底规避 `mkstemp` 问题)。
- `--no-perms --no-owner --no-group`: 忽略 Unix 权限同步，防止 GCS 不支持的属性导致错误。