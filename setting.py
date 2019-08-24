# -*- coding: utf-8 -*-

f = open("F:/19_hanguelclock/hanguel_gui/data.txt", "r")
lines = f.readlines()
print(lines)
f.close()

print(lines[0])
print(lines[1])
print(lines[2])
print(lines[3])
print(lines[4])
print(lines[5])
print(lines[6])
print(lines[7])
print(lines[8])
print(lines[9])
print(lines[10])
print(lines[11])
print(lines[12])
print("=====================")


#'''
class Custom:
    def __init__(self):
        self.clock_on = lines[0].replace("\\n","")
        self.wallpaper_source = str(lines[1]).replace("\\n","")
        self.fontsize = int(str(lines[2]).replace("\\n",""))
        self.fontfile = lines[3].replace("\\n","")
        self.fontfolder = lines[4].replace("\\n","")
        self.text_on = lines[5].replace("\\n","")
        self.screen_W = int(str(lines[6]).replace("\\n",""))
        self.screen_H = int(str(lines[7]).replace("\\n",""))
        self.text_align = lines[8].replace("\\n","")
        self.text_fill = lines[9].replace("\\n","")
        self.wallpaper_mode = lines[10].replace("\\n","")
        self.wallpaper_image = lines[11].replace("\\n","")
        self.timezone = int(lines[12])

ct = Custom()


print(ct.clock_on)
print(ct.wallpaper_source)
print(ct.fontsize)
print(ct.fontfile)
print(ct.fontfolder)
print(ct.text_on)
print(ct.screen_W)
print(ct.screen_H)
print(ct.text_align)
print(ct.text_fill)
print(ct.wallpaper_mode)
print(ct.wallpaper_image)
print(ct.timezone)

'''
class Custom:
    def __init__(self):
        self.clock_on = True
        self.wallpaper_source = "hanguel_wallpaper.png"
        self.fontsize = 60
        self.fontfile = "SSFlower.ttf"
        self.fontfolder = "F:/19_hanguelclock/hanguel_gui/font"
        self.text_on = True
        self.screen_W = 1920
        self.screen_H = 1080
        self.text_align = "center"
        self.text_fill = "white"
        self.wallpaper_mode = "fix"
        self.wallpaper_image = "F:/19_hanguelclock/hanguel_gui/image/saved/hanguel_clock.png"
        self.timezone = 9
'''