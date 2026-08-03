# 批量清理docker容器日志文件内容

# 批量清理docker容器日志文件内容
docker ps -aq --no-trunc | xargs docker inspect --format='{{.LogPath}}'|xargs truncate -s 0



> 更新: 2024-07-04 08:58:24  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/yxbk5luouvwa0kqv>