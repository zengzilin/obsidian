

```
sh: $APP/root/shell/entrypoint.sh: No such file or directory
```

### **🚨** **核心问题**

**变量** `**$APP**` **没有被解析！**  
Shell 把 `$APP` 当作了文件名的一部分，它试图寻找一个 literally 叫做 `"$APP/root/shell/entrypoint.sh"` 的文件，而不是 `/home/user/dockermanagement/root/shell/entrypoint.sh`。

这通常是因为：

1. **启动命令方式不对**：你可能在 Dockerfile 或 K8s YAML 中使用了 `exec` 直接调用脚本，但没有通过 `bash` 或 `sh` 来解释变量。
2. **环境变量未生效**：`ENV APP=...` 定义的位置不对，或者脚本执行时没有加载该环境变量。
3. **Shebang 缺失或错误**：脚本第一行不是 `#!/bin/bash`。

---

### **✅** **解决方案**

请检查你的 **Dockerfile** 或 **Kubernetes YAML** 中的启动部分，按以下任一方式修改：

#### **方案 A：在 Dockerfile 中修正 CMD (推荐)**

确保使用 `bash` 来启动脚本，并且不要直接用 `exec` 替换掉 shell 环境（除非你确定环境变量已注入）。

**错误的写法 (可能导致变量不解析):**

**dockerfile**

编辑

```
# 如果直接 exec 脚本，且脚本没有正确 shebang 或 env 未加载，就会报 $APP 未定义
CMD ["/home/user/dockermanagement/root/shell/entrypoint.sh"]
```

**✅** **正确的写法:**

**dockerfile**

编辑

```
# 显式调用 bash，确保环境变量加载和变量解析
CMD ["/bin/bash", "-c", "/home/user/dockermanagement/root/shell/entrypoint.sh"]
```

_注意：这里最好把路径写死（绝对路径），不要在 CMD 里依赖_ `_$APP_` _变量，因为 CMD 的解析层级有时很迷。_

#### **方案 B：在脚本内部写死路径 (最稳妥)**

既然 `$APP` 在启动时解析失败，不如直接在 `entrypoint.sh` 内部定义它，或者干脆不用变量。

**修改** `**entrypoint.sh**`**:**

**bash**

编辑

```
#!/bin/bash

# 【关键修改】在脚本内部重新定义 APP，确保它一定存在
export APP="/home/user/dockermanagement"

SCRIPT_PATH="$APP/root/shell/dockerRsync.sh"
```