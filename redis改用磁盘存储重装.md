# redis改用磁盘存储重装

# <font style="color:#0f4761;">1. backup newredis-cluster</font>
helm get values newredis-cluster > newredis_values.yaml -n middleware

# <font style="color:#0f4761;">2.monifiy the values.yaml </font>
cp  newredis_values.yaml values.yaml



vim values.yaml  #change storageClass to “oci-bv”

…

global:

storageClass: oci-bv 

….

# <font style="color:#0f4761;">3. Uninstall</font><font style="color:#0f4761;">  </font><font style="color:#0f4761;">newredis-cluster </font>
helm uninstall newredis-cluster -n middleware

kubectl delete pvc redis-data-newredis-cluster-0 redis-data-newredis-cluster-1 redis-data-newredis-cluster-2 redis-data-newredis-cluster-3 redis-data-newredis-cluster-4 redis-data-newredis-cluster-5 -n middleware

# <font style="color:#0f4761;">4. Reinstall newredis-cluster</font>
helm install newredis-cluster bitnami/redis-cluster  --version=8.3.8  -f values.yaml -n middleware



# <font style="color:#0f4761;">5.backup the game redis</font>


helm get values redis-game > redis-game_values.yaml -n middleware

cp  redis-game_values.yaml values.yaml



# <font style="color:#0f4761;">6.monifiy the values.yaml</font>


vim values.yaml  #change storageClass to “oci-bv”

…

global:

storageClass: oci-bv 

….

# <font style="color:#0f4761;">7. Uninstall  game redis-cluster</font>
helm uninstall redis-game -n middleware



kubectl delete pvc redis-data-redis-game-cluster-redis-cluster-0  redis-data-redis-game-cluster-redis-cluster-1  redis-data-redis-game-cluster-redis-cluster-2  redis-data-redis-game-cluster-redis-cluster-3  redis-data-redis-game-cluster-redis-cluster-4  redis-data-redis-game-cluster-redis-cluster-5 -n middleware

# <font style="color:#0f4761;">8.Reinstall game redis-cluster</font>
helm install redis-game bitnami/redis-cluster  --version=8.3.8  -f  values.yaml -n middleware

# 9.check the result
helm list -n middleware

kubectl get po -n middleware







> 更新: 2025-04-21 11:24:46  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/fzbwvestbbltc2vn>