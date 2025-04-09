import requests
import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from popular_songs.utils import run_chart_crawler

# 환경 변수 로드
load_dotenv()

# 크롤링 설정
TJ_POPULAR_TABLE_NAME = "tj_popular_songs"
OUTPUT_FILE = "tj_popular_songs.xlsx"
TIMEOUT = 10  # 요청 타임아웃(초)

# 필수 데이터 필드
DATA_FIELDS = [
    "rank",
    "number",
    "title",
    "singer",
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


def crawl_popular_chart():
    url = "https://www.tjmedia.com/tjsong/song_monthPopular.asp"
    all_results = []

    try:
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        # HTML 파싱 (인코딩 처리)
        html = response.content.decode("utf-8", "replace")
        soup = BeautifulSoup(html, "lxml")

        # 테이블에서 모든 tr 요소 가져오기 (첫 번째는 헤더이므로 제외)
        rows = soup.select("table.board_type1 tr")[1:]

        for row in rows:
            try:
                columns = row.select("td")

                if len(columns) < 4:
                    continue

                rank = columns[0].text.strip()
                number = columns[1].text.strip()
                title = columns[2].text.strip()
                singer = columns[3].text.strip()
                created_at = datetime.date.today().isoformat()

                all_results.append(
                    {
                        "rank": int(rank),
                        "number": number,
                        "title": title,
                        "singer": singer,
                        "created_at": created_at,
                    }
                )

            except Exception as e:
                print(f"항목 파싱 중 오류 발생: {str(e)}")
                continue

        print(f"인기 차트 {len(all_results)}개 항목 파싱 완료")
        return all_results

    except Exception as e:
        print(f"인기 차트 크롤링 중 오류 발생: {str(e)}")
        return []


def crawl_and_save():
    return run_chart_crawler(
        crawler_func=crawl_popular_chart,
        output_file=OUTPUT_FILE,
        table_name=TJ_POPULAR_TABLE_NAME,
        data_fields=DATA_FIELDS,
        service_name="태진 노래방 인기 차트",
    )


if __name__ == "__main__":
    crawl_and_save()
