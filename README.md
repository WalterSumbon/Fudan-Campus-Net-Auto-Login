# 自动登录复旦校园网

## 介绍

复旦的校园网每次连接上时候，都需要再在网页中登录，很麻烦。

login_campus.py的功能是，每5秒检测一次，如果检测到连接了名为iFudan.stu的校园网，就会通过登录接口登录校园网。

本仓库的代码已在我个人的windows电脑上测试过。

欢迎大家贡献代码😊

## 使用

在config.ini中填写用户名和密码。

## windows上添加开机自启

参考startup_campus_wifi_auto_login.bat脚本，把其中的 pythonw路径 和 python脚本路径 改成你自己的，然后放到开机自启程序文件夹中（win+R，输入shell:startup，即可快速打开这个文件夹）。

## MacOS上添加开机自启

创建文件：~/Library/LaunchAgents/com.user.startup.plist
写入：
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.startup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/your/script.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```
注意将其中的/path/to/your/script.sh替换成启动脚本。

修改权限：
```
chmod 644 ~/Library/LaunchAgents/com.user.startup.plist
chmod +x /path/to/your/script.sh
```

加载plist文件：
```
launchctl load ~/Library/LaunchAgents/com.user.startup.plist
```

这种方法允许脚本在**用户登陆时**自动运行脚本。如果想在**系统启动时**（在用户登录之前）运行脚本，则需要将 plist 文件放在`/Library/LaunchDaemons/`目录下，这需要管理员权限。

## TODO

- [x] 在MacOS上测试
- [ ] 支持其他的校园网类型（移动等）
- [ ] 增加错误处理