from pywinauto import Desktop
from pywinauto.timings import Timings, TimeoutError
from subprocess import Popen
from Config import load_config

config = load_config()
exe = config['exe']
nickname = config['nickname']

Timings.fast()

def outline(wnd, debug):
    if debug:
        wnd.draw_outline()
    return wnd

def signIn(meeting_id, password=None, debug=False):
    Popen(exe)
    desktop = Desktop(backend='uia')
    loadingWnd = desktop['腾讯会议(LoadingWnd)']
    try:
        loadingWnd.wait('ready')
        outline(loadingWnd.child_window(title="加入会议"), debug).click_input()
    except TimeoutError:
        pass
    joinWnd = desktop['腾讯会议(JoinWnd)']
    clear = joinWnd.child_window(title="Join_meeting_clear_meeting_number")
    if clear.exists():
        outline(clear, debug)
        clear.click_input()
    meeting_number = joinWnd.child_window(title="Join_meeting_meeting_number")
    outline(meeting_number, debug)
    meeting_number.click_input()
    meeting_number.type_keys(meeting_id)
    nickname_frame = joinWnd.child_window(title="NickNameFrameContainer")
    outline(nickname_frame.Edit, debug)
    nickname_frame.Edit.click_input()
    outline(nickname_frame.Button, debug)
    nickname_frame.Button.exists() and nickname_frame.Button.click_input()
    nickname_frame.Edit.click_input()
    nickname_frame.Edit.type_keys(nickname)
    joinWnd.child_window(title="Join_meeting_Join_meeting").click_input()
    if password is not None:
        outline(joinWnd.child_window(title="PasswordEdit"), debug).type_keys(password)
        outline(joinWnd.child_window(title="加入"), debug).click_input()
    inMeetingWnd = desktop['腾讯会议(InMeetingWnd)']
    if inMeetingWnd.child_window(title="会议未开始，等待主持人进入").exists():
        outline(inMeetingWnd.child_window(title="离开会议"), debug).click_input()
        outline(inMeetingWnd.child_window(title="离开"), debug).click_input()
        return False
    return True

