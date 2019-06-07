#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Kelly Hwong
# Date: April 7th, 2019

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}

XML_HEADERS = {
    'Cookie': 'JSESSIONID=7F32D68CBB3B9F41914A11BFBCE025AD; _ga=GA1.2.2033543352.1542960994',

    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

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
