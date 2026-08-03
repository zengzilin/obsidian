# Warning: putenv() has been disabled for security reasons in /www/wwwroot/soravideodownloader.com/wp-content/plugins/jnews-meta-h

报错

Warning: putenv() has been disabled for security reasons in /www/wwwroot/soravideodownloader.com/wp-content/plugins/jnews-meta-header/class.jnews-meta-header.php on line 66 Warning: putenv() has been disabled for security reasons in /www/wwwroot/soravideodownloader.com/wp-content/plugins/jnews-meta-header/class.jnews-meta-header.php on line 77

方法一：通过PHP配置启用putenv()函数

1. 修改PHP配置文件（推荐）  
步骤：  
登录服务器管理面板（如宝塔面板），找到当前网站使用的PHP版本，进入「禁用函数」设置。  
在禁用函数列表中删除 putenv 123。  
手动修改php.ini （适用于无面板环境）：  
通过SSH连接服务器，使用命令 php --ini 查找 php.ini 路径（通常为 /usr/local/php/etc/php.ini ）。  
编辑文件，找到 disable_functions 配置项，移除其中的 putenv，保存并重启PHP服务 45。
2. 重启PHP服务  
修改后需重启PHP-FPM或Web服务器（如Nginx/Apache）使配置生效 7



解决方式 禁止了7.4相关函数，重启php



> 更新: 2025-02-18 13:42:52  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/om02lsus5qsymvrm>