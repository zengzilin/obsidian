# GCP k8s 1.32集群自动升级后redis部署报错 may require authorization: server message: insufficient_scope: authorization failed

![1752724438827-c6db3f41-e72e-4369-aa8b-494c9c4e49f7.png](./img/yoJvmGEv5n3D-408/1752724438827-c6db3f41-e72e-4369-aa8b-494c9c4e49f7-182097.png)

**<font style="color:#DF2A3F;">ps :其他环境用旧版本正常，</font>**

# 创建一个假的仓库secret
kubectl -n default create secret docker-registry dockerhub-anon   --docker-server=[https://index.docker.io/v1/](https://index.docker.io/v1/)   --docker-username=anonymous   --docker-password=anonymous   --docker-email=anonymous@example.com

# values里面配置引用该secrets
:::info
cluster:

  init: true

  nodes: 6

  replicas: 1

clusterDomain: cluster.local

global:

  imageRegistry: ""

<font style="color:#DF2A3F;">  imagePullSecrets:</font>

<font style="color:#DF2A3F;">    - dockerhub-anon</font>

  redis:

    password: tiqmo

  <font style="color:#DF2A3F;">storageClass: standard-rwo</font>

metrics:

  <font style="color:#DF2A3F;">enabled: false</font>

persistence:

  enabled: true

  size: 10Gi

readinessProbe:

  enabled: true

redis:

  configmap: logfile /bitnami/redis/data/redis.log

  podAntiAffinityPreset: hard

service:

  ports:

    redis: 6379

  type: NodePort

volumePermissions:

  enabled: true

:::



# 除了安装secret还需要删除旧版本redis
helm uninstall redis-cluster-test

# 安装新版本redis


```plain
kubectl delete pvc redis-data-redis-cluster-test-0 redis-data-redis-cluster-test-1 redis-data-redis-cluster-test-2 redis-data-redis-cluster-test-3 redis-data-redis-cluster-test-4 redis-data-redis-cluster-test-5
```



```plain
 helm install redis-cluster-test bitnami/redis-cluster  --version=8.8.1 -f  values.yaml
```



> 更新: 2025-07-17 14:25:12  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/fb2k04hxgi7sm3ce>