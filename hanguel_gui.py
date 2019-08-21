import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QRadioButton, QMenu, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox, QSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from hanguel_time import korean_time


class hanguel_clock(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        #그리드 
        grid = QGridLayout()
        grid.addWidget(self.hanguel_groupbox(), 0, 0)
        grid.addWidget(self.custom_groupbox(), 1, 0)
        grid.addWidget(self.other_groupbox(), 2, 0)
        #grid.addWidget(self.createPushButtonGroup(), 1, 1)

        self.setLayout(grid)


        #창
        self.setWindowTitle('지금몇시계 설정')
        self.setWindowIcon(QIcon('지금몇시계.png'))
        self.setFixedSize(400,700)
        self.center()
        self.show()

    def hanguel_groupbox(self):

        groupbox = QGroupBox('지금몇시계')

        clock_on_label = QLabel("지금몇시계 활성화", self)
        clock_on = QRadioButton("활성화")
        clock_off = QRadioButton("비활성화")
        clock_on.setChecked(True)

        clock_box = QHBoxLayout()
        clock_box.addWidget(clock_on_label)
        clock_box.addWidget(clock_on)
        clock_box.addWidget(clock_off)

        text_on_label = QLabel("문구 표시 (미지원)", self) #아직 지원하지 않음
        text_on = QRadioButton("활성화")
        text_off = QRadioButton("비활성화")
        text_on.setChecked(True)

        text_box = QHBoxLayout()
        text_box.addWidget(text_on_label)
        text_box.addWidget(text_on)
        text_box.addWidget(text_off)

        #텍스트 문구 위치 추가하기

        hanguel_box = QVBoxLayout()
        hanguel_box.addLayout(clock_box)
        hanguel_box.addLayout(text_box)

        groupbox.setLayout(hanguel_box)

        return groupbox

    def custom_groupbox(self):
        groupbox = QGroupBox('커스텀마이징')

        self.wallpaper_lable = QLabel("배경사진")
        self.wallpaper_url = QLineEdit()
        self.wallpaper_button = QPushButton("파일 선택")
        self.wallpaper_button.clicked.connect(self.select_wallpaper)

        wallpaper_box = QHBoxLayout()
        wallpaper_box.addWidget(self.wallpaper_lable)
        wallpaper_box.addWidget(self.wallpaper_url)
        wallpaper_box.addWidget(self.wallpaper_button)

        self.font_lable = QLabel("폰트")
        self.font_url = QLineEdit()
        self.font_button = QPushButton("파일 선택")
        self.font_button.clicked.connect(self.select_font)

        font_box = QHBoxLayout()
        font_box.addWidget(self.font_lable)
        font_box.addWidget(self.font_url)
        font_box.addWidget(self.font_button)

        self.clock_label = QLabel("시계 위치")
        self.clock_combo = QComboBox(self)
        self.clock_combo.addItem("왼쪽")
        self.clock_combo.addItem("가운데")
        self.clock_combo.addItem("오른쪽")

        clock_box = QHBoxLayout()
        clock_box.addWidget(self.clock_label)
        clock_box.addWidget(self.clock_combo)

        self.fontsize_label = QLabel("폰트 크기")
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(10, 200)
        self.fontsize_spin.setValue(60)

        fontsize_box = QHBoxLayout()
        fontsize_box.addWidget(self.fontsize_label)
        fontsize_box.addWidget(self.fontsize_spin)

        self.textalign_label = QLabel("폰트 정렬")
        self.textalign_combo = QComboBox(self)
        self.textalign_combo.addItem("왼쪽 정렬")
        self.textalign_combo.addItem("가운데 정렬")
        self.textalign_combo.addItem("오른쪽 정렬")

        textalign_box = QHBoxLayout()
        textalign_box.addWidget(self.textalign_label)
        textalign_box.addWidget(self.textalign_combo)

        custom_box = QVBoxLayout()
        custom_box.addLayout(wallpaper_box)
        custom_box.addLayout(font_box)
        custom_box.addLayout(clock_box)
        custom_box.addLayout(fontsize_box)
        custom_box.addLayout(textalign_box)

        groupbox.setLayout(custom_box)
        return groupbox

    def other_groupbox(self):
        groupbox = QGroupBox("그 외의 것들")

        self.timezone_label = QLabel("시간대(GMT+)")
        self.timezone_spin = QSpinBox()
        self.timezone_spin.setRange(0, 12)
        self.timezone_spin.setValue(9)

        timezone_box = QHBoxLayout()
        timezone_box.addWidget(self.timezone_label)
        timezone_box.addWidget(self.timezone_spin)

        self.screensize_label = QLabel("화면크기(너비x높이)")
        self.screensize_W = QSpinBox()
        self.screensize_W.setRange(100,4096)
        self.screensize_W.setValue(1920)
        self.screensize_H = QSpinBox()
        self.screensize_H.setRange(100, 2160)
        self.screensize_H.setValue(1080)

        screensize_box = QHBoxLayout()
        screensize_box.addWidget(self.screensize_label)
        screensize_box.addWidget(self.screensize_W)
        screensize_box.addWidget(self.screensize_H)

        custom_box = QVBoxLayout()
        custom_box.addLayout(timezone_box)
        custom_box.addLayout(screensize_box)

        groupbox.setLayout(custom_box)
        return groupbox


    def select_wallpaper(self):
        fname = QFileDialog.getOpenFileName(self)
        self.wallpaper_url.setText(fname[0])

    def select_font(self):
        fname = QFileDialog.getOpenFileName(self)
        self.font_url.setText(fname[0])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = hanguel_clock()
    sys.exit(app.exec_())