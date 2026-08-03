# 安装官方kafka集群

Redhat 8.10安装docker 29.1.3版本



sudo dnf -y install dnf-plugins-core

sudo dnf config-manager --add-repo [https://download.docker.com/linux/rhel/docker-ce.repo](https://download.docker.com/linux/rhel/docker-ce.repo)



sudo dnf install docker-ce-29.1.3-1.el8 docker-ce-cli-29.1.3-1.el8 containerd.io docker-buildx-plugin docker-compose-plugin



<font style="color:rgb(67, 76, 95);background-color:rgb(249, 250, 251);">sudo systemctl </font><font style="color:rgb(184, 110, 0);background-color:rgb(249, 250, 251);">enable</font><font style="color:rgb(67, 76, 95);background-color:rgb(249, 250, 251);"> --now docker</font>







> 更新: 2026-01-05 19:21:23  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ts6stbxtgz7g2ifc>