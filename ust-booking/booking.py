#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Kelly Hwong
# Date: April 8th, 2019

import json
import requests
import random
from bs4 import BeautifulSoup
from urllib import parse
from captcha.ruokuai import RClient
from settings import HEADERS, SHAPE_MAP, TARGET_MAP

TEST = 1
if TEST:
    config_file = "user-test.json"
else:
    config_file = "user.json"


class FBS(object):
    """docstring for FBS"""

    def __init__(self, ):
        super(FBS, self).__init__()
        with open(config_file, "r") as f:
            user = json.load(f)
        self.user = user  # 没有就回直接报错，那么就要去 user.json 里填写user信息了
        self.url = "https://w6.ab.ust.hk/fbs_user/CaptchaServlet"
        self.session = requests.Session()
        self.draggable_id = None
        self.verify_text = None

    def get_draggable_id(self) -> bool:
        response = self.session.post(
            self.url, headers=HEADERS, data={'action': 'refresh'})
        # self.cookie = response.headers["Cookie"]
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, "lxml")
        captchaWrapper = soup.find("div", {"class", "captchaWrapper"})
        draggables = captchaWrapper.find_all("div", {"class", "draggable"})

        targetWrapper = soup.find("div", {"class", "targetWrapper"})
        target = targetWrapper.find("div", {"class", "target"})
        style = target["style"]
        bg_pos = style[style.find(
            "background-position:") + len("background-position:"):]

        for key in TARGET_MAP.keys():
            if bg_pos.find(key) >= 0:
                match = key
                break
        shape = TARGET_MAP[match]
        bg_pos = SHAPE_MAP[shape]

        for draggable in draggables:
            # print(draggable["id"])
            # print(draggable["style"])
            style = draggable["style"]
            draggable_bg_pos = style[style.find(
                "background-position:") + len("background-position:"):]
            if draggable_bg_pos.find(bg_pos) >= 0:
                self.draggable_id = draggable["id"]
                return True
        return False

    def get_verify_text(self) -> bool:
        response = self.session.get(
            "https://w6.ab.ust.hk/fbs_user/Captcha.jpg?" + str(random.random()), headers=HEADERS)
        with open("./image/Captcha.jpg", "wb") as f:
            length = response.headers.get('content-length')
            if length is None:
                f.write(response.content)
            else:
                for chunk in response.iter_content(2048):
                    f.write(chunk)

        rc = RClient('kellyhwong', 'Hbxn8310189')
        im = open('./image/Captcha.jpg', 'rb').read()
        result = rc.rk_create(im, 3050)
        # print(type(result))
        if "Result" in result.keys():
            self.verify_text = result["Result"].lower()
            return True
        else:
            self.verify_text = None
            return False

    def login(self):
        data = {"loginID": self.user["username"], "passwd": self.user["password"],
                "verify_text": self.verify_text, "captcha": self.draggable_id, "Button": "Login", "JSEnable": "true"}
        data = parse.urlencode(data).encode('utf-8')
        login_headers = HEADERS
        # login_headers["Cookie"] = self.cookie
        response = self.session.post(
            url="https://w6.ab.ust.hk/fbs_user/bin2/main", headers=login_headers, data=data)
        # print(response.headers)
        # print(response.request.headers)
        print(response.text)
        with open("debugLogin.html", "wb") as f:
            f.write(response.content)

    def test_login(self):
        url = "https://w6.ab.ust.hk/fbs_user/bin2/user_info"
        response = self.session.get(url=url, headers=HEADERS)
        print(response.text)
        with open(("debugInfo.html"), "wb") as f:
            f.write(response.content)


def main():
    fbs = FBS()
    if fbs.get_draggable_id():
        print(fbs.draggable_id)
    if fbs.get_verify_text():
        print(fbs.verify_text)
    fbs.login()
    fbs.test_login()


if __name__ == '__main__':
    main()
