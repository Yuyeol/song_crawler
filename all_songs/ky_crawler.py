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
START_NUMBER = 121
END_NUMBER = 130
PROCESSES = 4  # 멀티프로세싱 프로세스 수
KY_TABLE_NAME = "ky_songs"
OUTPUT_FILE = "ky_songs.xlsx"
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
    "composer",
    "lyricist",
    "release_date",
    "created_at",
]

# 브라우저 헤더
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://kysing.kr/search/",
    "Connection": "keep-alive",
}


def crawl_song_info(song_number):
    url = f"https://kysing.kr/search/?category=1&keyword={song_number}"

    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        search_results = soup.select(".search_chart_list")

        if len(search_results) < 2:
            return {
                "number": str(song_number),
                "error": True,
                "error_message": "검색 결과 없음",
            }

        result_row = search_results[1]  # [0]은 헤더이므로 다음 row 선택

        # 직접 각 요소를 선택
        title_el = result_row.select_one(".search_chart_tit .tit")
        singer_el = result_row.select_one(".search_chart_sng")
        composer_el = result_row.select_one(".search_chart_cmp")
        lyricist_el = result_row.select_one(".search_chart_wrt")
        release_date_el = result_row.select_one(".search_chart_rel")

        # 요소가 없으면 "정보 없음" 처리
        title = title_el.text.strip() if title_el else "정보 없음"
        singer = singer_el.text.strip() if singer_el else "정보 없음"
        composer = composer_el.text.strip() if composer_el else "정보 없음"
        lyricist = lyricist_el.text.strip() if lyricist_el else "정보 없음"
        release_date = release_date_el.text.strip() if release_date_el else "정보 없음"

        # 기본 데이터
        data = {
            "number": str(song_number),
            "title": title,
            "singer": singer,
            "composer": composer,
            "lyricist": lyricist,
            "release_date": release_date,
            "created_at": datetime.date.today().isoformat(),
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
    numbers_to_crawl = get_numbers_to_crawl(KY_TABLE_NAME, START_NUMBER, END_NUMBER)

    if numbers_to_crawl is None:
        return False

    if len(numbers_to_crawl) == 0:
        return True

    # 크롤링 실행
    return run_crawler(
        crawler_func=crawl_song_info,
        processes=PROCESSES,
        output_file=OUTPUT_FILE,
        table_name=KY_TABLE_NAME,
        data_fields=DATA_FIELDS,
        service_name="금영 노래방",
        custom_numbers=numbers_to_crawl,
    )


if __name__ == "__main__":
    crawl_and_save()
