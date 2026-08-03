# gcloud授权

gcloud auth activate-service-account svc-bkt-logs@prj-tiq-damm-p-wallyt-01.iam.gserviceaccount.com --key-file=./svc-bkt-logs@prj-tiq-damm-p-wallyt-01.json

GOOGLE_APPLICATION_CREDENTIALS=xxxx/key.json

```
gcsfuse -o allow_other --file-mode=777 --dir-mode=777 --foreground --debug_fuse --debug_gcs bkt-tiq-damm-p-logs /mnt/gcs-logs-bucket/
```

```
gcsfuse -o allow_other --file-mode=777 --dir-mode=777  bkt-tiq-damm-p-logs /mnt/gcs-logs-bucket/
```

# 挂载是减少缓存时间

```
gcsfuse -o allow_other   --implicit-dirs   --stat-cache-ttl 10s   --type-cache-ttl 10s   --file-mode=777   --dir-mode=777   bkt-tiq-damm-p-logs   /mnt/gcs-logs-bucket
```

## 挂载kuw生产tiqmo_logs

```
 gcsfuse -o allow_other   --implicit-dirs   --stat-cache-ttl 10s   --type-cache-ttl 10s   --file-mode=777   --dir-mode=777  tiqmo-p-wallyt-logs-bucket   /mnt/tiqmo_logs/
```

# gfuse卸载

```
fusermount -u /mnt/gcs-logs-bucket
```