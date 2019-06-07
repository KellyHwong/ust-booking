#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Kelly Hwong
# Date: April 8th, 2019

import requests
from bs4 import BeautifulSoup

from settings import HEADERS, XML_HEADERS

# from shape to bg-pos, then to id
SHAPE_MAP = {
    "star": "-120px -3px",
    "heart": "0 -3px",
    "triple": "-56px -3px",
    "square": "-185px -3px"
}

TARGET_MAP = {
    "-185px -66px": "square",
    "-56px -66px": "triple",
    "-120px -66px": "star",
    "0px -66px": "heart"
}


def main():
    url = "https://w6.ab.ust.hk/fbs_user/CaptchaServlet"
    session = requests.Session()
    response = session.post(url, headers=XML_HEADERS,
                            data={'action': 'refresh'})
    # print(response) # 200
    soup = BeautifulSoup(response.content, "lxml")
    captchaWrapper = soup.find("div", {"class", "captchaWrapper"})
    # print(captchaWrapper)
    draggables = captchaWrapper.find_all("div", {"class", "draggable"})

    targetWrapper = soup.find("div", {"class", "targetWrapper"})
    target = targetWrapper.find("div", {"class", "target"})
    style = target["style"]
    bg_pos = style[style.find("background-position:") +
                   len("background-position:"):]
    print(bg_pos)

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
            print(draggable["id"])
            break


if __name__ == '__main__':
    main()
