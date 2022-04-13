import os
import pyautogui
import time
from datetime import datetime
import cv2
import pyperclip
import json
from Config import load_config
from sys import exit


class TemplateMatchFailed(Exception):
    pass


def locateTemplate(template, debug=False, mask=None):
    pyautogui.screenshot('screen.png')
    gray = cv2.imread('screen.png')
    img_template = cv2.imread(template)
    img_mask = None if mask is None else cv2.imread(mask)
    h, w = img_template.shape[0:2]
    res = cv2.matchTemplate(
        gray, img_template, cv2.TM_SQDIFF_NORMED, mask=img_mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top = min_loc[0]
    left = min_loc[1]
    x = [top, left, w, h]
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    if debug:
        img = cv2.imread("screen.png", 1)
        os.remove("screen.png")
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5,
                         interpolation=cv2.INTER_NEAREST)
        cv2.imshow("processed", img)
        if cv2.waitKey(0) == ord('q'):
            exit(1)
        cv2.destroyAllWindows()

    if min_val > 0.01:
        if debug:
            print(min_val)
        return None

    pyautogui.moveTo(top+h/2, left+w/2)
    return x


def mustLocateTemplate(template, *args):
    pos = locateTemplate(template, *args)
    if pos == None:
        raise TemplateMatchFailed(template)
    return pos


def signIn(meeting_id, password=None, debug=False):
    os.startfile(exe)
    for _ in range(0, 10):
        time.sleep(.5)
        pos = locateTemplate("img/start.png", debug)
        if pos is not None:
            pyautogui.click(pos)
            break
    else:
        return False
    pos = mustLocateTemplate("img/meeting-id.png", debug, "img/meeting-id.png")
    pyautogui.click(pos)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyautogui.write(meeting_id)
    pos = mustLocateTemplate("img/nickname.png", debug, "img/nickname.png")
    pyautogui.click(pos)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    pyperclip.copy(nickname)
    pyautogui.hotkey('ctrl', 'v')
    pos = mustLocateTemplate("img/join.png", debug)
    pyautogui.click(pos)
    if password is not None:
        time.sleep(1)
        # Cursor automatically focused to password
        pyautogui.write(password)
        pos = mustLocateTemplate("img/password-join.png", debug)
        pyautogui.click(pos)
    time.sleep(1)
    pos = locateTemplate('img/not-started.png', debug)
    if pos is not None:
        pos = mustLocateTemplate('img/exit.png', debug)
        pyautogui.click(pos)
        pos = mustLocateTemplate('img/exit2.png', debug)
        pyautogui.click(pos)
        return False
    return True


config = load_config()
exe = config['exe']
nickname = config['nickname']

if __name__ == '__main__':
    meeting_id = "123456789"
    password = "1234"
    res = signIn(meeting_id, password, False)
    print(res)
