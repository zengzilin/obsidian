# gfuse 操作挂载tiqmo logs

# gcloud授权
gcloud auth activate-service-account svc-bkt-logs@prj-tiq-damm-p-wallyt-01.iam.gserviceaccount.com --key-file=./svc-bkt-logs@prj-tiq-damm-p-wallyt-01.json



<font style="color:rgb(36, 36, 36);">GOOGLE_APPLICATION_CREDENTIALS=xxxx/key.json</font>

<font style="color:rgb(36, 36, 36);"></font>

```plain
gcsfuse -o allow_other --file-mode=777 --dir-mode=777 --foreground --debug_fuse --debug_gcs bkt-tiq-damm-p-logs /mnt/gcs-logs-bucket/
```

<font style="color:rgb(36, 36, 36);"></font>

```plain
gcsfuse -o allow_other --file-mode=777 --dir-mode=777  bkt-tiq-damm-p-logs /mnt/gcs-logs-bucket/
```

# 挂载是减少缓存时间
```plain
gcsfuse -o allow_other   --implicit-dirs   --stat-cache-ttl 10s   --type-cache-ttl 10s   --file-mode=777   --dir-mode=777   bkt-tiq-damm-p-logs   /mnt/gcs-logs-bucket
```

## 挂载kuw生产tiqmo_logs
```plain
 gcsfuse -o allow_other   --implicit-dirs   --stat-cache-ttl 10s   --type-cache-ttl 10s   --file-mode=777   --dir-mode=777  tiqmo-p-wallyt-logs-bucket   /mnt/tiqmo_logs/
```

# gfuse卸载
```plain
fusermount -u /mnt/gcs-logs-bucket
```



> 更新: 2026-03-30 11:10:24  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ip2dt1vtm47c6fc5>