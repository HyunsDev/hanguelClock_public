import configparser
import subprocess
import sys
import winreg
import time
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QButtonGroup, QWidget, QRadioButton, QSpinBox, QLabel, QGroupBox, \
    QLineEdit, QFileDialog, QVBoxLayout, QGridLayout, QDesktopWidget, QApplication

key = winreg.HKEY_LOCAL_MACHINE
subkey = "SOFTWARE\\WhatClockIsIt"
registry = winreg.CreateKey(key, subkey)
inipath, _ = winreg.QueryValueEx(registry, "datainipath")

config = configparser.ConfigParser()
config.read(inipath)
data = config['main']

sys.path.insert(0, 'pkgs')

data['check_live_call'] = "call"
data['check_live_back'] = "waiting"
with open(inipath, 'w') as main:  # save
    config.write(main)
time.sleep(0.05)

if data["check_live_back"] == "back":
    print("gui : wallpaper가 살아있어요!!!")
else:
    print("gui : wallpaper가 죽어있어요!!!")
    data['clock_on'] = "off"
    with open(inipath, 'w') as main:  # save
        config.write(main)

class hanguel_clock(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        key = winreg.HKEY_LOCAL_MACHINE
        subkey = "SOFTWARE\\WhatClockIsIt"
        registry = winreg.CreateKey(key, subkey)
        inipath, _ = winreg.QueryValueEx(registry, "datainipath")
        winreg.CloseKey(registry)

        config = configparser.ConfigParser()
        config.read(inipath)
        data = config['main']

        #그리드 
        grid = QGridLayout()
        grid.addWidget(self.hanguel_groupbox(), 0, 0)
        grid.addWidget(self.custom_groupbox(), 1, 0)
        grid.addWidget(self.other_groupbox(), 2, 0)

        self.setLayout(grid)


        #창
        self.setWindowTitle('지금몇시계 설정')
        self.setWindowIcon(QIcon('지금몇시계.png'))
        self.setFixedSize(400,700)
        self.center()
        self.show()

    def hanguel_groupbox(self):

        groupbox = QGroupBox('지금몇시계')

        hanguel_box = QVBoxLayout()

        # 지금 몇시계 활성화
        clock_on_label = QLabel("지금몇시계 활성화", self)
        clock_on_group = QButtonGroup(self)
        clock_on = QRadioButton("활성화")
        clock_off = QRadioButton("비활성화")
        clock_on_group.addButton(clock_on)
        clock_on_group.addButton(clock_off)


        if data['clock_on'] == "off":
            clock_off.setChecked(True)
        else:
            clock_on.setChecked(True)

        clock_on.clicked.connect(self.clock_on)
        clock_off.clicked.connect(self.clock_off)

        clock_box = QHBoxLayout()
        clock_box.addWidget(clock_on_label)
        clock_box.addWidget(clock_on)
        clock_box.addWidget(clock_off)

        hanguel_box.addLayout(clock_box)
        #

        # 문구 표시 활성화
        text_on_label = QLabel("문구 표시 (미지원)", self) #아직 지원하지 않음
        text_on_group = QButtonGroup(self)
        text_on = QRadioButton("활성화")
        text_off = QRadioButton("비활성화")
        text_on_group.addButton(text_on)
        text_on_group.addButton(text_off)
        if data['text_on'] == "off":
            text_off.setChecked(True)
        else:
            text_on.setChecked(True)

        text_on.toggled.connect(self.text_on)
        text_off.toggled.connect(self.text_off)

        text_box = QHBoxLayout()
        text_box.addWidget(text_on_label)
        text_box.addWidget(text_on)
        text_box.addWidget(text_off)

        hanguel_box.addLayout(text_box)
        #

        groupbox.setLayout(hanguel_box)

        return groupbox

    def clock_on(self):
        data['clock_on'] = "on"
        data['check_live_call'] = "call"
        data['check_live_back'] = "waiting"
        with open(inipath, 'w') as main:  # save
            config.write(main)

        time.sleep(0.1)
        if data['check_live_back'] != "back":
            subprocess.Popen('whatclockisit_wallpaper.exe')
        time.sleep(1)

    def clock_off(self):
        data['clock_on'] = "offing"
        data['check_live'] = "connect"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        time.sleep(1)

    def text_on(self):
        data['text_on'] = "on"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        self.reflesh()

    def text_off(self):
        data['text_on'] = "off"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        self.reflesh()

    def custom_groupbox(self):
        groupbox = QGroupBox('커스텀마이징')

        self.wallpaper_lable = QLabel("배경사진")
        self.wallpaper_url = QLineEdit(data['wallpaper_source'])
        self.wallpaper_button = QPushButton("파일 선택")
        self.wallpaper_button.clicked.connect(self.select_wallpaper)

        wallpaper_box = QHBoxLayout()
        wallpaper_box.addWidget(self.wallpaper_lable)
        wallpaper_box.addWidget(self.wallpaper_url)
        wallpaper_box.addWidget(self.wallpaper_button)

        font_url = data['fontfolder'] + "/" + data['fontfile']
        self.font_lable = QLabel("폰트")
        self.font_url = QLineEdit(font_url)
        self.font_button = QPushButton("파일 선택")
        self.font_button.clicked.connect(self.select_font)

        font_box = QHBoxLayout()
        font_box.addWidget(self.font_lable)
        font_box.addWidget(self.font_url)
        font_box.addWidget(self.font_button)

        self.clock_position_label = QLabel("시계 위치(중앙으로부터)", self)

        self.clock_position_X = QSpinBox()
        self.clock_position_X.setRange(-4096, 4096)
        self.clock_position_X.setValue(int(data['clock_position_X']))
        self.clock_position_X.valueChanged.connect(self.clock_pos_X_set)

        self.clock_position_Y = QSpinBox()
        self.clock_position_Y.setRange(-2160, 2160)
        self.clock_position_Y.setValue(int(data['clock_position_Y']))
        self.clock_position_Y.valueChanged.connect(self.clock_pos_Y_set)

        clock_position_box = QHBoxLayout()
        clock_position_box.addWidget(self.clock_position_label)
        clock_position_box.addWidget(self.clock_position_X)
        clock_position_box.addWidget(self.clock_position_Y)

        self.fontsize_label = QLabel("폰트 크기")
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(10, 200)
        self.fontsize_spin.setValue(int(data['fontsize']))
        self.fontsize_spin.valueChanged.connect(self.fontsize_set)

        fontsize_box = QHBoxLayout()
        fontsize_box.addWidget(self.fontsize_label)
        fontsize_box.addWidget(self.fontsize_spin)

        textalign_label = QLabel("글씨 정렬", self)  # 아직 지원하지 않음
        textalign_left = QRadioButton("왼쪽 정렬")
        textalign_center = QRadioButton("가운데 정렬")
        textalign_right = QRadioButton("오른쪽 정렬")

        if data['text_align'] == "left":
            textalign_left.setChecked(True)
        elif data['text_align'] == "right":
            textalign_right.setChecked(True)
        else:
            textalign_center.setChecked(True)

        textalign_left.clicked.connect(self.ta_l)
        textalign_center.clicked.connect(self.ta_c)
        textalign_right.clicked.connect(self.ta_r)


        textalign_box = QHBoxLayout()
        textalign_box.addWidget(textalign_label)
        textalign_box.addWidget(textalign_left)
        textalign_box.addWidget(textalign_center)
        textalign_box.addWidget(textalign_right)
        #

        custom_box = QVBoxLayout()
        custom_box.addLayout(wallpaper_box)
        custom_box.addLayout(font_box)
        custom_box.addLayout(clock_position_box)
        custom_box.addLayout(fontsize_box)
        custom_box.addLayout(textalign_box)

        groupbox.setLayout(custom_box)
        return groupbox

    def clock_pos_X_set(self):
        val = self.clock_position_X.value()

        data['clock_position_x'] = str(val)
        with open(inipath, 'w') as main:  # save
            config.write(main)

    def clock_pos_Y_set(self):
        val = self.clock_position_Y.value()
        data['clock_position_y'] = str(val)
        with open(inipath, 'w') as main:  # save
            config.write(main)

    def fontsize_set(self):
        data['fontsize'] = str(self.fontsize_spin.value())
        with open(inipath, 'w') as main:  # save
            config.write(main)

    def ta_l(self):
        data['text_align'] = "left"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        self.reflesh()

    def ta_c(self):
        data['text_align'] = "center"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        self.reflesh()

    def ta_r(self):
        data['text_align'] = "right"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        self.reflesh()

    def other_groupbox(self):
        groupbox = QGroupBox("그 외의 것들")

        self.timezone_label = QLabel("시간대 보정")
        self.timezone_spin = QSpinBox()
        self.timezone_spin.setRange(-12, 12)
        self.timezone_spin.setValue(int(data['timezone']))
        self.timezone_spin.valueChanged.connect(self.timezone_set)

        timezone_box = QHBoxLayout()
        timezone_box.addWidget(self.timezone_label)
        timezone_box.addWidget(self.timezone_spin)

        self.screensize_label = QLabel("화면크기(너비x높이)")
        self.screensize_W = QSpinBox()
        self.screensize_W.setRange(100,4096)
        self.screensize_W.setValue(int(data['screen_W']))
        self.screensize_W.valueChanged.connect(self.screen_W_set)

        self.screensize_H = QSpinBox()
        self.screensize_H.setRange(100, 2160)
        self.screensize_H.setValue(int(data['screen_H']))
        self.screensize_H.valueChanged.connect(self.screen_H_set)

        screensize_box = QHBoxLayout()
        screensize_box.addWidget(self.screensize_label)
        screensize_box.addWidget(self.screensize_W)
        screensize_box.addWidget(self.screensize_H)

        #self.discord_label = QLabel("https://discord.gg/AwYVNNA")

        #discord_box = QHBoxLayout()
        #discord_box.addWidget(self.discord_label)

        #테스트 전용 구문

        #self.test_button = QPushButton("라이브 테스트")
        #self.test_button.clicked.connect(self.test)

        #test_box = QHBoxLayout()
        #test_box.addWidget(self.test_button)

        self.notice_label = QLabel("시계위치와 폰트크기, 시간데 보정과 화면크기는\n새로고침을 눌러주세요!")

        notice_box = QHBoxLayout()
        notice_box.addWidget(self.notice_label)

        #테스트 전용 구문 끝

        self.reflesh_button = QPushButton("적용하고 새로고침")
        self.reflesh_button.clicked.connect(self.reflesh)

        reflesh_box = QHBoxLayout()
        reflesh_box.addWidget(self.reflesh_button)

        custom_box = QVBoxLayout()
        custom_box.addLayout(timezone_box)
        custom_box.addLayout(screensize_box)

        #테스트 전용 구문
        #custom_box.addLayout(test_box)
        #테스트 전용 구문 끝
        custom_box.addLayout(reflesh_box)
        #custom_box.addLayout(discord_box)
        custom_box.addLayout(notice_box)

        groupbox.setLayout(custom_box)
        return groupbox

    '''
    def test(self):
        config = configparser.ConfigParser()
        config.read(inipath)
        data = config['main']

        data['check_live_call'] = "call"
        data['check_live_back'] = "waiting"
        with open(inipath, 'w') as main:  # save
            config.write(main)

        time.sleep(1)

        config = configparser.ConfigParser()
        config.read(inipath)
        data = config['main']

        if data['check_live_back'] == "back":
            print("GUI : wallpaper는 살아있음")
        elif data['check_live_back'] == "waiting":
            print("GUI : wallpaper는 죽어있음")
    '''

    def screen_W_set(self):
        val = self.screensize_W.value()
        data['screen_W'] = str(val)
        with open(inipath, 'w') as main:  # save
            config.write(main)

    def screen_H_set(self):
        val = self.screensize_H.value()

        data['screen_H'] = str(val)
        with open(inipath, 'w') as main:  # save
            config.write(main)

    def timezone_set(self):
        val = self.timezone_spin.value()

        data['timezone'] = str(val)
        with open(inipath, 'w') as main:  # save
            config.write(main)


    def select_wallpaper(self):
        title = "배경사진을 골라주세요"
        filter = "png(*.png)"
        fname = QFileDialog.getOpenFileName(self, title, None, filter)
        if fname[0] != "":
            self.wallpaper_url.setText(fname[0])
            data['wallpaper_source'] = fname[0]
            with open(inipath, 'w') as main:  # save
                config.write(main)

    def select_font(self):
        title = "폰트파일을 골라주세요"
        filter = "폰트파일(*.ttf *.otf)"
        fname = QFileDialog.getOpenFileName(self, title, None, filter)
        print(fname)
        if fname[0] != "":
            fname = fname[0]
            sp = fname.rfind("/")
            ffile = fname[sp+1:]
            ffolder = fname[:sp]
            data['fontfile'] = ffile
            data['fontfolder'] = ffolder
            with open(inipath, 'w') as main:  # save
                config.write(main)
            self.font_url.setText(fname)

    def reflesh(self):
        data['reflesh'] = "yes"
        data['check_live_call'] = "call"
        data['check_live_back'] = "waiting"
        with open(inipath, 'w') as main:  # save
            config.write(main)
        time.sleep(0.1)
        if data['check_live_back'] == "waiting":
            subprocess.Popen('python whatclockisit_wallpaper.py')



    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = hanguel_clock()
    sys.exit(app.exec_())