# kubespray新增节点报错

****

**kubespray 报错1：fatal: [node18]: FAILED! => {"changed": false, "module_stderr": "Shared connection to 192.168.4.94 closed.\r\n", "module_stdout": "/bin/sh: /usr/bin/python3.6: 没有那个文件或目录\r\n", "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error", "rc": 127}**

# **安装python36**
<font style="color:rgb(0, 0, 0);">yum install python36 </font>

**1. 确认Python环境**

**首先要确认node18节点上使用的Python版本以及Ansible使用的Python解释器是否正确。你可以通过以下命令查看node18节点上的Python版本：**

<font style="color:rgb(171, 178, 191);background-color:rgb(40, 44, 52);">python3.6 --version </font>



****

**kubespray报错2：An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ModuleNotFoundError: No module named 'selinux'**

**fatal: [node18]: FAILED! => {"changed": false, "msg": "Failed to import the required Python library (libselinux-python) on node18's Python /usr/bin/python3.6. Please read the module documentation and install it in the appropriate location. If the required library is installed, but Ansible is using the wrong Python interpreter, please consult the documentation on ansible_python_interpreter"}**



****

# **安装libselinux-python库**
**在node18节点上安装libselinux-python库，不同的Linux发行版安装命令有所不同：**

****

**CentOS/RHEL系统**

**使用yum命令进行安装：**



**sudo yum install -y libselinux-python3 **

**Ubuntu/Debian系统**

**使用apt命令进行安装：**



**sudo apt update **

**sudo apt install -y python3-selinux**



> 更新: 2025-04-10 10:09:22  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/abb2oe5ebgayil31>