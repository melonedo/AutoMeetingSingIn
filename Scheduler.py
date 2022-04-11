import json
from collections import namedtuple
import re
from datetime import datetime, timedelta
import time
from AutoSignIn import signIn
import ctypes

Class = namedtuple('Class', 'name teacher start end meetingid password')

def load_data() -> list[Class]:
    with open("data/classes.json", encoding='utf-8') as f:
        data = json.load(f)
    result = []
    for c in data['data']:
        m = re.match(r'(.+?) \| (.+?)\r\n会号:(\d+) \| 密码:(\d+)', c['title'])
        if m is None:
            print(f"Failed to parse title '{c['title']}'")
            continue
        start = datetime.fromisoformat(c['start'])
        end = datetime.fromisoformat(c['end'])
        result.append(Class(m[1], m[2], start, end, m[3], m[4]))
    return result

def get_next_class(classes: list[Class], time=datetime.now()):
    not_ended = (c for c in classes if c.end > time)
    return min(not_ended, key=lambda x: x.start)

def schedule(c: Class):
    key = ctypes.windll.user32.MessageBoxW(0, f"是否登录腾讯会议〔{c.name}〕", "确认后请勿操作键盘和鼠标", 1)
    if key == 1:
        signIn(c.meetingid, c.password)
    return key == 1

def schedule_next_class(classes: list[Class]):
    c = get_next_class(classes)
    time_str = c.start.strftime("%m月%d日(星期%w) %H:%M")
    print(f"下一节课是：{c.name}「{c.teacher}」 {time_str}")
    print(f"会议号：{c.meetingid} 密码：{c.password}")
    # 提前一段时间进入
    start = c.start - timedelta(minutes=8)
    while datetime.now() < start:
        time.sleep(30)
    while not schedule(c):
        time.sleep(30)

classes = load_data()
while True:
    schedule_next_class(classes)
    time.sleep(60*60)
