#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Kelly Hwong
# Date: April 4th, 2019

import requests
from PIL import Image
from lxml import etree
from bs4 import BeautifulSoup
import execjs

from captcha.ruokuai import RClient
from settings import HEADERS

shape_values = {
    "1": "1",
    "heart": "draggable_+lD1yU/2yqtmXEtzN7pNxNB/vJ3xGHgXE/zOYLHgwvo="
}

STATICS_ROOT = "./fbs_user/html/"
js_files = ["js/jquery.min.js", "js/jquery.js",
            "js/jquery-ui-1.7.2.custom.min.js", "js/jquery.sexy-captcha-0.1.js"]

js_contents = ""
for file in js_files:
    with open(STATICS_ROOT + file, "r") as f:
        js_contents = js_contents + f.read()
ctx = execjs.compile(js_contents)


def readCaptcha(image):
    """
    识别验证码
    """
    rc = RClient('kellyhwong', 'Hbxn8310189')
    # image = open('./tkcode', 'rb').read()
    Result = rc.rk_create(image, 3050)
    return Result


def main():
    '''
    image = "./captcha/Captcha.png"
    image = open(image, 'rb').read()
    captcha = readCaptcha(image)
    print(captcha.lower())
    '''

    main_url = "https://w6.ab.ust.hk/fbs_user/html/main.htm"
    session = requests.Session()
    response = session.get(main_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "lxml")

    '''
    # DEBUG
    with open("./debugCaptcha.html", "wb") as f:
        f.write(response.content)
    '''
    '''
    with open("./fbs_user/html/main.htm") as f:
        main_html = f.read()
    soup = BeautifulSoup(main_html, "lxml")
    '''
    # 调用

    imgCaptcha = soup.find("img", {"id": "imgCaptcha"})
    # print(imgCaptcha["src"])

    scripts = soup.find_all("script")
    target_script = scripts[-1]
    target_script = target_script.text
    # print(target_script)
    ctx.eval("$('.myCaptcha').sexyCaptcha('../CaptchaServlet');")

    # https://w6.ab.ust.hk/fbs_user/Captcha.jpg?0.39701897636037664


if __name__ == '__main__':
    main()
