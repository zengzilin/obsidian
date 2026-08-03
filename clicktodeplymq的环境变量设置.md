# click to deply mq的环境变量设置

for the app. In most cases, you can use the `default` namespace.

```shell

export APP_INSTANCE_NAME=rabbitmq-1

export NAMESPACE=default

```

Set the number of replicas:

```shell

export REPLICAS=3

```

For the persistent disk provisioning of the RabbitMQ StatefulSets, you will need to:

* Set the StorageClass name. Check your available options using the command below:

  * `kubectl get storageclass`

  * Or check how to create a new StorageClass in \[Kubernetes Documentation]\(<https://kubernetes.io/docs/concepts/storage/storage-classes/#the-storageclass-res>                                                                                                                                                              ource)

* Set the persistent disk's size. The default disk size is "5Gi".

```shell

export RABBITMQ_STORAGE_CLASS="standard" # provide your StorageClass name if not "standard"

export RABBITMQ_PERSISTENT_DISK_SIZE="5Gi"

```

Set or generate the

[Erlang cookie]([https://www.rabbitmq.com/clustering.html#erlang-cookie).]\(https://www.rabbitmq.com/clustering.html#erlang-cookie).) The

cookie must be encoded in base64.

```shell

export RABBITMQ_ERLANG_COOKIE=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1 | tr -d '\n' | base64)

```

Set the username for the app:

```shell

export RABBITMQ_DEFAULT_USER=rabbit

```

Set or generate a password. The value must be encoded in base64.

```shell

export RABBITMQ_DEFAULT_PASS=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1 | tr -d '\n' | base64)

```

Enable Stackdriver Metrics Exporter:

> **NOTE:** Your GCP project must have Stackdriver enabled. If you are using a

> non-GCP cluster, you cannot export metrics to Stackdriver.

By default, application does not export metrics to Stackdriver. To enable this

option, change the value to `true`.

```shell

export METRICS_EXPORTER_ENABLED=false



```


> 更新: 2025-11-12 09:24:07  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gdd38kfez2d36vie>