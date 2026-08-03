# k8s删除 Terminating 状态的资源

# <font style="color:rgb(77, 77, 77);">处于 Terminating 状态的 ns 经常无法正常删除。可尝试以下两种方法解决：</font>

<font style="color:rgb(77, 77, 77);">方法1、使用 --force 参数，</font><font style="color:red;">【delnsname 为要删除的命名空间，需要替换掉哦】</font>

```plain
kubectl delete ns delnsname --force --grace-period=0


1
```

<font style="color:rgb(77, 77, 77);">这种方法一般情况下是</font>[<font style="color:rgb(77, 77, 77);">有效的</font>](https://so.csdn.net/so/search?q=%E6%9C%89%E6%95%88%E7%9A%84\&spm=1001.2101.3001.7020)<font style="color:rgb(77, 77, 77);">。但在ns长时间处于Terminating的时候也会失效</font>

<font style="color:rgb(77, 77, 77);">方法2、修改</font><font style="color:rgb(77, 77, 77);"> </font><code><font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">finalize</font></code>

<font style="color:rgb(77, 77, 77);">a、导出ns的</font>[<font style="color:rgb(77, 77, 77);">json</font>](https://so.csdn.net/so/search?q=json\&spm=1001.2101.3001.7020)<font style="color:rgb(77, 77, 77);">文件</font><font style="color:red;">【delnsname 为要删除的命名空间，需要替换掉哦】</font>

```plain
kubectl get ns delnsname -o json > delnsname.json


1
```

<font style="color:rgb(77, 77, 77);">b、修改 json文件，删除 “finalizers” 内的 “kubernetes”</font>

```plain
vi delnsname.json


1
```

![1725861220953-b4c7f609-bcb2-45cb-8d1f-b2a9faf88410.png](./img/-cfX4ILtqBLQpMG9/1725861220953-b4c7f609-bcb2-45cb-8d1f-b2a9faf88410-636236.png)<font style="color:rgb(77, 77, 77);">\ </font><font style="color:rgb(77, 77, 77);">c、执行命令：</font><font style="color:red;">【delnsname 为要删除的命名空间，需要替换掉哦】</font>

```plain
kubectl replace --raw "/api/v1/namespaces/delnsname/finalize" -f ./delnsname.json


1
```

<font style="color:rgb(77, 77, 77);">再检查就发现已经被删除了</font>

# <font style="color:rgb(77, 77, 77);">删除terminating 状态的pvc</font>

## <font style="color:rgb(77, 77, 77);">--force强制删除</font>

```bash
kubectl delete pvc <pvc-name> -n <namespace> --force --grace-period=0
```

## <font style="color:rgb(77, 77, 77);">当强制删除不生效时可以用patch</font>

```bash
kubectl patch pvc <pvc-name> -n <namespace> -p '{"metadata":{"finalizers":null}}'
```

## **<font style="color:rgba(0, 0, 0, 0.5);">第三步 如果PVC仍未删除，检查关联的PV状态</font>**<font style="color:rgba(0, 0, 0, 0.5);">： 有时PV的finalizer也会导致PVC卡住，可以尝试移除PV的finalizer</font>

```bash
kubectl patch pv <pv-name> -p '{"metadata":{"finalizers":null}}'
```


> 更新: 2025-09-28 18:21:20  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rbyryt66l3l66euk>