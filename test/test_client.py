#-*- encoding:UTF-8 -*-
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Weather and Money show programme. Copyright (c) 2020 Author: Unicoder Ji (unicoder@sohu.com)
#
import math
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import mmap
import contextlib

#coding=utf-8

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype("/home/pi/Prog/ssd1306/msyh.ttc", 15)
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as this python script!
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

# Create drawing object.
draw = ImageDraw.Draw(image)

# Define text and get total width.
#text = u'你好，北京' + '0' + u'度' + u'零钱：2195.00 ' + u'浦发：749.00 ' + u'余额宝：66.15' 
#text = 'SSD1306 ORGANIC LED DISPLAY. THIS IS AN OLD SCHOOL DEMO SCROLLER!! GREETZ TO: LADYADA & THE ADAFRUIT CREW, TRIXTER, FUTURE CREW, AND FARBRAUSCH'
#text = u'你好，我们很好。北京 0'+chr(0x2103)+', '
#text = u"你好，北京 0" + u'\x00\xb0' + u'\x21\x03' + u'\x24\x60'
#text1 = u"你好,北京 0" + unichr(0x2103) + u"北戴河 10" + unichr(0x2103) + u"三亚 25" + unichr(0x2103) + u"青岛 5" + unichr(0x2103) + u"大连 0" + unichr(0x2103)
text1 = "Test to weather and money! Author: unicoder@sohu.com"
text2 = u"   零钱：2500.00 " + u"  浦发：749.00 " + u"  余额宝：66.15"


# Set animation and sine wave parameters.
amplitude = height/4
#offset = height/2 - 4
offset = -2
velocity = -3
startpos = width

# Animate text moving in sine wave.
print('Press Ctrl-C to quit.')
pos = startpos
count = 0
first_run = True
#draw.rectangle((0,0,width,height), outline=0, fill=0)
while True:
    count += 1

    if count > 100 and not first_run:
        with open("/home/pi/Prog/ssd1306/test/data","r") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 1024, access=mmap.ACCESS_READ)) as m:
                text1 = m.read(1024)
                text1 = str(text1, encoding = 'utf-8').replace('\x00', '')
        count = 0   # count归零
        #print (text1)
    if len(text1) > len(text2):
        maxwidth, unused = draw.textsize(text1, font=font)
    else:
        maxwidth, unused = draw.textsize(text2, font=font)
    # Clear image buffer by drawing a black filled box.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    # Enumerate characters and draw them offset vertically based on a sine wave.
    x = pos
    for i, c in enumerate(text1):
        # Stop drawing if off the right side of screen.
        if x > width:
            break
        # Calculate width but skip drawing if off the left side of screen.
        if x < -10:  #这里10表示入10个像素进去这个字就不再显示了。如果字体大，字到一半就消失了。可以设置成字体的宽度。
            char_width, char_height = draw.textsize(c, font=font)
            x += char_width
            continue
        # Calculate offset from sine wave.
        #y = offset+math.floor(amplitude*math.sin(x/float(width)*2.0*math.pi))
        y = offset
        # Draw text.
        draw.text((x, y), c, font=font, fill=255)
        # Increment x position based on chacacter width.
        char_width, char_height = draw.textsize(c, font=font)
        x += char_width
    x = pos
    for i, c in enumerate(text2):
        if x > width:
            break
        if x < -10:
            char_width,char_height = draw.textsize(c, font=font)
            x += char_width
            continue
        y = offset+16
        draw.text((x, y), c, font=font, fill=255)
        char_width, char_height = draw.textsize(c, font=font)
        x += char_width
    # Draw the image buffer.
    disp.image(image)
    disp.display()
    # Move position for next frame.
    pos += velocity
    # Start over if text has scrolled completely off left side of screen.
    if pos < -maxwidth + width - 50:  #接到尾部50个像素就从新（从头）显示。
        first_run = False
        pos = startpos
    # Pause briefly before drawing next frame.
    time.sleep(0.1)
