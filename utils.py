import json
import time, os
import requests
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def download_img(url, basepath, filename):
    with open(f'{basepath}/{filename}.jpg', "wb") as file:        
        res = requests.get(url)
        file.write(res.content)

def download_movie(url, basepath, filename):
    with open(f'{basepath}/{filename}.mp4', "wb") as file:
        res = requests.get(url)
        file.write(res.content)

def parse_datetime(report_date):
    short_date = report_date[:report_date.rfind(' ')]
    try:
        time_t = datetime.strptime(short_date, '%Y년 %m월 %d일')
        str_time = time_t.strftime('%Y_%m_%d')
    except:
        str_time = f'{short_date.split(".")[0]}_{int(short_date.split(".")[1]):02d}_{int(short_date.split(".")[2]):02d}'

    #print(str_time) # 2021_08_24
    return str_time


def get_exif_time(basepath, filename):
    img = Image.open(f'{basepath}/{filename}.jpg')
    info = img.getexif()
    
    # for tag, value in info.items():
    #     decoded_tag = TAGS.get(tag)
    #     print(f'{decoded_tag} : {value}')
    # pass

    try:
        #print(f'{TAGS[306]} : {info[306]}')
        return info[306]
    except:
        #print('No Datetime at EXIF')
        return ''


def update_file_time(basepath:str, filename:str, article_date:str):
    exif_time = get_exif_time(basepath, filename)
    tm = 0
    if exif_time == '':
        # use article_date
        tm = time.mktime(datetime(*([int(x) for x in article_date.split('_')] + [12,0,0])).timetuple())
        pass
    else:        
        tm = time.mktime(datetime(*[int(x) for x in exif_time.replace(' ', ':').split(':')]).timetuple())
    os.utime(f'{basepath}/{filename}.jpg', (tm, tm))

def update_file_time_movie(basepath:str, filename:str, article_date:str):
    tm = time.mktime(datetime(*([int(x) for x in article_date.split('_')] + [12,0,0])).timetuple())
    os.utime(f'{basepath}/{filename}.mp4', (tm, tm))


def write_message(message, basepath, filename):
    with open(f'{basepath}/{filename}.json', "w", encoding='utf8') as file:
        only_msg = dict(message)
        del only_msg['images']
        if 'movie' in only_msg:
            del only_msg['movie']
        #print(only_msg)
        json.dump(only_msg, file, ensure_ascii=False)
        #file.write(only_msg)

def make_filename(type, date, idx):
    #print(f'date[{date}] idx[{idx}]')
    # YYYY_MM_DD_idx.jpg
    return f'{type}_{date}_{idx:03d}'
