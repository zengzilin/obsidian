# agocd autopilot相关操作

argocd autopilot-bootstrap识别不了域名，tls校验不通过

 kubectl get app -n argocd

NAME                  SYNC STATUS   HEALTH STATUS

autopilot-bootstrap   Unknown       Healthy

[wallytjmpadmin@cin-tiq-damm-u-wallyt-jmp ~]$ argocd app get autopilot-bootstrap

Name:               argocd/autopilot-bootstrap

Project:            default

Server:             [https://kubernetes.default.svc](https://kubernetes.default.svc)

Namespace:          argocd

URL:                [https://localhost:8080/applications/autopilot-bootstrap](https://localhost:8080/applications/autopilot-bootstrap)

Source:

- Repo:             [https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git](https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git)

  Target:

  Path:             bootstrap

SyncWindow:         Sync Allowed

Sync Policy:        Automated (Prune)

Sync Status:        Unknown

Health Status:      Healthy



CONDITION        MESSAGE                                                                                                                                                                                                                                                                                                                  LAST TRANSITION

ComparisonError  Failed to load target state: failed to generate manifest for source 1 of 1: rpc error: code = Unknown desc = failed to list refs: Get "[https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git/info/refs?service=git-upload-pack":](https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git/info/refs?service=git-upload-pack":) tls: failed to verify certificate: x509: certificate signed by unknown authority  2026-01-08 13:13:06 +0300 +03

# 合成CA
 cat "CA Bundle/Sectigo_Public_Server_Authentication_CA_DV_R36.pem" "CA Bundle/Sectigo_Public_Server_Authentication_Root_R46.pem" "CA Bundle/USERTrust_RSA_Certification_Authority.pem" > git.tiqmopayment.com.crt



openssl x509 -in git.tiqmopayment.com.crt -noout -text | grep "CA:"

                CA:TRUE, pathlen:0



# 创建secret
kubectl -n argocd create configmap argocd-tls-certs-cm \

  --from-file=git.tiqmopayment.com=star.tiqmopayment.com.crt \

  --dry-run=client -o yaml | kubectl apply -f -



kubectl -n argocd rollout restart deploy argocd-repo-server

kubectl -n argocd rollout status deploy argocd-repo-server



:::info
无效，重启之后证书会被删除

:::



# ，跳过证书，添加仓库
argocd repo server 重启之后证书会被删除，添加仓库的最快方法跳过证书，添加仓库

```plain
 argocd repo add https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git \
    --username shawn@wallyt.com \
    --password  P@ssw0rd@4 \
    --insecure-skip-server-verification


```

# 创建app也需要提前添加app仓库地址
    argocd repo add [https://git.tiqmopayment.com/preprod/jed-preprod-manifest-repo-ksa.git](https://git.tiqmopayment.com/preprod/jed-preprod-manifest-repo-ksa.git) \

    --username shawn@wallyt.com \

    --password  P@ssw0rd@4 \

    --insecure-skip-server-verification



# autopilot命令创建删除app
前提 导入变量

export PATH=/root/.local/bin:/root/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin/

export GIT_REPO=[https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git](https://git.tiqmopayment.com/preprod/u-argocd-autopilot.git)

export GIT_TOKEN=gRk1A7S3oyDmNftueYxD



创建app

url不要写错和sorce path不要写错



argocd-autopilot app create preprod-app-frontend --app [https://git.tiqmopayment.com/preprod/jed-preprod-manifest-repo-ksa.git/tiqmo_frontend](https://git.tiqmopayment.com/preprod/jed-preprod-manifest-repo-ksa.git/tiqmo_frontend) -p dam-preprod  --type dir --dest-namespace frontend

指定project一定要指定ns,不指定默认为default ns

删除app命令

 argocd-autopilot app delete preprod-app-account -p dam-preprod





创建 sftp

argocd-autopilot app create infra-app-sftp --app [https://git.tiqmopayment.com/sysops/jed-main-infrastructure-repo.git/jed-middleware/sftp](https://git.tiqmopayment.com/sysops/jed-main-infrastructure-repo/-/tree/main/jed-middleware/sftp) -p dam-preprod  --type dir --dest-namespace middleware



创建 nacos 

 argocd-autopilot app create infra-app-nacos --app [https://git.tiqmopayment.com/sysops/jed-main-infrastructure-repo.git/jed-middleware/nacos-cluster](https://git.tiqmopayment.com/sysops/jed-main-infrastructure-repo.git/jed-middleware/nacos-cluster) -p dam-preprod --type dir --dest-namespace middleware

删除  infra-app-nacos

argocd-autopilot app delete infra-app-nacos -p dam-preprod



创建dam-preprod-infra-common (因为ingress涉及多个命名空间，所以ns指定为"")

argocd-autopilot app create infra-common --app [https://git.tiqmopayment.com/sysops/jed-main-infrastructure-repo.git/common](https://git.tiqmopayment.com/sysops/jed-main-infrastructure-repo.git/jed-main-infrastructure-repo/common)  -p dam-preprod --type dir --dest-namespace ""

删除 infra-common

argocd-autopilot app delete infra-common -p dam-preprod



#  Argo CD Autopilot Bootstrap 流程图（概念图）  
       +----------------+

       |  Git Repo       | <---- 用户提供，包含 bootstrap manifests

       +----------------+

                 |

                 | HTTPS/SSH (+ CA 证书或 SSH key)

                 v

       +----------------+

       |  Argo CD Repo   | 

       |  Server         |

       +----------------+

       | - 读取 ConfigMap TLS

       | - 拉取仓库 manifests

       +----------------+

                 |

                 v

       +----------------+

       |  Autopilot      |

       |  Bootstrap App  |

       +----------------+

       | - 自动创建 AppProjects

       | - 自动创建 Apps

       | - Auto Sync Policy

       +----------------+

                 |

                 v

       +----------------+

       |  Cluster /      |

       |  Namespaces     |

       +----------------+

       | - 部署资源

       | - 设置健康状态

       +----------------+

                 |

                 v

       +----------------+

       |  Argo CD UI / CLI

       |  状态查看

       +----------------+

# 堡垒机登录argocd
argocd login localhost:8080   --username admin   --password 5fkwyLwX3C1nSsIJ   --insecure





> 更新: 2026-01-19 16:32:19  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/dgie6u58g048s556>