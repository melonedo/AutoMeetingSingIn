import json
from os.path import exists
from textwrap import dedent
from sys import exit

def load_config(path="data/config.json"):
    if not exists(path):
        with open(path, 'wt', encoding='utf-8') as f:
            f.write(dedent("""\
            {
                "exe": "腾讯会议完整路径.exe",
                "nickname": "入会昵称",
                "dialog": true,
                "user_id": "学号",
                "password": "统一认证密码"
            }
            """))

    with open(path, encoding='utf-8') as f:
        config = json.load(f)
    if config['exe'] == "腾讯会议完整路径.exe":
        print(f"请先填写配置文件{path}")
        exit(1)
    return config


