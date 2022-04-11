# 腾讯会议定时自动进入

支持读取courses课程表，提前8分钟自动进入下一节课。

## 安装

仅在Windows可用。需要安装库pyautogui、opencv-python、pillow、pyperclip。或者可以用pipenv管理

```shell
# pip install pipenv
pipenv install
pipenv shell
```

### 导入courses课程表

首先选择课程表选项卡，同时打开网络调试工具。时间范围选择“月”后，查看路径为`/tmbs/api/v1/user/calendar/my`的响应，将响应的json储存到data/classes.json。

### 配置腾讯会议路径和昵称

新建文件`data/config.json`，内容为

```json
{
    "exe": "腾讯会议完整路径.exe",
    "nickname": "入会昵称"
}
```

## 运行

- AutoSignIn.py提供自动登录工具，`signIn`函数自动打开腾讯会议，填入会议号、昵称、密码。登录过程中不应操作鼠标和键盘
- Scheduler.py提供课程表支持，反复轮询下一节课的时间并登录。

两个代码中包括了一些硬编码的时间常数，可以根据自己的需要改变。
