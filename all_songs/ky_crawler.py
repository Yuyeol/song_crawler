import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from all_songs.utils import run_crawler, process_title_singer_for_supabase

# 환경 변수 로드
load_dotenv()

# 크롤링 설정
START_NUMBER = 100
END_NUMBER = 110
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
    "lyrics",
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

        selectors = {
            "title": ".search_chart_tit .tit",
            "singer": ".search_chart_sng",
            "composer": ".search_chart_cmp",
            "lyricist": ".search_chart_wrt",
            "release_date": ".search_chart_rel",
            "lyrics": ".LyricsWrap .LyricsCont",
        }

        data = {"number": str(song_number)}
        for key, selector in selectors.items():
            element = result_row.select_one(selector)
            data[key] = element.text.strip() if element else "정보 없음"

        lyrics_el = result_row.select_one(selectors["lyrics"])
        data["lyrics"] = lyrics_el.get_text(strip=True) if lyrics_el else "정보 없음"
        data["created_at"] = datetime.date.today().isoformat()

        # 다국어 변환 적용
        processed_data = process_title_singer_for_supabase(
            data["title"], data["singer"]
        )

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
    return run_crawler(
        crawler_func=crawl_song_info,
        start_number=START_NUMBER,
        end_number=END_NUMBER,
        processes=PROCESSES,
        output_file=OUTPUT_FILE,
        table_name=KY_TABLE_NAME,
        data_fields=DATA_FIELDS,
        service_name="금영 노래방",
    )


if __name__ == "__main__":
    crawl_and_save()
