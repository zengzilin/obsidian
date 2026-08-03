# 下面是基于 Nacos 2.5 Docker 部署的三节点集群示例。生产环境建议使用独立 MySQL，而不是单机 Docker 内的 MySQL。
## 1. 准备 MySQL
创建数据库 nacos_config，字符集使用 utf8mb4，执行 Nacos 发行包中的初始化脚本：
conf/mysql-schema.sql
确认 MySQL 可被三个 Nacos 容器访问，例如：
192.168.1.10:3306
## 2. 创建 docker-compose.yml
```
services:
  nacos1:
    image: nacos/nacos-server:v2.5.0
    container_name: nacos1
    hostname: nacos1
    restart: unless-stopped
    ports:
      - "8848:8848"
      - "9848:9848"
      - "9849:9849"
    environment:
      MODE: cluster
      NACOS_SERVERS: "nacos1:8848 nacos2:8848 nacos3:8848"
      SPRING_DATASOURCE_PLATFORM: mysql
      MYSQL_SERVICE_HOST: 192.168.1.10
      MYSQL_SERVICE_PORT: 3306
      MYSQL_SERVICE_DB_NAME: nacos_config
      MYSQL_SERVICE_USER: nacos
      MYSQL_SERVICE_PASSWORD: "修改为实际密码"
      MYSQL_SERVICE_DB_PARAM: "characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=false&useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=Asia/Shanghai"
      NACOS_AUTH_ENABLE: "true"
      NACOS_AUTH_IDENTITY_KEY: "nacos"
      NACOS_AUTH_IDENTITY_VALUE: "修改为集群共享值"
      NACOS_AUTH_TOKEN: "修改为符合要求的Base64密钥"
    networks: [nacos]

  nacos2:
    image: nacos/nacos-server:v2.5.0
    container_name: nacos2
    hostname: nacos2
    restart: unless-stopped
    ports:
      - "8858:8848"
      - "9858:9848"
      - "9859:9849"
    environment:
      MODE: cluster
      NACOS_SERVERS: "nacos1:8848 nacos2:8848 nacos3:8848"
      SPRING_DATASOURCE_PLATFORM: mysql
      MYSQL_SERVICE_HOST: 192.168.1.10
      MYSQL_SERVICE_PORT: 3306
      MYSQL_SERVICE_DB_NAME: nacos_config
      MYSQL_SERVICE_USER: nacos
      MYSQL_SERVICE_PASSWORD: "修改为实际密码"
      MYSQL_SERVICE_DB_PARAM: "characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=false&useUnicode=true&serverTimezone=Asia/Shanghai"
      NACOS_AUTH_ENABLE: "true"
      NACOS_AUTH_IDENTITY_KEY: "nacos"
      NACOS_AUTH_IDENTITY_VALUE: "修改为集群共享值"
      NACOS_AUTH_TOKEN: "修改为符合要求的Base64密钥"
    networks: [nacos]

  nacos3:
    image: nacos/nacos-server:v2.5.0
    container_name: nacos3
    hostname: nacos3
    restart: unless-stopped
    ports:
      - "8868:8848"
      - "9868:9848"
      - "9869:9849"
    environment:
      MODE: cluster
      NACOS_SERVERS: "nacos1:8848 nacos2:8848 nacos3:8848"
      SPRING_DATASOURCE_PLATFORM: mysql
      MYSQL_SERVICE_HOST: 192.168.1.10
      MYSQL_SERVICE_PORT: 3306
      MYSQL_SERVICE_DB_NAME: nacos_config
      MYSQL_SERVICE_USER: nacos
      MYSQL_SERVICE_PASSWORD: "修改为实际密码"
      MYSQL_SERVICE_DB_PARAM: "characterEncoding=utf8&zeroDateTimeBehavior=convertToNull&useSSL=false&useUnicode=true&serverTimezone=Asia/Shanghai"
      NACOS_AUTH_ENABLE: "true"
      NACOS_AUTH_IDENTITY_KEY: "nacos"
      NACOS_AUTH_IDENTITY_VALUE: "修改为集群共享值"
      NACOS_AUTH_TOKEN: "修改为符合要求的Base64密钥"
    networks: [nacos]

networks:
  nacos:
    driver: bridge
```
三个节点必须使用相同的数据库、认证配置和 NACOS_SERVERS。NACOS_AUTH_TOKEN 应使用随机生成的 Base64 密钥，例如：
openssl rand -base64 32
## 3. 启动集群
docker compose up -d
docker compose ps
docker compose logs -f nacos1
## 4. 检查节点状态
curl http://127.0.0.1:8848/nacos/v1/console/health/readiness
curl http://127.0.0.1:8858/nacos/v1/console/health/readiness
curl http://127.0.0.1:8868/nacos/v1/console/health/readiness
返回 UP 或就绪状态后，访问：
http://服务器IP:8848/nacos
默认账号通常为：
nacos / nacos
首次登录后应立即修改密码。
## 5. 客户端连接地址
客户端不要只配置一个节点，建议配置：
192.168.1.10:8848,192.168.1.10:8858,192.168.1.10:8868