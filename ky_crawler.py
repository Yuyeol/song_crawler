import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
KY_TABLE_NAME = os.getenv("SUPABASE_KY_TABLE")

# Supabase 클라이언트 초기화
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

START_NUMBER = 129
END_NUMBER = 136


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
            "number": str(song_number),
            "title": title,
            "singer": singer,
            "composer": composer,
            "lyricist": lyricist,
            "release_date": release_date,
            "lyrics": lyrics,
        }

    except Exception as e:
        return {"number": str(song_number), "error": True, "error_message": str(e)}


def upload_to_supabase(data, batch_size=100):
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase 연결 정보가 없습니다. .env 파일을 확인하세요.")
        return False

    if not KY_TABLE_NAME:
        print(
            "테이블 이름이 설정되지 않았습니다. .env 파일의 SUPABASE_KY_TABLE을 확인하세요."
        )
        return False

    success_count = 0
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        try:
            # upsert 메서드 사용, number 필드로 충돌 해결
            response = (
                supabase.table(KY_TABLE_NAME)
                .upsert(batch, on_conflict="number")  # number 필드를 기준으로 충돌 감지
                .execute()
            )

            # 응답 확인
            if hasattr(response, "error") and response.error:
                print(f"업로드 실패 (배치 {i//batch_size + 1}): {response.error}")
                return False

            success_count += len(batch)
            print(f"업로드 진행 중: {success_count}/{len(data)} 완료")

            # 요청 간 짧은 대기 시간 추가
            time.sleep(0.5)

        except Exception as e:
            print(f"업로드 중 오류 발생: {str(e)}")
            return False

    return True


def save_to_excel(data, filename="ky_songs.xlsx"):
    df = pd.DataFrame(data)
    columns = [
        "number",
        "title",
        "singer",
        "composer",
        "lyricist",
        "release_date",
        "lyrics",
    ]
    df = df[columns]
    df.to_excel(filename, index=False)
    print(f"{len(data)}개의 노래 정보를 '{filename}' 파일에 저장했습니다.")
    return df


if __name__ == "__main__":
    print(
        f"{START_NUMBER}번부터 {END_NUMBER}번까지 금영 노래방 곡 정보 크롤링을 시작합니다..."
    )

    start_time = time.time()
    pool = Pool(processes=4)
    results = pool.map(crawl_kysing_song_info, range(START_NUMBER, END_NUMBER + 1))
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

    # 실패한 결과 출력
    if failed_results:
        print("\n===== 크롤링 실패한 노래 번호 =====")
        for number, error_message in failed_results:
            print(f"노래번호 {number}: {error_message}")
        print("================================\n")

    # 성공한 결과가 없으면 종료
    if not success_results:
        print("크롤링에 성공한 노래 정보가 없습니다.")
        exit(1)

    # 엑셀 파일로 저장
    output_file = "ky_songs.xlsx"
    save_to_excel(success_results, output_file)

    # 경과 시간 계산
    elapsed_time = time.time() - start_time
    print(f"크롤링 완료! 소요 시간: {elapsed_time:.2f}초")

    # Supabase에 업로드
    print("\nSupabase에 데이터 업로드 중...")

    # 필드 확인 및 필터링 (error 필드 제거)
    upload_data = []
    for result in success_results:
        # 필요한 필드만 추출
        filtered_result = {
            "number": result["number"],
            "title": result["title"],
            "singer": result["singer"],
            "composer": result["composer"],
            "lyricist": result["lyricist"],
            "release_date": result["release_date"],
            "lyrics": result["lyrics"],
        }
        upload_data.append(filtered_result)

    upload_success = upload_to_supabase(upload_data)

    if upload_success:
        print(
            f"Supabase '{KY_TABLE_NAME}' 테이블에 {len(upload_data)}개의 노래 정보 업로드 완료!"
        )
    else:
        print("Supabase 업로드에 실패했습니다.")
