import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
import pandas as pd


def crawl_kysing_song_info(song_number):
    url = f"https://kysing.kr/search/?category=1&keyword={song_number}"
    browser_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://kysing.kr/search/",
        "Connection": "keep-alive",
    }

    try:
        response = requests.get(url, headers=browser_headers, timeout=10)
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

        title_el = result_row.select_one(".search_chart_tit .tit")
        singer_el = result_row.select_one(".search_chart_sng")
        composer_el = result_row.select_one(".search_chart_cmp")
        lyricist_el = result_row.select_one(".search_chart_wrt")
        release_date_el = result_row.select_one(".search_chart_rel")
        lyrics_el = result_row.select_one(".LyricsWrap .LyricsCont")

        title = title_el.text.strip() if title_el else "정보 없음"
        singer = singer_el.text.strip() if singer_el else "정보 없음"
        composer = composer_el.text.strip() if composer_el else "정보 없음"
        lyricist = lyricist_el.text.strip() if lyricist_el else "정보 없음"
        release_date = release_date_el.text.strip() if release_date_el else "정보 없음"
        lyrics = lyrics_el.get_text(strip=True) if lyrics_el else "정보 없음"

        return {
            "number": song_number,
            "title": title,
            "singer": singer,
            "composer": composer,
            "lyricist": lyricist,
            "release_date": release_date,
            "lyrics": lyrics,
        }

    except Exception as e:
        return {"number": str(song_number), "error": True, "error_message": str(e)}


if __name__ == "__main__":
    start_number = 99
    end_number = 102

    print(
        f"{start_number}번부터 {end_number}번까지 금영 노래방 곡 정보 크롤링을 시작합니다..."
    )

    pool = Pool(processes=4)
    results = pool.map(crawl_kysing_song_info, range(start_number, end_number + 1))
    pool.close()
    pool.join()

    success_results = []
    failed_results = []

    for result in results:
        if result.get("error", False):
            failed_results.append(
                (result["number"], result.get("error_message", "알 수 없는 오류"))
            )
        else:
            success_results.append(result)

    if failed_results:
        print("\n===== 크롤링 실패한 노래 번호 =====")
        for number, error_message in failed_results:
            print(f"노래번호 {number}: {error_message}")
        print("================================\n")

    df = pd.DataFrame(success_results)
    df = df[
        ["number", "title", "singer", "composer", "lyricist", "release_date", "lyrics"]
    ]

    output_file = "ky_songs.xlsx"
    df.to_excel(output_file, index=False)

    print(
        f"크롤링 완료! {len(success_results)}개의 노래 정보를 '{output_file}' 파일에 저장했습니다."
    )
