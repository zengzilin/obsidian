## 全局环境变量

首先需要确定 Cloudflare 上的各域名的 ZONE_ID 和生成一个 API Token 用于调用加密套件配置接口。

### Zone ID

`wallyt.net` 的 Zone ID 是 `21cff9a37816007944a216c8bfc52678`

`wepayez.com` 的 Zone ID 是 `6a253218ba44e1b02d483c5ae16c5db5`

### API Token

API Token 的生成位置在 Cloudflare Dashboard 右上角点击 **头像 - My Profile** 下，选 **API Tokens**，再点击蓝色按钮 **Create Token** 按照最小权限根据指导配置：

1. wallyt.net - **SSL and Certificates:Edit**
2. wepayez.com - **SSL and Certificates:Edit**

**注**：Token 有效期应当设置为短期，或在完成部署后手动吊销。



## 实施命令

变量名：

- `ZONE_ID` - 即在上文中提及的 Zone ID。
- `CLOUDFLARE_API_TOKEN` - 即在上文中提及的 API Token。
- `HOSTNAME` - 子域名，例如 `gatewaycftest.wepayez.com`。

### 应用自定义加密套件

通过以下接口为子域名配置自定义加密套件：

```sh
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/hostnames/settings/ciphers/$HOSTNAME" \
  --request PUT \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --header "Content-Type: application/json" \
  --d '{
    "value": [
        "ECDHE-ECDSA-AES128-GCM-SHA256",
        "ECDHE-RSA-AES128-GCM-SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
        "ECDHE-RSA-AES256-GCM-SHA384"
    ]
  }'

```

### 查看加密套件配置

当对子域名执行自定义加密套件配置后，可通过以下接口查看部署情况，以及具体配置细节：

```sh
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/hostnames/settings/ciphers" \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

### 


curl "https://api.cloudflare.com/client/v4/user/tokens/verify" \
-H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" 


curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/hostnames/settings/ciphers/$HOSTNAME"   --request PUT   --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN"   --header "Content-Type: application/json"   --data '{
      "value": [
        "ECDHE-ECDSA-AES128-GCM-SHA256",
          "ECDHE-RSA-AES128-GCM-SHA256",
          "ECDHE-ECDSA-AES256-GCM-SHA384",
         "ECDHE-RSA-AES256-GCM-SHA384"
        ]
     }'



{"success":true,"errors":[],"messages":[],"result":[{"hostname":"glue-stage.wallyt.net","value":["ECDHE-ECDSA-AES128-GCM-SHA256","ECDHE-RSA-AES128-GCM-SHA256","ECDHE-ECDSA-AES256-GCM-SHA384","ECDHE-RSA-AES256-GCM-SHA384"],"status":"active","created_at":"2026-04-22T03:35:48.284554Z","updated_at":"2026-04-22T06:31:48.682936Z"},{"hostname":"sit54-pay-main-k8s-test.wallyt.net","value":["ECDHE-ECDSA-AES128-GCM-SHA256","ECDHE-RSA-AES128-GCM-SHA256","ECDHE-ECDSA-AES256-GCM-SHA384","ECDHE-RSA-AES256-GCM-SHA384"],"status":"active","created_at":"2026-04-30T09:44:06.548559Z","updated_at":"2026-04-30T09:44:07.136597Z"}],"result_info":{"page":1,"per_page":50,"count":2,"total_count":2,"total_pages":1}}
