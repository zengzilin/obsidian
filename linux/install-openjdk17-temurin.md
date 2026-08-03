# 二进制安装 OpenJDK 17 Temurin 17.0.9+9

本文记录在 Linux 服务器上通过二进制包安装 OpenJDK 17，并切换系统/用户 Java 环境变量的步骤。

目标版本：

```bash
openjdk version "17.0.9" 2023-10-17
OpenJDK Runtime Environment Temurin-17.0.9+9 (build 17.0.9+9)
OpenJDK 64-Bit Server VM Temurin-17.0.9+9 (build 17.0.9+9, mixed mode, sharing)
```

## 1. 下载 JDK 17 二进制包

```bash
cd /tmp
wget https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_x64_linux_hotspot_17.0.9_9.tar.gz
```

如果服务器不能直接访问 GitHub，可以在本地下载后上传到服务器。

## 2. 解压安装

推荐安装目录：`/usr/local/java`

```bash
sudo mkdir -p /usr/local/java
sudo tar -zxvf OpenJDK17U-jdk_x64_linux_hotspot_17.0.9_9.tar.gz -C /usr/local/java
```

解压后目录通常为：

```bash
/usr/local/java/jdk-17.0.9+9
```

确认文件存在：

```bash
ls -l /usr/local/java/jdk-17.0.9+9/bin/java
/usr/local/java/jdk-17.0.9+9/bin/java -version
```

## 3. 临时切换当前 shell 到 JDK 17

```bash
export JAVA_HOME=/usr/local/java/jdk-17.0.9+9
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib
hash -r
java -version
which java
echo $JAVA_HOME
```

期望：

```bash
which java
# /usr/local/java/jdk-17.0.9+9/bin/java
```

## 4. 全局配置 `/etc/profile`

编辑：

```bash
sudo vi /etc/profile
```

在文件末尾加入：

```bash
# Java 17
export JAVA_HOME=/usr/local/java/jdk-17.0.9+9
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib
```

生效：

```bash
source /etc/profile
hash -r
java -version
which java
echo $JAVA_HOME
```

注意：JDK 17 不建议再配置 JDK 8 的旧路径：

```bash
$JAVA_HOME/jre/lib/ext
$JAVA_HOME/lib/tool.jar
```

JDK 17 没有传统 JDK 8 的 `jre/lib/ext` 和 `tool.jar`。

## 5. 如果当前用户仍显示 Java 1.8

先查看当前环境：

```bash
echo $JAVA_HOME
echo $PATH
which java
type -a java
java -version
```

如果仍显示：

```bash
JAVA_HOME=/opt/java/jdk1.8.0_192
PATH=/opt/java/jdk1.8.0_192/bin:...
```

说明当前 shell 还在使用旧环境变量。

查找哪里设置了 JDK 1.8：

```bash
grep -R "jdk1.8.0_192\|JAVA_HOME\|CLASSPATH" /etc/profile /etc/profile.d/* ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null
```

找到后把旧配置：

```bash
export JAVA_HOME=/opt/java/jdk1.8.0_192
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=$JAVA_HOME/jre/lib/ext:$JAVA_HOME/lib/tool.jar
```

改为：

```bash
export JAVA_HOME=/usr/local/java/jdk-17.0.9+9
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib
```

## 6. 针对普通用户单独配置

例如当前用户是 `abroad`，可以配置用户级环境变量。

编辑：

```bash
vi /home/abroad/.bash_profile
```

文件末尾加入：

```bash
export JAVA_HOME=/usr/local/java/jdk-17.0.9+9
export PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib
```

如有需要，也可加入：

```bash
vi /home/abroad/.bashrc
```

生效：

```bash
source /home/abroad/.bash_profile
source /home/abroad/.bashrc
hash -r
java -version
which java
echo $JAVA_HOME
```

重新 SSH 登录后再次验证：

```bash
java -version
which java
echo $JAVA_HOME
```

## 7. 使用 alternatives 切换系统默认 Java

如果希望系统 `/usr/bin/java` 默认指向 JDK 17，可使用 alternatives。

CentOS/RHEL：

```bash
sudo alternatives --install /usr/bin/java java /usr/local/java/jdk-17.0.9+9/bin/java 1709
sudo alternatives --install /usr/bin/javac javac /usr/local/java/jdk-17.0.9+9/bin/javac 1709
sudo alternatives --config java
sudo alternatives --config javac
```

没有 sudo 时，使用 root 执行：

```bash
alternatives --install /usr/bin/java java /usr/local/java/jdk-17.0.9+9/bin/java 1709
alternatives --install /usr/bin/javac javac /usr/local/java/jdk-17.0.9+9/bin/javac 1709
alternatives --config java
alternatives --config javac
```

选择：

```bash
/usr/local/java/jdk-17.0.9+9/bin/java
```

验证：

```bash
java -version
javac -version
which java
```

## 8. 常见问题

### `java -version` 仍显示 1.8

优先执行：

```bash
source /etc/profile
hash -r
java -version
which java
echo $JAVA_HOME
```

如果仍不生效，检查用户配置或 `/etc/profile.d`：

```bash
grep -R "jdk1.8.0_192\|JAVA_HOME\|CLASSPATH" /etc/profile /etc/profile.d/* ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null
```

### 命令拼写错误

正确命令是：

```bash
java -version
```

不是：

```bash
java -verslon
```

### 容器/Pod 中安装

如果是在 Kubernetes Pod 或容器中手动安装，Pod 重启后修改可能丢失。长期生效应修改镜像 Dockerfile 或 Deployment 环境变量。

Dockerfile 示例：

```dockerfile
ADD OpenJDK17U-jdk_x64_linux_hotspot_17.0.9_9.tar.gz /usr/local/java/
ENV JAVA_HOME=/usr/local/java/jdk-17.0.9+9
ENV PATH="${JAVA_HOME}/bin:${PATH}"
```
