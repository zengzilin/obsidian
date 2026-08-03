# 在 Docker 部署的 GitLab 环境中，若要让 gitlab.rb 配置生效但不重启所有服务，可通过以下步骤实现：

1. <font style="color:rgba(0, 0, 0, 0.85) !important;">进入 GitLab 容器内部</font>

<font style="color:rgb(28, 31, 35);"></font>

<font style="color:rgb(28, 31, 35);">docker exec -it gitlab /bin/bash</font>

<font style="color:rgb(28, 31, 35);"></font>

2. <font style="color:rgba(0, 0, 0, 0.85) !important;">执行配置重新加载命令</font><font style="color:rgb(28, 31, 35);">  
</font>

<font style="color:rgb(28, 31, 35);">gitlab-ctl reconfigure</font>

<font style="color:rgb(28, 31, 35);"></font>

3. <font style="color:rgba(0, 0, 0, 0.85) !important;">执行服务重载命令</font>

<font style="color:rgb(28, 31, 35);">gitlab-ctl hup  
</font><font style="color:rgb(28, 31, 35);"> </font>



> 更新: 2025-07-09 15:00:11  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/sgyii6erdk1kyb51>