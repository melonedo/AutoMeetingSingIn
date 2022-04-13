import json
from collections import namedtuple
import re
from datetime import datetime, timedelta
import time
from AutoSignIn import signIn
import ctypes
from Config import load_config
from FetchCalendar import fetch
from os.path import exists

Class = namedtuple('Class', 'name teacher start end meetingid password')


def load_data(path="data/classes.json") -> list[Class]:
    if not exists(path):
        print("课程表不存在，尝试导入")
        fetch()
        print("如果课程表有更新，删除data/classes.json以重新导入课程表。")
    with open(path, encoding='utf-8') as f:
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
    if dialog:
        key = ctypes.windll.user32.MessageBoxW(
            0, "确认后请勿操作键盘和鼠标。可在配置data/config.json中将dialog设为false避免弹出此对话框。", f"是否进入会议会议〔{c.name}〕", 1)
        if key != 1:
            return False
    return signIn(c.meetingid, c.password)


def schedule_next_class(classes: list[Class], end_time=None):
    c = get_next_class(classes, end_time)
    time_str = c.start.strftime("%m月%d日(星期%w) %H:%M")
    print(f"下一节课是：{c.name}「{c.teacher}」 {time_str}")
    print(f"会议号：{c.meetingid} 密码：{c.password}")
    # 提前一段时间进入
    start = c.start - timedelta(minutes=8)
    while datetime.now() < start:
        time.sleep(30)
    while not schedule(c):
        time.sleep(30)
    print("成功进入！")
    return c.end


config = load_config()
dialog = config['dialog']

if __name__ == '__main__':
    classes = load_data()
    end_time = datetime.now()
    while True:
        end_time = schedule_next_class(classes, end_time)

