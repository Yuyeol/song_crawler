import requests
import datetime
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from all_songs.utils import (
    run_crawler,
    process_title_singer_for_supabase,
    get_numbers_to_crawl,
)

# 환경 변수 로드
load_dotenv()

# 크롤링 설정
START_NUMBER = 1
END_NUMBER = 100000
PROCESSES = 4  # 멀티프로세싱 프로세스 수
TJ_TABLE_NAME = "tj_songs"
OUTPUT_FILE = "tj_songs.xlsx"
TIMEOUT = 10  # 요청 타임아웃(초)

# 필수 데이터 필드
DATA_FIELDS = [
    "number",
    "title",
    "title_pron",
    "title_chosung",
    "singer",
    "singer_pron",
    "singer_chosung",
    "created_at",
]

# 브라우저 헤더
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.tjmedia.com/",
    "Connection": "keep-alive",
}


def crawl_song_info(song_number):
    url = f"https://www.tjmedia.com/song/accompaniment_search?nationType=&strType=16&searchTxt={song_number}"

    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        html = response.content.decode("utf-8", "replace")
        soup = BeautifulSoup(html, "lxml")

        # 새로운 HTML 구조에 맞춰 셀렉터 수정
        # 첫 번째 li를 제외한 나머지 li 선택 (첫 번째는 헤더)
        song_list = soup.select("ul.chart-list-area > li:not(:first-child)")

        if not song_list:
            return {
                "number": str(song_number),
                "error": True,
                "error_message": "검색 결과 없음",
            }

        # 첫 번째 결과를 가져옴
        first_song = song_list[0]

        # 노래 번호
        song_number_el = first_song.select_one(".grid-item .num2 .highlight")

        # 노래 제목
        song_title_el = first_song.select_one(
            ".grid-item.title3 .flex-box p:last-child span"
        )

        # 가수 이름
        singer_name_el = first_song.select_one(".grid-item.title4.singer p span")

        if not song_number_el or not song_title_el or not singer_name_el:
            return {
                "number": str(song_number),
                "error": True,
                "error_message": "검색 결과 요소 찾기 실패",
            }

        number = song_number_el.text.strip() if song_number_el else "정보 없음"
        title = song_title_el.text.strip() if song_title_el else "정보 없음"
        singer = singer_name_el.text.strip() if singer_name_el else "정보 없음"
        created_at = datetime.date.today().isoformat()

        # 기본 데이터
        data = {
            "number": number,
            "title": title,
            "singer": singer,
            "created_at": created_at,
        }

        # 다국어 변환 적용
        processed_data = process_title_singer_for_supabase(title, singer)

        # 결과 데이터 병합
        data.update(
            {
                "title_pron": processed_data["title_pron"],
                "title_chosung": processed_data["title_chosung"],
                "singer_pron": processed_data["singer_pron"],
                "singer_chosung": processed_data["singer_chosung"],
            }
        )

        return data

    except Exception as e:
        return {"number": str(song_number), "error": True, "error_message": str(e)}


def crawl_and_save():
    # 크롤링할 번호 목록 가져오기
    numbers_to_crawl = get_numbers_to_crawl(TJ_TABLE_NAME, START_NUMBER, END_NUMBER)

    if numbers_to_crawl is None:
        return False

    if len(numbers_to_crawl) == 0:
        return True

    # 크롤링 실행
    return run_crawler(
        crawler_func=crawl_song_info,
        processes=PROCESSES,
        output_file=OUTPUT_FILE,
        table_name=TJ_TABLE_NAME,
        data_fields=DATA_FIELDS,
        service_name="태진 노래방",
        custom_numbers=numbers_to_crawl,
    )


if __name__ == "__main__":
    crawl_and_save()
