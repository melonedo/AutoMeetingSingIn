# 腾讯会议定时自动进入

支持读取courses课程表，提前8分钟自动进入下一节课。

## 安装

仅在Windows可用。需要python 3.9，库pyautogui、opencv-python、pillow、pyperclip、requests、pycryptodome。推荐使用pipenv管理

```shell
# pip install pipenv
pipenv install
pipenv shell
```

### 个人配置文件

新建文件`data/config.json`，内容为

```json
{
    "exe": "腾讯会议完整路径.exe",
    "nickname": "入会昵称",
    "dialog": true,
    "user_id": "学号",
    "password": "统一认证密码"
}
```

### 导入courses课程表

配置好`data/config.json`后，运行下列指令导入下一个月的课程表。

```shell
git submodule update --init
python src/FetchCalendar.py # 不使用pipenv时需要注意设置PYTHONPATH=crackids
```

## 运行

- AutoSignIn.py提供自动登录工具，`signIn`函数自动打开腾讯会议，填入会议号、昵称、密码。登录过程中不应操作鼠标和键盘
- Scheduler.py提供课程表支持，反复轮询下一节课的时间并登录。若config.json中`dialog`为真，则会首先弹窗确认。

两个代码中包括了一些硬编码的时间常数，可以根据自己的需要改变。

### 自动开启课程

```shell
python src/Scheduler.py
```
