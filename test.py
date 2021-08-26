#-*- coding: utf-8 -*-
from datetime import datetime

def parse_date():
    date_str = '2021년 8월 24일 화요일'
    date_str2 = date_str[:date_str.rfind(' ')]

    time_t = datetime.strptime(date_str2, '%Y년 %m월 %d일')
    str_time = time_t.strftime('%Y%m%d')

    print(str_time)

from PIL import Image
from PIL.ExifTags import TAGS

def read_exif():
    img = Image.open('test.jpg')
    info = img.getexif()
    
    for tag, value in info.items():
        decoded_tag = TAGS.get(tag)
        print(f'{decoded_tag} : {value}')
    pass

    try:
        print(f'{TAGS[306]} : {info[306]} {type(info[306])}')
        return info[306]
    except:
        print('No Datetime at EXIF')
        return ''

import os
def read_datetime_from_file(filename):
    stat = os.stat(filename)
    print(stat)

if __name__ == '__main__':
    exif_time:str = read_exif()

    read_datetime_from_file('test.jpg')

    if exif_time == '':
        pass
    else:
        import time
        tm = time.mktime(datetime(*[int(x) for x in exif_time.replace(' ', ':').split(':')]).timetuple())
        print(tm)
        os.utime('test.jpg', (tm, tm))

        read_datetime_from_file('test.jpg')
        pass
