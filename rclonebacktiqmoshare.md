# rclone back tiqmo share

rclone copy \

/mnt/tiqmo_share/ \

--no-traverse \

--create-empty-src-dirs \

--max-age 2h \

--exclude 'dumpfile/' \

--exclude 'wallyt-tms-service-*.hprof' \

--exclude '.snapshot/' \

remote:jed-prod-bkt-k8s-share \

--progress \

--stats-one-line \

--max-stats-groups 10 \

--fast-list \

--buffer-size 50Mi \

--multi-thread-streams 50 \

--transfers 50 \

--checkers 12 \

--retries 10 \

--oos-chunk-size 16Mi \

--oos-upload-concurrency 8 \

--oos-attempt-resume-upload \

--oos-upload-cutoff 10Mi \

--multi-thread-cutoff 16Mi \

--log-level INFO \

--log-file /filesbackup/backup_tiqmoshare/rclone.log \

--timeout 3600s \

--oos-no-check-bucket \

--oos-leave-parts-on-error \

--oos-storage-tier Archive





> 更新: 2025-10-10 09:42:28  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/cxaix6ngflla1c88>