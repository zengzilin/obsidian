# helm kube-prometheus 升级被锁定

\[opc@jed-preprod-vm-jump prometheus]$ helm history prometheus -n monitoring

REVISION        UPDATED                         STATUS          CHART                           APP VERSION     DESCRIPTION

```
   Upgrade complete
```

65              Wed May 28 03:39:40 2025        superseded      kube-prometheus-stack-70.1.1    v0.81.0         Upgrade complete

66              Tue Jul 29 06:35:49 2025        superseded      kube-prometheus-stack-70.1.1    v0.81.0         Upgrade complete

67              Thu Jul 31 04:57:32 2025        superseded      kube-prometheus-stack-70.1.1    v0.81.0         Upgrade complete

68              Thu Oct 16 11:49:28 2025        superseded      kube-prometheus-stack-70.1.1    v0.81.0         Upgrade complete

69              Thu Oct 16 12:41:17 2025        deployed        kube-prometheus-stack-70.1.1    v0.81.0         Upgrade complete

70              Thu Oct 16 12:45:26 2025        failed          kube-prometheus-stack-70.1.1    v0.81.0         Upgrade "prometheus" failed: context canceled

<font style="color:#DF2A3F;">71              Thu Oct 16 12:48:32 2025        pending-upgrade kube-prometheus-stack-70.1.1    v0.81.0         Preparing upgrade</font>

### <font style="color:rgb(0, 0, 0);">1. 确认锁定状态并清理</font>

<font style="color:rgb(0, 0, 0);">当前</font><font style="color:rgb(0, 0, 0);"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">pending-upgrade</font></code><font style="color:rgb(0, 0, 0);"> </font><font style="color:rgb(0, 0, 0);">状态会阻止新操作，需要手动清理对应的 Helm 状态 secret：</font>

**<font style="color:rgba(0, 0, 0, 0.85);">bash</font>**

```bash
# 清理 prometheus Release 的锁定 secret（版本 71 对应的状态记录）
kubectl delete secret -n monitoring sh.helm.release.v1.prometheus.v71
```


> 更新: 2025-10-17 15:06:29  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/eelye8kgy8gy3qf1>