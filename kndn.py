#-*- coding: utf-8 -*-

import configparser
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup as bs
from datetime import datetime


config = configparser.ConfigParser()
config.read('kidsnote.ini')

s = requests.Session()
s.mount('https://', HTTPAdapter())

csrfmiddlewaretoken = ""
request_headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',
                        'Referer': 'https://www.kidsnote.com/login/',
                        'Origin': 'https://www.kidsnote.com',
                        'Host': 'www.kidsnote.com',
                        'Accept-Language': 'ko,en;q=0.9,en-US;q=0.8',
                        'Upgrade-Insecure-Requests': '1'}
max_page = 0

def get_csrfmiddelwaretoken(res):
    soup = bs(res.text, features='html.parser')
    elem = soup.find('input', attrs={'name':'csrfmiddlewaretoken'})

    global csrfmiddlewaretoken
    csrfmiddlewaretoken = elem.attrs['value']

def open_first_page():
    res = s.get("https://www.kidsnote.com/login/", headers=request_headers)
    get_csrfmiddelwaretoken(res)

def login():
    username = config['KIDSNOTE']['Id']
    password = config['KIDSNOTE']['Pw']
    #print(f'username[{username}], password[{password}]')
    form_datas = {'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'username': username,
                'password': password,
                'next': ''}
    
    
    res = s.post('https://www.kidsnote.com/login/',
    headers=request_headers,
    data=form_datas)

    get_csrfmiddelwaretoken(res)

def set_nick_name():
    nickname = config['KIDSNOTE']['Nick']
    form_datas = {'csrfmiddlewaretoken': csrfmiddlewaretoken,
                'nickname': nickname,
                'next': '/home/'}    
    
    res = s.post('https://www.kidsnote.com/accounts/role/name/',
    headers=request_headers,
    data=form_datas)

    get_csrfmiddelwaretoken(res)


def open_box_of_remember():
    form_datas = {'csrfmiddlewaretoken': csrfmiddlewaretoken}    
    res = s.post('https://www.kidsnote.com/accounts/parents/children/activate/1802891/feed/',
    headers=request_headers,
    data=form_datas)

def open_reports():
    res = s.get("https://www.kidsnote.com/reports/", headers=request_headers)
    get_csrfmiddelwaretoken(res)

    soup = bs(res.text, features='html.parser')
    pagination = soup.find('ul', attrs={'class':'pagination-sm'})
    
    global max_page
    max_page = int(pagination.find_all('li')[-2].a.text)
    #print(f'max_page : {max_page}')

def open_page_and_get_article_list(page):
    res = s.get(f'https://www.kidsnote.com/reports/?page={page}', headers=request_headers)
    
    soup = bs(res.text, features='html.parser')
    _list = soup.find('div', attrs={'class':'report-list-wrapper'})
    article_list = [ x.attrs['href'] for x in _list.find_all('a')]
    print(f'Page [{page}] has {len(article_list)} articles.')
    return article_list

def download_img(url, filename):
    with open(f'./images/{filename}.jpg', "wb") as file:        
        res = requests.get(url)
        file.write(res.content)

def open_article_and_get_data(article):
    print(article)
    res = s.get(f'https://www.kidsnote.com{article}', headers=request_headers)
    
    soup = bs(res.text, features='html.parser')
    _author_info = soup.find('div', attrs={'class':'author-info'})
    _main_msg = soup.find('div', attrs={'class':'content-text'})
    _img_container = []
    try:
        _img_container = soup.find('div', id='img-grid-container').find_all('a')
    except:
        print("No Image")

    _comment_list = soup.find('ul', attrs={'class':'comment-list'}).find_all('li')

    _author_name = _author_info.find_all('span')[0].text
    _written_date = _author_info.find_all('span')[1].text

    info = {}    
    info['main'] = {}
    info['main']['author'] = _author_name
    info['main']['date'] = _written_date
    inner_html = _main_msg.encode_contents()
    inner_html = inner_html.replace(b'<br/>', b'\n')
    info['main']['content'] = inner_html.decode('utf8')[2:].strip()
    info['comments'] = []    
    
    for comment in _comment_list:
        _comment_name = comment.find('span', attrs={'class':'author-name'}).text
        _comment_date = comment.find('span', attrs={'class':'date-written'}).text
        _comment_msg = comment.find('p').text
        info['comments'].append({'author':_comment_name, 'date':_comment_date, 'content':_comment_msg})

    info['images'] = []

    for img in _img_container:
        info['images'].append(img.attrs['data-download'])

    #print(info)
    #print(len(info['images']))

    return info
    
def parse_datetime(report_date):
    short_date = report_date[:report_date.rfind(' ')]
    time_t = datetime.strptime(short_date, '%Y년 %m월 %d일')
    str_time = time_t.strftime('%Y_%m_%d')

    #print(str_time) # 2021_08_24
    return str_time

from PIL import Image
from PIL.ExifTags import TAGS
def get_exif_time(filename):
    img = Image.open(f'./images/{filename}.jpg')
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

import time, os
def update_file_time(filename:str, article_date:str):
    exif_time = get_exif_time(filename)
    tm = 0
    if exif_time == '':
        # use article_date
        tm = time.mktime(datetime(*([int(x) for x in article_date.split('_')] + [12,0,0])).timetuple())
        pass
    else:        
        tm = time.mktime(datetime(*[int(x) for x in exif_time.replace(' ', ':').split(':')]).timetuple())
    os.utime(f'./images/{filename}.jpg', (tm, tm))

import json
def write_message(message, filename):
    with open(f'./images/{filename}.json', "w", encoding='utf8') as file:
        only_msg = dict(message)
        del only_msg['images']
        #print(only_msg)
        json.dump(only_msg, file, ensure_ascii=False)
        #file.write(only_msg)

def make_filename(date, idx):
    #print(f'date[{date}] idx[{idx}]')
    # YYYY_MM_DD_idx.jpg
    return f'{date}_{idx:03d}'

def download_all():
    # 각 페이지 마다 돌면서 
    total_page = 0
    total_article = 0
    total_image = 0
    for page in range(1, max_page+1):
        total_page += 1
        article_list = open_page_and_get_article_list(page)
        # 각 글마다 들어가서
        previous_article_date = ''
        previous_idx_delta = 0
        for article in article_list:
            total_article += 1
            # 각 이미지를 다운로드
            info = open_article_and_get_data(article)
            article_date = parse_datetime(info['main']['date'])
            # 중복 해결
            idx_delta = 0
            if previous_article_date == article_date:
                previous_idx_delta += 100
                idx_delta = previous_idx_delta
            else:
                previous_idx_delta = 0
            previous_article_date = article_date

            for idx in range(len(info['images'])):
                total_image += 1
                # 날짜 변경
                filename = make_filename(article_date, idx+idx_delta)
                download_img(info['images'][idx], filename)
                update_file_time(filename, article_date)
                print(f'PAGE[{total_page}] ART[{total_article}] IMG[{total_image}] : {article_date}')
            filename = make_filename(article_date, idx_delta)
            write_message(info, filename) 
    
    
    
    
open_first_page()
login()
set_nick_name()
open_box_of_remember()
open_reports()
download_all()
# article_list = open_page_and_get_article_list(1)
# info = open_article_and_get_data(article_list[1])
# article_date = parse_datetime(info['main']['date']) # 2021_08_24
# filename = make_filename(article_date, 1)
# download_img(info['images'][0], filename)
# update_file_time(filename, article_date)
# write_message(info, filename) 