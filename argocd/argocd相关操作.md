# argocd 相关操作

#  autopilot创建初始化仓库
export GIT_TOKEN=gRk1A7S3oyDmNftueYxD

切换到root用户的话，需要autopilot命令工具加入环境变量

export PATH=$PATH:/usr/local/bin/

argocd-autopilot repo bootstrap --repo [http://git.tiqmopayment.com/preprod/u-argocd-autopilot.git](http://git.tiqmopayment.com/preprod/u-argocd-autopilot.git) --branch main --namespace argocd

argocd-autopilot repo bootstrap --repo [http://git.tiqmopayment.com/preprod/u-argocd-autopilot.git](http://git.tiqmopayment.com/preprod/u-argocd-autopilot.git) --namespace argocd



# 批量创建argocd application
sh create-frontend-app.sh ci-ksa-frontend dev [https://gitlab.wallyt.com/devops/tiqmo/configs/deploy-config/deploy-config-tiqmo.git](https://gitlab.wallyt.com/devops/tiqmo/configs/deploy-config/deploy-config-tiqmo.git)  [https://gitlab.wallyt.com/devops/tiqmo/configs/service-config/service-config-tiqmo.git](https://gitlab.wallyt.com/devops/tiqmo/configs/service-config/service-config-tiqmo.git)  [https://repo.swifer.co/artifactory/charts-local](https://repo.swifer.co/artifactory/charts-local) [https://kubernetes.default.svc](https://kubernetes.default.svc)



# argocd获取admin初始密码
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo



# argocd修改密码
argocd login 192.168.4.108:30495

<font style="color:rgb(34, 34, 34);">argocd account update-password --account admin --current-password <当前密码> --new-password <新密码> </font>

<font style="color:rgb(34, 34, 34);"></font>

# <font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);">命令行获取project配置</font>
## argocd命令行获取project列表
argocd proj list

## k8s命令获取project对象
 kubectl get  appproject -n argocd

kubectl get appproject ksa-stress -o yaml  -n argocd



# argocd升级后重新生成密码
```plain
# 安装（一次即可）
pip3 install bcrypt 
# 生成并更新
python3 -c " import bcrypt, base64, subprocess, sys, time; new_pass = 'Tiqmo2025' hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt(rounds=10)) mtime = str(int(time.time())) patch = { 'data': { 'admin.password': base64.b64encode(hashed).decode(), 'admin.passwordMtime': base64.b64encode(mtime.encode()).decode() } } import json, os; cmd = ['kubectl', 'patch', 'secret', 'argocd-secret', '-n', 'argocd', '-p', json.dumps(patch)] os.execvp(cmd[0], cmd) "
```



> 更新: 2026-01-09 15:54:15  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/tsx2zb7m9h8ywayw>