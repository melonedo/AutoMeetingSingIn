from datetime import date, timedelta
from urllib.parse import urlparse, parse_qs
import json
import requests
import crack
from Config import load_config


config = load_config()
user_id, password = config['user_id'], config['password']


def login(id, pwd):
    # 验证码
    s = requests.Session()
    code = crack.getCode()
    assert code is not None
    # ids
    data = {'option': 'credential', 'Ecom_User_ID': id,
            'Ecom_Password': pwd, 'Ecom_Captche': code}
    s.post('https://ids.tongji.edu.cn:8443/nidp/app/login', data=data)
    # courses
    r = s.get("https://ids.tongji.edu.cn:8443/nidp/oauth/nam/authz?scope=profile&response_type=code&redirect_uri=https%3A%2F%2Fcourses.tongji.edu.cn%2Fsign-in&client_id=241129f4-7528-4207-8751-ee240727b41c")
    code = parse_qs(urlparse(r.url).query)['code'][0]
    data = {"code": code}
    r = s.post("https://courses.tongji.edu.cn/tmbs/api/v1/sso", data=data)
    token = r.json()["data"]["token"]
    # fetch calendar
    today = date.today()
    data = {"user_token": token, "start": today,
            "end": today+timedelta(weeks=4)}
    r = s.post(
        "https://courses.tongji.edu.cn/tmbs/api/v1/user/calendar/my", data=data)
    with open("data/classes.json", "wt", encoding='utf-8') as f:
        json.dump(r.json(), f, ensure_ascii=False)
    print("成功导入课程表")


login(user_id, password)
