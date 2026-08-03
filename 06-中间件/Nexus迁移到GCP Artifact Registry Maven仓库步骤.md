# Nexus 迁移到 GCP Artifact Registry Maven 仓库步骤

## 迁移目标

当前 Nexus 仓库 `maven-public` 是一个 `group` 仓库，成员如下：

- `maven-releases`
- `maven-snapshots`
- `maven-central`

推荐迁移方式：

- 将 `maven-releases` 迁移到 GCP Maven `standard` 仓库
- 将 `maven-snapshots` 迁移到 GCP Maven `standard` 仓库
- 不迁移 `maven-central` 的历史缓存，改为在 GCP 中创建 Maven `remote` 仓库
- 如需一个统一下载入口，再创建一个 Maven `virtual` 仓库

这样做的原因：

- `maven-public` 只是聚合入口，不适合直接整库迁移
- `maven-central` 里大多是公网依赖缓存，没有必要物理搬迁
- 私有包和公网依赖拆开后，后续维护更简单

## 迁移前准备

建议先确认以下信息：

- GCP 项目 ID，例如 `PROJECT_ID`
- GCP 区域，例如 `asia-east1`
- Nexus 管理员账号
- 一台可以同时访问 Nexus 和 GCP 的迁移机器
- 本地已安装并登录 `gcloud`
- 本地已安装 `Java` 和 `Maven`

迁移前建议暂停写入：

- 暂停 CI 向 `maven-releases` 发版
- 暂停 CI 向 `maven-snapshots` 发版

建议顺序：

1. 先迁移 `maven-releases`
2. 再迁移 `maven-snapshots`
3. 最后切换业务配置

## 第一步：在 GCP 创建目标仓库

先启用 Artifact Registry：

```bash
gcloud services enable artifactregistry.googleapis.com --project=PROJECT_ID
```

创建 release 仓库：

```bash
gcloud artifacts repositories create maven-releases \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository-format=maven \
  --description="Private Maven releases" \
  --version-policy=Release
```

创建 snapshot 仓库：

```bash
gcloud artifacts repositories create maven-snapshots \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository-format=maven \
  --description="Private Maven snapshots" \
  --version-policy=Snapshot \
  --allow-snapshot-overwrites
```

创建 Maven Central remote 仓库：

```bash
gcloud artifacts repositories create maven-central-remote \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository-format=maven \
  --description="Remote Maven Central" \
  --mode=remote-repository \
  --remote-repo-config-desc="Maven Central" \
  --remote-mvn-repo=MAVEN-CENTRAL
```

说明：

- `maven-releases` 用于正式版本
- `maven-snapshots` 用于快照版本
- `maven-central-remote` 用于替代 Nexus 中的 `maven-central` 代理缓存

## 第二步：可选创建统一读取入口

如果希望像原来的 `maven-public` 一样提供统一访问地址，可以创建一个 `virtual` 仓库。

先创建 `upstreams.json`：

```json
[
  {
    "id": "releases",
    "repository": "projects/PROJECT_ID/locations/LOCATION/repositories/maven-releases",
    "priority": 100
  },
  {
    "id": "snapshots",
    "repository": "projects/PROJECT_ID/locations/LOCATION/repositories/maven-snapshots",
    "priority": 90
  },
  {
    "id": "central",
    "repository": "projects/PROJECT_ID/locations/LOCATION/repositories/maven-central-remote",
    "priority": 10
  }
]
```

创建 virtual 仓库：

```bash
gcloud artifacts repositories create maven-public \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository-format=maven \
  --mode=virtual-repository \
  --description="Unified Maven read endpoint" \
  --upstream-policy-file=upstreams.json
```

说明：

- `virtual` 仓库通常只用于读取
- 发布时仍然建议分别推送到 `maven-releases` 和 `maven-snapshots`

## 第三步：配置 Maven 认证

输出 Artifact Registry 的 Maven 配置：

```bash
gcloud artifacts print-settings mvn \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository=maven-releases
```

将输出内容加入：

- `~/.m2/settings.xml`
- 或项目的 `pom.xml`

建议先做一次连通性测试：

- 先手工向 `maven-releases` 上传一个测试包
- 确认上传成功后再开始批量迁移

## 第四步：从 Nexus 导出私有包

不要从 `maven-public` 导出，直接导出以下两个真实仓库：

- `maven-releases`
- `maven-snapshots`

推荐使用 Nexus `Components API` 获取组件信息：

```bash
curl -u USER:PASS \
  "http://192.168.1.19:8081/service/rest/v1/components?repository=maven-releases"
```

如果结果很多，需要使用 `continuationToken` 翻页继续请求。

导出时建议保留：

- `pom`
- 主 `jar`
- `sources jar`
- `javadoc jar`
- 其他 classifier 文件

导出时建议跳过：

- `*.md5`
- `*.sha1`
- `*.sha256`
- `*.sha512`
- `maven-metadata.xml`
- `maven-metadata.xml.md5`
- `maven-metadata.xml.sha1`

原因：

- 校验文件通常会由目标仓库重新生成或校验
- `maven-metadata.xml` 不建议手工迁移

## 第五步：上传到 GCP Artifact Registry

迁移每个 Maven 组件时，推荐使用 `mvn deploy:deploy-file`。

### 1. 只有 pom 和主 jar 的普通组件

```bash
mvn deploy:deploy-file \
  -Durl=artifactregistry://LOCATION-maven.pkg.dev/PROJECT_ID/maven-releases \
  -DrepositoryId=artifact-registry \
  -DpomFile=demo-1.0.0.pom \
  -Dfile=demo-1.0.0.jar
```

### 2. 带 sources 和 javadoc 的组件

```bash
mvn deploy:deploy-file \
  -Durl=artifactregistry://LOCATION-maven.pkg.dev/PROJECT_ID/maven-releases \
  -DrepositoryId=artifact-registry \
  -DpomFile=demo-1.0.0.pom \
  -Dfile=demo-1.0.0.jar \
  -Dfiles=demo-1.0.0-sources.jar,demo-1.0.0-javadoc.jar \
  -Dclassifiers=sources,javadoc \
  -Dtypes=jar,jar
```

### 3. 只有 pom 的组件

```bash
mvn deploy:deploy-file \
  -Durl=artifactregistry://LOCATION-maven.pkg.dev/PROJECT_ID/maven-releases \
  -DrepositoryId=artifact-registry \
  -DpomFile=demo-1.0.0.pom \
  -Dfile=demo-1.0.0.pom \
  -Dpackaging=pom
```

### 4. 上传 snapshot 组件

将地址改为：

```text
artifactregistry://LOCATION-maven.pkg.dev/PROJECT_ID/maven-snapshots
```

说明：

- `release` 上传到 `maven-releases`
- `snapshot` 上传到 `maven-snapshots`
- 不要手工上传 `maven-metadata.xml`

## 第六步：迁移验证

先检查 GCP 中是否有包：

```bash
gcloud artifacts packages list \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository=maven-releases
```

检查指定包的版本：

```bash
gcloud artifacts versions list \
  --project=PROJECT_ID \
  --location=LOCATION \
  --repository=maven-releases \
  --package=com.example:demo
```

然后做实际验证：

1. 用一个测试项目从 GCP 拉取依赖
2. 验证 release 依赖能正常下载
3. 验证 snapshot 依赖能正常下载
4. 验证 Maven Central 公共依赖能通过 remote 仓库拉取

## 第七步：切换业务配置

建议的仓库使用方式：

- 发布 release：指向 `maven-releases`
- 发布 snapshot：指向 `maven-snapshots`
- 下载依赖：指向 `maven-public` virtual 仓库

切换后建议保留旧 Nexus 一段时间，只读运行几天，确认没有漏包后再下线。

## 推荐的迁移节奏

### 方案一：停机窗口迁移

适合包数量不算太大，或者允许短时间暂停发版的场景。

步骤：

1. 暂停所有发布任务
2. 导出 `maven-releases`
3. 上传到 GCP `maven-releases`
4. 导出 `maven-snapshots`
5. 上传到 GCP `maven-snapshots`
6. 验证
7. 切换配置

### 方案二：分阶段迁移

适合想降低风险的场景。

步骤：

1. 先迁移 `maven-releases`
2. 业务先继续使用旧 Nexus
3. 验证 GCP 中的 release 包完整性
4. 约定一个时间窗口迁移 `maven-snapshots`
5. 切换读写配置

## 注意事项

- 不要直接迁移 `maven-public`
- 不要物理迁移 `maven-central` 历史缓存
- `snapshot` 最容易出现元数据差异，建议最后迁移
- `Artifact Registry` 的仓库版本策略建议在创建时就规划好
- 如果历史包很多，建议先抽样验证再批量执行

## 建议的最终结构

GCP 中建议保留以下仓库：

- `maven-releases`
- `maven-snapshots`
- `maven-central-remote`
- `maven-public`

其中：

- `maven-releases` 和 `maven-snapshots` 用于发布
- `maven-central-remote` 用于公网依赖缓存
- `maven-public` 用于统一读取

## 官方参考

- GCP Artifact Registry 创建仓库  
  https://docs.cloud.google.com/artifact-registry/docs/repositories/create-repos

- GCP Artifact Registry remote 仓库  
  https://docs.cloud.google.com/artifact-registry/docs/repositories/remote-repo

- GCP Artifact Registry virtual 仓库  
  https://docs.cloud.google.com/artifact-registry/docs/repositories/virtual-repo

- GCP Artifact Registry Maven 认证  
  https://docs.cloud.google.com/artifact-registry/docs/java/authentication

- GCP Artifact Registry Java 包管理  
  https://docs.cloud.google.com/artifact-registry/docs/java/store-java

- Nexus Components API  
  https://help.sonatype.com/en/components-api.html

## 后续可补充内容

如果后面需要，可以继续补：

- 一份 PowerShell 批量迁移脚本
- 一份 Linux shell 批量迁移脚本
- 一份 Maven `settings.xml` 完整示例
- 一份迁移核对清单
