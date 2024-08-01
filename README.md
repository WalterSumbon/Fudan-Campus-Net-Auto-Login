# 自动登录复旦校园网

## 介绍

复旦的校园网每次连接上时候，都需要再在网页中登录，很麻烦。

login_campus.py的功能是，每5秒检测一次，如果检测到连接了名为iFudan.stu的校园网，就会通过登录接口登录校园网。

本仓库的代码已在我个人的windows电脑上测试过。

用户名和密码的配置在config.ini中填写。

如果你需要添加开机自启的话，可以参考startup_campus_wifi_auto_login.bat脚本，把其中的pythonw路径和python脚本路径改成你自己的，然后放到开机自启程序文件夹中（win+R，输入shell:startup，即可快速打开这个文件夹）。

## TODO

- [ ] 在MacOS上测试
- [ ] 支持其他的校园网类型（移动等）