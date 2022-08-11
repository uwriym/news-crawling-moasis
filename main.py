# 필요한 패키지 불러오기
import requests  # URL 요청
from bs4 import BeautifulSoup  # 웹사이트 크롤링
from collections import Counter  # 단어 빈도수 정리

keyword = input('검색어를 입력하세요: ')
last_page = int(input('몇 페이지까지 검색할까요? '))

# keyword에 띄어쓰기가 있는 경우 띄어쓰기를 +로 대체하여 유효한 URL로 변경
if ' ' in keyword:
    keyword = keyword.replace(' ','+')

search_url = f'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={keyword}'

news_count = [] # 검색된 기사 개수 확인 용 변수 정의

# link 얻기
def get_link():

    link_list = []  # 최종 링크 리스트
    bad_link_list = []  # 필요없는 링크 포함

    page_count = 1
    for page in range(1, last_page * 10, 10):  # 1페이지부터 last_page까지 반복
        print(f"Scrapping page {page_count}")
        page_count += 1

        url = requests.get(f"{search_url}&start={page}") # start=1 -> 1페이지, start=11 -> 2페이지
        webpage = BeautifulSoup(url.text, 'html.parser')
        element_list = webpage.select('a.info')  # html 요소 중 <a class='info'></a> 선택

        for element in element_list:
            news_link = element["href"]  # a 태그의 href 요소(뉴스 링크) 선택
            bad_link_list.append(news_link)

        for link in bad_link_list:
            if 'naver' in link:  # URL에 'naver'가 들어가 있는지 확인
                link_list.append(link)

    global news_count  # news_count 전역 변수 설정
    news_count = link_list

    return link_list  # 뉴스 URL 리스트 반환


content_text_list = []  # 텍스트만 추출한 content 리스트

# content 얻기
def get_content(url):

    news_url = requests.get(url, headers={'User-Agent': 'Chrome'})  # 네이버 뉴스 페이지가 요구하는 브라우저 정보 작성
    webpage = BeautifulSoup(news_url.text, 'html.parser')
    content_list = webpage.select('div._article_content')

    for content in content_list:
        content_text_list.append(content.text)  # content의 텍스트만 추출하여 content_text_list에 저장

# 뉴스 URL 마다 get_content 함수 실행
for url in get_link():
    get_content(url)


# 불용어 제거 5단계

really_bad_word_list = []  # 공백을 기준으로 구분된 단어 리스트
bad_word_list = []  # 마침표를 기준으로 구분된 단어 리스트
word_list = []  # 불용어가 제거된 최종 단어 리스트

# 1단계
for word in content_text_list:
    really_bad_word_list.append(word.split())

# 2단계
for list in really_bad_word_list:
    for word in list:
        bad_word_list.append(word.split('.'))

# 3단계 - 문장부호 제거 및 두 글자 이상 불용어 제거
for word in bad_word_list:  # 제거가 필요한 두 글자 이상 불용어 제거
    word_list.append(word[0].replace('\'','').replace('\"','').replace('(','').replace(')','')\
                     .replace('<','').replace('>','').replace(',','').replace('‘','')\
                     .replace('’', '').replace('[','').replace(']','').replace('=','')\
                     .replace('했다','').replace('이하','').replace('해나가고','').replace('입니다','')\
                     .replace('있다','').replace('대비','').replace('전년','').replace('동기','')\
                     .replace('지난','').replace('위해','').replace('통해','').replace('기자','')\
                     .replace('것으','').replace('밝혔다','').replace('이들','').replace('특히','')\
                     .replace('경우','').replace('가장','').replace('매우','').replace('한다','')\
                     .replace('모든','').replace('또한','').replace('따라','').replace('가장','')\
                     .replace('이다','').replace('최근','').replace('보다','').replace('가진','')\
                     .replace('다양한','').replace('때문','').replace('그런데','').replace('으로','')\
                     .replace('합니다','').replace('아니라','').replace('다른','').replace('정도','')\
                     .replace('하지만','').replace('것이다','').replace('따르면','').replace('최대','')\
                     .replace('있어','').replace('있고','').replace('어떤','').replace('하고','')\
                     .replace('것”이라고',''))


# 4단계 - 단어 끝 조사 제거
word_list_count = 0
for word in word_list:
    if len(word) != 0:
        if word[-1] in '을를이가은는수의로있에것와한':  # 제거가 필요한 한 글자 조사 추가
            word_list[word_list_count] = word[:-1]
            print(f"{word[-1]} replaced to {word[:-1]} at {word_list_count}")
    word_list_count += 1

# 5단계 - 한 글자 이하 단어 제거
for word in word_list:
    if len(word) < 2:
        word_list.remove(word)
    if (word == '있') or (word == '이'):
        word_list.remove(word)  # 잘 안 없어지는 한 글자 제거
# 단어 빈도 수 측정
word_count = Counter(word_list)


# 파일 생성
words_file = open(f'/Users/eoorim/Desktop/Coding/Python/bigdata_seminar/{keyword} Words.txt', 'w')
for word in word_list:
    words_file.write(word)
    words_file.write(', ')

count_file = open(f'/Users/eoorim/Desktop/Coding/Python/bigdata_seminar/{keyword} Count.txt', 'w')
count_file.write(str(word_count))

print(f"\n검색된 기사: {len(news_count)}개")
print(f"검색된 단어: {len(word_list)}개")


