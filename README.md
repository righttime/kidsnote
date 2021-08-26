# kidsnote downloader cli
## 키즈노트의 사진을 다운받아 보자
- 사진의 Created time update with exif 인데... 이건 윈도우에서만 가능? 리눅스만 가지고 하면 될듯?
- 어떤 시간을 기준으로 되는걸까?
- 요 파일들을... 다 올리면 되는건데 ...
- NAS 로? MOBILE 로?
## 선생님, 부모님의 이야기도 보존해 보자
- 일단 JSON 정도라도.

## REQUEST

### Header 
```
POST /login/ HTTP/1.1
Host: www.kidsnote.com
Connection: keep-alive
Content-Length: 127
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Microsoft Edge";v="92"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
Origin: https://www.kidsnote.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://www.kidsnote.com/login/
Accept-Encoding: gzip, deflate, br
Accept-Language: ko
Cookie: csrftoken=V7YSJydSaiwyCEf6jU2gsnDlUwPi89oHQ0d2qRlyd3r4Jpn7KC78aIt6Oxgxuhwe; sessionid=ukmguzgtuup28gzotuzefdwzw3t9egx3; _ga=GA1.2.447816361.1629811691; _gid=GA1.2.1163741950.1629811691; _gat=1
```
### Formdata
- csrfmiddlewaretoken : qg4u6lWF2kanlHhWrX5ht1t9jp2UnPhtNkjWzmLrFvfniJ0FOpZzZ67NPq5vMWvq
- username
- password
- next