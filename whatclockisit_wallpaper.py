# -*- coding:utf-8 -*-
from ctypes import windll
from os import path
from time import sleep
import datetime
from configparser import ConfigParser
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
from PIL import Image, ImageDraw, ImageFont
import winreg

key = winreg.HKEY_LOCAL_MACHINE
subkey = "SOFTWARE\\WhatClockIsIt"
registry = winreg.CreateKey(key, subkey)
inipath, _ = winreg.QueryValueEx(registry, "datainipath")



#함수 제작

def korean_time():
    now = datetime.datetime.now()
    nowtime = now.strftime('%H%M')
    nowtime = str(nowtime)
    if nowtime == '0000':
        showtime = "지금은 자정이야"
        return showtime
    elif nowtime == '1200':
        showtime = "지금은 정오야"
        return showtime
    else:
        hour = int(nowtime[0:2])
        if hour == 00:
            hour = 24
        # showhour = ""
        minu = int(nowtime[2:4])
        # showminu = ""
        time_map_hour = {0: "", 1: "한", 2: "두", 3: "세", 4: "네", 5: "다섯", 6: "여섯", 7: "일곱", 8: "여덟", 9: "아홉"}
        time_map_minu = {0: "", 1: "일", 2: "이", 3: "삼", 4: "사", 5: "오", 6: "육", 7: "칠", 8: "팔", 9: "구"}

        # 오전 오후 구문
        if hour >= 21:
            showhour = "밤 "
        elif hour >= 17:
            showhour = "저녁 "
        elif hour >= 15:
            showhour = "오후 "
        elif hour >= 11:
            showhour = "점심 "
        elif hour >= 7:
            showhour = "아침 "
        elif hour >= 5:
            showhour = "이른 아침 "
        elif hour >= 3:
            showhour = "새벽 "
        elif hour >= 1:
            showhour = "늦은 밤 "
        elif hour >= 0:
            showhour = "밤 "

            # 24 to 12
        if hour > 12:
            hour = hour - 12

        # 시간 구문
        if hour >= 10:
            hour = hour - 10
            showhour = showhour + "열" + time_map_hour[hour] + " 시 "
        else:
            showhour = showhour + time_map_hour[hour] + " 시 "

        # 분 구문
        showminu = ""
        if minu >= 10:
            if minu > 20:
                minu_ten = int(str(minu)[0])
                showminu = time_map_minu[minu_ten] + "십"
            else:
                showminu = "십"
            minu_one = int(str(minu)[1])
            showminu = showminu + time_map_minu[minu_one] + " 분"
        elif minu > 0:
            minu_one = int(str(minu)[0])
            showminu = showminu + time_map_minu[minu_one] + " 분"
        else:
            showminu = showminu + "정각"

            # 최종 출력 구문
        showtime = showhour + showminu + "이야."
        return showtime

def korean_text():
    now = datetime.datetime.now()
    nowdate = now.strftime('%H')
    time_now = int(nowdate) // 2 + 1
    time_now = int(time_now)
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        url = urlopen('http://hyuns.space/api/hanguel/1/')
        soup = BeautifulSoup(url, "lxml")
        soup = str(soup.body)
        soup = soup.replace("<body>", "")
        soup = soup.replace("</body>", "")
        soup = soup.strip()
        show_text = soup


    except:
        print("서버연결 오류발생")
        if time_now == 1:
            show_text = "좋은 꿈 꿔"
        elif time_now == 2:
            show_text = "아직 안 자고 뭐해?"
        elif time_now == 3:
            show_text = "오늘도 좋은 아침"
        elif time_now == 4:
            show_text = "잠은 잘 잤니?"
        elif time_now == 5:
            show_text = "아침은 먹었니?"
        elif time_now == 6:
            show_text = "지금 뭐해?"
        elif time_now == 7:
            show_text = "뭐하고 있어?"
        elif time_now == 8:
            show_text = "기재기 한 번 어때?"
        elif time_now == 9:
            show_text = "힘들지 않아?"
        elif time_now == 10:
            show_text = "오늘 저녁 맛있었어?"
        elif time_now == 11:
            show_text = "지금 뭐해?"
        elif time_now == 12:
            show_text = "굿나잇!"

    return show_text

def korean_clock():
    showtime = korean_text() + "\n" + korean_time()
    return showtime

def hanguel_wallpaper(wallpaper_source, fontfolder, fontfile, fontsize, screen_W, screen_H, clock_position_X, clock_position_Y ,text_fill, text_align, wallpaper_temp, text_on):
    korean_nowtext = korean_text()
    now = datetime.datetime.now()
    korean_nowtime = korean_time()
    nowminu = now.strftime('%M')
    if text_on == "off":
        msg = str(korean_nowtime)
    else:
        msg = str(korean_nowtext) + "\n" + str(korean_nowtime)
    imagepath = Image.open(wallpaper_source)
    font = ImageFont.truetype(path.join(fontfolder, fontfile), fontsize)
    draw = ImageDraw.Draw(imagepath)
    w, h = draw.textsize(msg, font=font)

    draw.text(((screen_W - w) / 2 + int(clock_position_X), (screen_H - h ) / 2 - 50 + int(clock_position_Y)), msg, fill=text_fill, font=font, align=text_align)
    savedimage = wallpaper_temp
    imagepath.save(savedimage)
    imagepath = path.normpath(savedimage)
    windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)

    if nowminu == '59':
        korean_nowtext = korean_text()
    elif nowminu == '29':
        korean_nowtext = korean_text()

config = ConfigParser()
config.read(inipath)
data = config['main']
data['clock_on'] = "on"
with open(inipath, 'w') as main:  # save
    config.write(main)
ws = data['wallpaper_source']
ffolder = data['fontfolder']
ffile = data['fontfile']
fs = int(data['fontsize'])
sW = int(data['screen_W'])
sH = int(data['screen_H'])
cpX = int(data['clock_position_X'])
cpY = int(data['clock_position_Y'])
tf = data['text_fill']
ta = data['text_align']
wt = data['wallpaper_temp'] + "temp.png"
to = data['text_on']
#hanguel_wallpaper(data['wallpaper_source'], data['fontfolder'], data['fontfile'], int(data['fontsize']), int(data['screen_W']), int(data['screen_H']), int(data['clock_position_X']), int(data['clock_position_Y']) ,data['text_fill'], data['text_align'], data['wallpaper_temp'])
hanguel_wallpaper(ws, ffolder, ffile, fs, sW, sH, cpX, cpY, tf, ta, wt, to)
print("Wallpaper 시작")

try:
    while True:
        try:
            now = datetime.datetime.now()
            config = ConfigParser()
            config.read(inipath)
            data = config['main']

            if data['clock_on'] == "off":
                sleep(1)

            if data["reflesh"] == "yes":
                ws = data['wallpaper_source']
                ffolder = data['fontfolder']
                ffile = data['fontfile']
                fs = int(data['fontsize'])
                sW = int(data['screen_W'])
                sH = int(data['screen_H'])
                cpX = int(data['clock_position_X'])
                cpY = int(data['clock_position_Y'])
                tf = data['text_fill']
                ta = data['text_align']
                wt = data['wallpaper_temp'] + "temp.png"
                to = data['text_on']
                hanguel_wallpaper(ws, ffolder, ffile, fs, sW, sH, cpX, cpY, tf, ta, wt, to)

                data['reflesh'] = "no"
                with open('data.ini', 'w') as main:  # save
                    config.write(main)
                print("바탕화면 리프레쉬 완료")

            if now.strftime('%S') == "00":
                hanguel_wallpaper(ws, ffolder, ffile, fs, sW, sH, cpX, cpY, tf, ta, wt, to)
                print("바탕화면 변경 완료")
                sleep(0.9)

            if data['clock_on'] == "offing":
                ws = data['wallpaper_source']
                ffolder = data['fontfolder']
                ffile = data['fontfile']
                fs = int(data['fontsize'])
                sW = int(data['screen_W'])
                sH = int(data['screen_H'])
                cpX = int(data['clock_position_X'])
                cpY = int(data['clock_position_Y'])
                tf = data['text_fill']
                ta = data['text_align']
                wt = data['wallpaper_temp'] + "temp.png"

                msg = "지금몇시계 영업종료"
                imagepath = Image.open(ws)
                font = ImageFont.truetype(path.join(ffolder, ffile), fs)
                draw = ImageDraw.Draw(imagepath)
                w, h = draw.textsize(msg, font=font)

                draw.text(((sW - w) / 2 + int(cpX), (sH - h) / 2 - 50 + int(cpY)), msg,
                          fill=tf, font=font, align=ta)
                savedimage = data['wallpaper_temp'] + "close.png"
                imagepath.save(savedimage)

                imagepath = path.normpath(savedimage)
                windll.user32.SystemParametersInfoW(20, 0, imagepath, 0)

                data['clock_on'] = "off"
                with open(inipath, 'w') as main:  # save
                    config.write(main)

                print("지금몇시계 영업종료")


            if data['check_live_call'] == "call":
                data['check_live_call'] = "waiting"
                data['check_live_back'] = "back"
                with open(inipath, 'w') as main:  # save
                    config.write(main)
                if data['clock_on'] == "on":
                    print("wallpaper의 말 : 시계도 켜져있고 나도 살아있어요!!")
                else:
                    print("wallpaper의 말 : 시계는 죽었지만 나는 살아있어요!!")

            if data['clock_on'] == "on":
                sleep(0.7)

        except Exception as e:
            snow = datetime.datetime.now()
            print("에러 발생")
            f = open("log/error.log", "a")
            data = " 종료 되지는 않은 에러: %s/%s/%s %s|%s|%s| \n 에러내용 : %s\n" % (
            snow.year, snow.month, snow.day, snow.hour, snow.minute, snow.second, str(e))
            f.close()
except Exception as e:
    snow = datetime.datetime.now()
    print("심각한 에러 발생")
    f = open("log/error.log", "a")
    data = "심각한 에러 : %s/%s/%s %s|%s|%s \n 에러내용 : %s\n" % (snow.year, snow.month, snow.day, snow.hour, snow.minute, snow.second, str(e))
    f.close()
