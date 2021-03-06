# kidsnote downloader cli
## 키즈노트의 사진을 다운
- 모든 사진을 다운로드 (알림장, 앨범)
- 파일 명을 시간 순으로
- 파일 접근 시간을 Exif 또는 알림장 작성일 로 설정
  - 이유는 Google Photo 에 업로드 용
## 키즈노트의 글들도 다운
- JSON 형태로 다운로드 
```
{
    "main": {
        "author": "2018-새싹반 교사",
        "date": "2018년 9월 18일 화요일",
        "content": "내용 내용 내용"
    },
    "comments": [
        {
            "author": "아기 엄마",
            "date": "9.19 오전 8:54",
            "content": "내용 내용 내용"
        },
        {
            "author": "2018-새싹반 교사",
            "date": "9.19 오전 10:06",
            "content": "내용 내용 내용"
        },
        {
            "author": "아기 아빠",
            "date": "9.19 오전 10:08",
            "content": "내용 내용 내용"
        }
    ]
}
```
## 실행 할 때마다 증분 형식으로 받음
- 최초는 모든 아이템 다운로드
- 이후는 다운로드 한 아이템은 제외 (kidsnote.ini 파일 유지 되어야 함)

## 사용법
- 리눅스 환경 만 지원(ubuntu 18.04 이후 추천)
- kidsnote.ini 를 설정
  - id : 계정 id
  - pw : 계정 암호
  - nick : 아무거나 상관없음
  - downpath : 실제 다운로드 될 경로, 절대 경로 추천, 마지막 슬래시 제외
  - lastarticle, lastalbum : 마지막 다운로드한 글의 id (모두 받으려면 0으로 설정)
  - 아래 명령어로 실행
```
pip install -r requirements.txt
python3 kndn.py
```

- 코드를 깔끔하게 만들고 싶었는데...그냥 대충 잘 동작하길래 멈춥니다. 
- 아기가 둘이신 분들은 어떻게 될지 모르겠네요. 제가 애가 하나 뿐이라...
- 누군가에겐 도움이 되길