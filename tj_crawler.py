import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
import pandas as pd


# TJ 미디어 웹사이트에서 노래 번호로 노래 정보를 크롤링하는 함수
def crawl_song_info_by_num(num):
    req = requests.get(
        "https://www.tjmedia.com/tjsong/song_search_list.asp?strType=16&natType=&strText="
        + str(num)
        + "&strCond=1&strSize05=100"
    )

    # 응답 내용을 UTF-8로 디코딩 (인코딩 오류 시 대체 문자 사용)
    html = req.content.decode("utf-8", "replace")

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, "lxml")

    # CSS 선택자를 사용하여 테이블에서 필요한 정보 추출
    # 노래 번호 정보 추출
    songnumber = soup.select(
        "#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(1) > span"
    )
    # 노래 제목 정보 추출
    songname = soup.select("#BoardType1 > table > tbody > tr:nth-child(2) > td.left")
    # 가수 이름 정보 추출
    singername = soup.select(
        "#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(3)"
    )

    # 태그를 제거하고 텍스트만 추출하여 리스트로 저장
    song_numbers = []
    song_titles = []
    singer_names = []

    for data in songnumber:
        song_numbers.append(data.text)
    for data in songname:
        song_titles.append(data.text)
    for data in singername:
        singer_names.append(data.text)

    # 추출된 모든 데이터를 하나의 리스트로 합침
    # 참고: 현재 코드는 리스트를 단순 연결하여 [노래번호, 노래제목, 가수이름] 형태가 됨
    # 이 방식은 데이터 구조화 측면에서 개선이 필요할 수 있음
    result_data = song_numbers + song_titles + singer_names
    return result_data


# 크롤링 결과를 저장할 리스트 초기화
datasets = []

if __name__ == "__main__":
    # 멀티프로세싱 풀 생성 (CPU 코어 수에 맞게 자동 설정)
    pool = Pool()

    # 1부터 10까지의 노래 번호에 대해 병렬로 크롤링 실행
    # 원래는 1부터 100,000까지 크롤링하도록 설정되어 있었음
    datasets = pool.map(crawl_song_info_by_num, range(1, 11))
    # datasets = (pool.map(crawl_song_info_by_num, range(1, 100000)))

# 크롤링 결과를 pandas DataFrame으로 변환
df = pd.DataFrame.from_records(datasets)

# DataFrame을 Excel 파일로 저장
df.to_excel("tj_songs.xlsx")
