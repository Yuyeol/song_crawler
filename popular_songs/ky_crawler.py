import time
import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from utils import (
    save_to_excel,
    upload_to_supabase,
    filter_data_fields,
    calculate_elapsed_time,
)

# 환경 변수 로드
load_dotenv()

# 크롤링 설정
KY_POPULAR_TABLE_NAME = "ky_popular_songs"
OUTPUT_FILE = "ky_popular_songs.xlsx"
TIMEOUT = 10  # 요청 타임아웃(초)

# 필수 데이터 필드
DATA_FIELDS = [
    "rank",
    "number",
    "title",
    "singer",
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
    "Referer": "https://kysing.kr/",
    "Connection": "keep-alive",
}


def crawl_page(range_num, start_rank):
    url = f"https://kysing.kr/popular/?period=m&range={range_num}"
    page_results = []

    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        chart_items = soup.select(".popular_chart_list")

        # 첫 번째 행은 헤더이므로 건너뛰기, 모든 항목 처리
        for i, item in enumerate(chart_items[1:], 1):
            try:
                number_el = item.select_one(".popular_chart_num")
                title_el = item.select_one(".popular_chart_tit .tit")
                singer_el = item.select_one(".popular_chart_sng")
                composer_el = item.select_one(".popular_chart_cmp")
                lyricist_el = item.select_one(".popular_chart_wrt")
                release_date_el = item.select_one(".popular_chart_rel")

                rank = start_rank + i - 1
                number = number_el.text.strip() if number_el else None
                title = title_el.text.strip() if title_el else None
                singer = singer_el.text.strip() if singer_el else None
                composer = composer_el.text.strip() if composer_el else None
                lyricist = lyricist_el.text.strip() if lyricist_el else None
                release_date = release_date_el.text.strip() if release_date_el else None
                created_at = datetime.date.today().isoformat()

                page_results.append(
                    {
                        "rank": rank,
                        "number": number,
                        "title": title,
                        "singer": singer,
                        "composer": composer,
                        "lyricist": lyricist,
                        "release_date": release_date,
                        "created_at": created_at,
                    }
                )

            except Exception as e:
                print(f"항목 {rank} 파싱 중 오류 발생: {str(e)}")
                continue

        return page_results

    except Exception as e:
        print(f"인기 차트 페이지 {range_num} 크롤링 중 오류 발생: {str(e)}")
        return []


def crawl_popular_chart():
    all_results = []

    # 1페이지 크롤링
    print("인기 차트 첫 번째 페이지 크롤링 중...")
    page1_results = crawl_page(1, 1)
    all_results.extend(page1_results)

    # 2페이지 크롤링
    if len(page1_results) > 0:
        print("인기 차트 두 번째 페이지 크롤링 중...")
        page2_results = crawl_page(2, 51)  # 두 번째 페이지는 51위부터 시작
        all_results.extend(page2_results)

    return all_results


def crawl_and_save():
    print("금영 노래방 인기 차트 크롤링을 시작합니다...")

    start_time = time.time()
    chart_results = crawl_popular_chart()

    if not chart_results:
        print("크롤링에 성공한 인기 차트 정보가 없습니다.")
        return False

    save_to_excel(chart_results, OUTPUT_FILE, DATA_FIELDS)

    elapsed_time = calculate_elapsed_time(start_time)
    print(f"크롤링 완료! 총 {len(chart_results)}개 곡, 소요 시간: {elapsed_time:.2f}초")

    print("\nSupabase에 데이터 업로드 중...")
    upload_data = filter_data_fields(chart_results, DATA_FIELDS)

    # 인기차트는 테이블을 비우고 새로 데이터를 삽입
    upload_success = upload_to_supabase(
        upload_data, KY_POPULAR_TABLE_NAME, update_mode="truncate"
    )

    if upload_success:
        print(
            f"Supabase '{KY_POPULAR_TABLE_NAME}' 테이블에 {len(upload_data)}개의 인기 차트 정보 업로드 완료!"
        )
        return True
    else:
        print("Supabase 업로드에 실패했습니다.")
        return False


if __name__ == "__main__":
    crawl_and_save()
