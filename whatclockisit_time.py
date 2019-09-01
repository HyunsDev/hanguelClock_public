import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request

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


if __name__ == "__main__":
    # print(korean_time())
    print("텍스트 : " + korean_text())
    # print(korean_clock())
