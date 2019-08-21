#-*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import os, glob, ctypes, time
from hanguel_time import korean_clock
import setting

ct = setting.Custom()

while True:
    msg = korean_clock()
    imagepath = Image.open(ct.wallpaper_source)
    font = ImageFont.truetype(os.path.join(ct.fontfolder, ct.fontfile),ct.fontsize)
    draw = ImageDraw.Draw(imagepath)
    w, h = draw.textsize(msg, font=font)
    draw.text(((ct.screen_W-w)/2,(ct.screen_H-h)/2-50), msg, fill=ct.text_fill, font=font, align=ct.text_align)
    savedimage = ct.wallpaper_image
    imagepath.save(savedimage)
    imagepath = os.path.normpath (savedimage)
    ctypes.windll.user32.SystemParametersInfoW(20,0,imagepath,0)
    time.sleep(40)
