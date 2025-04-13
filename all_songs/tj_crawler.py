import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from all_songs.utils import run_crawler, add_chosung_fields

# 환경 변수 로드
load_dotenv()

# 크롤링 설정
START_NUMBER = 1
END_NUMBER = 13
PROCESSES = 4  # 멀티프로세싱 프로세스 수
TJ_TABLE_NAME = "tj_songs"
OUTPUT_FILE = "tj_songs.xlsx"
TIMEOUT = 10  # 요청 타임아웃(초)

# 필수 데이터 필드
DATA_FIELDS = [
    "number",
    "title",
    "title_chosung",
    "singer",
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
    url = f"https://www.tjmedia.com/tjsong/song_search_list.asp?strType=16&natType=&strText={song_number}&strCond=1&strSize05=100"

    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        html = response.content.decode("utf-8", "replace")
        soup = BeautifulSoup(html, "lxml")

        song_number_el = soup.select(
            "#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(1)"
        )

        song_title_el = soup.select(
            "#BoardType1 > table > tbody > tr:nth-child(2) > td.left"
        )

        singer_name_el = soup.select(
            "#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(3)"
        )

        if not song_number_el or not song_title_el or not singer_name_el:
            return {
                "number": str(song_number),
                "error": True,
                "error_message": "검색 결과 없음",
            }

        number = song_number_el[0].text.strip() if song_number_el else "정보 없음"
        title = song_title_el[0].text.strip() if song_title_el else "정보 없음"
        singer = singer_name_el[0].text.strip() if singer_name_el else "정보 없음"
        created_at = datetime.date.today().isoformat()

        data = {
            "number": number,
            "title": title,
            "singer": singer,
            "created_at": created_at,
        }

        # 초성 변환 적용
        data = add_chosung_fields(data)

        return data

    except Exception as e:
        return {"number": str(song_number), "error": True, "error_message": str(e)}


def crawl_and_save():
    return run_crawler(
        crawler_func=crawl_song_info,
        start_number=START_NUMBER,
        end_number=END_NUMBER,
        processes=PROCESSES,
        output_file=OUTPUT_FILE,
        table_name=TJ_TABLE_NAME,
        data_fields=DATA_FIELDS,
        service_name="태진 노래방",
    )


if __name__ == "__main__":
    crawl_and_save()
