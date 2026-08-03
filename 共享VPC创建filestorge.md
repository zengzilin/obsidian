# 共享VPC创建filestorge

## <font style="color:rgb(32, 33, 36);">在服务项目中的共享 VPC 网络上创建实例</font>
[https://cloud.google.com/filestore/docs/shared-vpc?hl=zh_CN&_gl=1*yyfh69*_ga*MTE0Nzg0NjE3Ni4xNzE2ODAwMzM2*_ga_WH2QY8WWF5*MTcxNzczODQyNy4yNS4xLjE3MTc3Mzg4NjAuNjAuMC4w&_ga=2.232301407.-1147846176.1716800336&_gac=1.241495734.1717577973.EAIaIQobChMI3cnNuYzEhgMVlQx7Bx32VwAHEAAYASAAEgK9W_D_Bw](https://cloud.google.com/filestore/docs/shared-vpc?hl=zh_CN&_gl=1*yyfh69*_ga*MTE0Nzg0NjE3Ni4xNzE2ODAwMzM2*_ga_WH2QY8WWF5*MTcxNzczODQyNy4yNS4xLjE3MTc3Mzg4NjAuNjAuMC4w&_ga=2.232301407.-1147846176.1716800336&_gac=1.241495734.1717577973.EAIaIQobChMI3cnNuYzEhgMVlQx7Bx32VwAHEAAYASAAEgK9W_D_BwE)



### <font style="color:rgb(32, 33, 36);">准备工作</font>
### [确保您的 Google Cloud 项目已启用结算功能](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-cn#console)。
### <font style="color:rgb(32, 33, 36);">创建包含宿主项目和关联服务项目的</font>[共享 VPC 网络](https://cloud.google.com/vpc/docs/provisioning-shared-vpc?hl=zh-cn)<font style="color:rgb(32, 33, 36);">。</font>
### 启用 Filestore and Service Networking API。
### [启用 API](https://console.cloud.google.com/flows/enableapi?apiid=file.googleapis.com%2C+servicenetworking.googleapis.com&hl=zh-cn&_ga=2.124703948.719022237.1717668019-1147846176.1716800336&_gac=1.241495734.1717577973.EAIaIQobChMI3cnNuYzEhgMVlQx7Bx32VwAHEAAYASAAEgK9W_D_BwE)
## <font style="color:rgb(32, 33, 36);">准备工作</font>
1. [确保您的 Google Cloud 项目已启用结算功能](https://cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-cn#console)。
2. <font style="color:rgb(32, 33, 36);">创建包含宿主项目和关联服务项目的</font>[共享 VPC 网络](https://cloud.google.com/vpc/docs/provisioning-shared-vpc?hl=zh-cn)<font style="color:rgb(32, 33, 36);">。</font>
3. 启用 Filestore and Service Networking API。

[启用 API](https://console.cloud.google.com/flows/enableapi?apiid=file.googleapis.com%2C+servicenetworking.googleapis.com&hl=zh-cn&_ga=2.124703948.719022237.1717668019-1147846176.1716800336&_gac=1.241495734.1717577973.EAIaIQobChMI3cnNuYzEhgMVlQx7Bx32VwAHEAAYASAAEgK9W_D_BwE)





> 更新: 2024-06-07 14:27:08  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gk41266udgnz2u4s>