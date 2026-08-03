# GKE 手动升级k8s版本

官方文档

[https://cloud.google.com/kubernetes-engine/docs/how-to/upgrading-a-cluster?hl=en](https://cloud.google.com/kubernetes-engine/docs/how-to/upgrading-a-cluster?hl=en)

# 获取当前支持的k8s版本信息
**<font style="color:#DF2A3F;">升级顺序，只能一个版本一个版本往上升级！！</font>**

**<font style="color:#DF2A3F;">本次升级 从1.31->1.32->1.33</font>**

# **<font style="color:#DF2A3F;">升级control plane</font>**
## 获取control plane k8s版本
```plain
gcloud container get-server-config     --location=us-central1-a  #control plane所在区域
```



## 指定升级版本
```plain
gcloud container clusters upgrade cluster-2 \
    --master \
    --location=us-central1-a \
    --cluster-version=1.32.9-gke.1575000
```

<font style="color:#DF2A3F;">命令遇到了报错：</font>

![1764744343461-894783ae-c287-45f1-894a-bd8ebd8b1741.png](./img/EvsLQ1_MSoUCeRax/1764744343461-894783ae-c287-45f1-894a-bd8ebd8b1741-531833.png)

因为创建集群时，我指定的默认Release channel为<font style="color:#DF2A3F;">Regular，会自动更新</font>

**需要改为**<font style="color:#DF2A3F;">no channel 才可以手动更新</font>

![1764744299762-905a289a-d165-4bda-8d4c-d2c87a1eaf15.png](./img/EvsLQ1_MSoUCeRax/1764744299762-905a289a-d165-4bda-8d4c-d2c87a1eaf15-393787.png)

修改后，命令正常执行

![1764744535616-32865241-20c4-46d8-b2a4-3643b29ebfa7.png](./img/EvsLQ1_MSoUCeRax/1764744535616-32865241-20c4-46d8-b2a4-3643b29ebfa7-825882.png)



# 升级节点池版本
命令行升级

```plain
gcloud container clusters upgrade CLUSTER_NAME \
  --node-pool=NODE_POOL_NAME \
  --location=CONTROL_PLANE_LOCATION \
  --cluster-version VERSION
```

在GCP平台升级

![1764747026297-ff11055b-3ce6-49ce-b2f8-475b8d82a3ac.png](./img/EvsLQ1_MSoUCeRax/1764747026297-ff11055b-3ce6-49ce-b2f8-475b8d82a3ac-835304.png)

# control plane升级到1.33
可以在console界面选择推荐版本

![1764749428947-8805bb37-3cb8-443c-98f4-583a4c4ae9dd.png](./img/EvsLQ1_MSoUCeRax/1764749428947-8805bb37-3cb8-443c-98f4-583a4c4ae9dd-761851.png)

在upgrade 监控界面可以当前看到升级的状态

![1764749654113-2da0bacc-b09b-4a70-95f2-66db0b4de7d3.png](./img/EvsLQ1_MSoUCeRax/1764749654113-2da0bacc-b09b-4a70-95f2-66db0b4de7d3-958257.png)



> 更新: 2025-12-03 16:14:41  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ktizxzlgqgsy5flx>