import requests
from bs4 import BeautifulSoup

def link_to_text(url):

    # 페이지 HTML 가져오기
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # #dic_area 내부의 텍스트 추출, img_desc 클래스 내용 제외
    dic_area = soup.find(id='dic_area')
    if dic_area:
        # img_desc 클래스의 요소들을 제거
        for img_desc in dic_area.find_all(class_='img_desc'):
            img_desc.extract()

        # img_desc를 제외한 나머지 텍스트 가져오기
        return dic_area.get_text()
    else:
        return "해당 기사를 찾을 수 없습니다."
