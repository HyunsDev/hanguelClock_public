# -*- coding:utf-8 -*-
import ctypes
import os
import time
import datetime

from PIL import Image, ImageDraw, ImageFont

import setting
from hanguel_time import korean_time, korean_text

ct = setting.Custom()

korean_nowtext = korean_text()

now = datetime.datetime.now()

korean_nowtime = korean_time()
nowminu = now.strftime('%M')

msg = str(korean_nowtext) + "\n" + str(korean_nowtime)

imagepath = Image.open(ct.wallpaper_source)

font = ImageFont.truetype(os.path.join(ct.fontfolder, ct.fontfile), ct.fontsize)
draw = ImageDraw.Draw(imagepath)
w, h = draw.textsize(msg, font=font)
draw.text(((ct.screen_W - w) / 2, (ct.screen_H - h) / 2 - 50), msg, fill=ct.text_fill, font=font, align=ct.text_align)
savedimage = ct.wallpaper_image
imagepath.save(savedimage)
imagepath = os.path.normpath(savedimage)
ctypes.windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)
print("바탕화면 리프레쉬 완료")

while True:

    now = datetime.datetime.now()

    if now.strftime('%S') == "00":
        korean_nowtime = korean_time()
        nowminu = now.strftime('%M')

        print(nowminu)

        msg = str(korean_nowtext) + "\n" + str(korean_nowtime)

        imagepath = Image.open(ct.wallpaper_source)
        font = ImageFont.truetype(os.path.join(ct.fontfolder, ct.fontfile), ct.fontsize)
        draw = ImageDraw.Draw(imagepath)
        w, h = draw.textsize(msg, font=font)
        draw.text(((ct.screen_W - w) / 2, (ct.screen_H - h) / 2 - 50), msg, fill=ct.text_fill, font=font,
                  align=ct.text_align)
        savedimage = ct.wallpaper_image
        imagepath.save(savedimage)
        imagepath = os.path.normpath(savedimage)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)
        print("바탕화면 리프레쉬 완료")

        if nowminu == '59':
            korean_nowtext = korean_text()
        elif nowminu == '29':
            korean_nowtext = korean_text()

        time.sleep(50)

    if ct.clock_on == "False":
        break
