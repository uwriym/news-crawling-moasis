# 필요한 패키지 불러오기
import requests # URL 요청
from bs4 import BeautifulSoup # 웹사이트 크롤링
from collections import Counter # 단어 빈도수 정리

keyword = '넷플릭스'#input('검색어를 입력하세요: ')

search_url = f'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={keyword}'

# link 얻기
def get_link():
    link_list = [] # 최종 링크
    bad_link_list = [] # 필요없는 링크 포함

    url = requests.get(search_url)
    webpage = BeautifulSoup(url.text, 'html.parser')
    element_list = webpage.select('a.info') # html 요소 중 <a class='info'></a> 선택

    for element in element_list:
        news_link = element["href"] # a 태그의 href 요소(뉴스 링크) 선택
        bad_link_list.append(news_link)

    for link in bad_link_list:
        if 'naver' in link: # URL에 'naver'가 들어가 있는지 확인
            link_list.append(link)

    return link_list # 뉴스 URL 리스트 반환


content_text_list = []  # 텍스트만 추출한 content 리스트

# content 얻기
def get_content(url):

    news_url = requests.get(url, headers={'User-Agent': 'Chrome'}) # 네이버 뉴스 페이지가 요구하는 브라우저 정보 작성
    webpage = BeautifulSoup(news_url.text, 'html.parser')
    content_list = webpage.select('div._article_content')

    for content in content_list:
        content_text_list.append(content.text) # content의 텍스트만 추출하여 content_text_list에 저장

# 뉴스 URL 마다 get_content 함수 실행
for url in get_link():
    get_content(url)

