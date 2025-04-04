import os
import time
import requests
from multiprocessing import Pool
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
START_NUMBER = int(os.getenv("TJ_START_NUMBER", 1))
END_NUMBER = int(os.getenv("TJ_END_NUMBER", 10))
PROCESSES = 4  # 멀티프로세싱 프로세스 수
TJ_TABLE_NAME = os.getenv("SUPABASE_TJ_TABLE", "taejin_songs")
OUTPUT_FILE = "tj_songs.xlsx"
TIMEOUT = 10  # 요청 타임아웃(초)

# 필수 데이터 필드
DATA_FIELDS = ["number", "title", "singer"]

# 브라우저 헤더
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.tjmedia.com/",
    "Connection": "keep-alive",
}


def crawl_song_info(song_number):
    """
    태진 노래방 사이트에서 노래 정보를 크롤링합니다.

    Args:
        song_number (int): 크롤링할 노래방 번호

    Returns:
        dict: 노래 정보가 담긴 딕셔너리 또는 에러 정보
    """
    url = f"https://www.tjmedia.com/tjsong/song_search_list.asp?strType=16&natType=&strText={song_number}&strCond=1&strSize05=100"

    try:
        # 요청 및 응답
        response = requests.get(url, headers=BROWSER_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()

        # HTML 파싱 (인코딩 처리)
        html = response.content.decode("utf-8", "replace")
        soup = BeautifulSoup(html, "lxml")

        # 테이블에서 데이터 추출 (셀렉터 수정)
        # span 태그를 사용하지 않고 td 자체를 선택
        song_number_el = soup.select(
            "#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(1)"
        )

        song_title_el = soup.select(
            "#BoardType1 > table > tbody > tr:nth-child(2) > td.left"
        )

        singer_name_el = soup.select(
            "#BoardType1 > table > tbody > tr:nth-child(2) > td:nth-child(3)"
        )

        # 결과가 없는 경우 처리
        if not song_number_el or not song_title_el or not singer_name_el:
            return {
                "number": str(song_number),
                "error": True,
                "error_message": "검색 결과 없음",
            }

        # 텍스트 추출 및 정리
        number = song_number_el[0].text.strip() if song_number_el else "정보 없음"
        title = song_title_el[0].text.strip() if song_title_el else "정보 없음"
        singer = singer_name_el[0].text.strip() if singer_name_el else "정보 없음"

        # 노래 정보를 딕셔너리로 반환
        return {
            "number": number,
            "title": title,
            "singer": singer,
        }

    except Exception as e:
        return {"number": str(song_number), "error": True, "error_message": str(e)}


def process_results(results):
    """
    크롤링 결과를 성공과 실패로 분류합니다.

    Args:
        results (list): 크롤링 결과 리스트

    Returns:
        tuple: (성공한 결과 리스트, 실패한 결과 리스트)
    """
    success_results = []
    failed_results = []

    for result in results:
        if result.get("error", False):
            failed_results.append(
                (result["number"], result.get("error_message", "알 수 없는 오류"))
            )
        else:
            success_results.append(result)

    return success_results, failed_results


def print_failed_results(failed_results):
    """
    실패한 크롤링 결과를 출력합니다.

    Args:
        failed_results (list): 실패한 결과 리스트 (number, error_message) 튜플 형태
    """
    if failed_results:
        print("\n===== 크롤링 실패한 노래 번호 =====")
        for number, error_message in failed_results:
            print(f"노래번호 {number}: {error_message}")
        print("================================\n")


def crawl_and_save():
    """
    태진 노래방 정보를 크롤링하고 저장합니다.

    Returns:
        bool: 크롤링 및 저장 성공 여부
    """
    print(
        f"{START_NUMBER}번부터 {END_NUMBER}번까지 태진 노래방 곡 정보 크롤링을 시작합니다..."
    )
    print(f"사용 프로세스 수: {PROCESSES}")

    # 시작 시간 기록
    start_time = time.time()

    # 멀티프로세싱으로 크롤링
    try:
        pool = Pool(processes=PROCESSES)
        results = pool.map(crawl_song_info, range(START_NUMBER, END_NUMBER + 1))
        pool.close()
        pool.join()
    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")
        return False

    # 결과 처리
    success_results, failed_results = process_results(results)

    # 실패한 결과 출력
    print_failed_results(failed_results)

    # 성공한 결과가 없으면 종료
    if not success_results:
        print("크롤링에 성공한 노래 정보가 없습니다.")
        return False

    # 엑셀 파일로 저장
    save_to_excel(success_results, OUTPUT_FILE, DATA_FIELDS)

    # 경과 시간 계산
    elapsed_time = calculate_elapsed_time(start_time)
    print(f"크롤링 완료! 소요 시간: {elapsed_time:.2f}초")

    # Supabase에 업로드
    print("\nSupabase에 데이터 업로드 중...")
    upload_data = filter_data_fields(success_results, DATA_FIELDS)
    upload_success = upload_to_supabase(
        upload_data, TJ_TABLE_NAME, conflict_column="number"
    )

    if upload_success:
        print(
            f"Supabase '{TJ_TABLE_NAME}' 테이블에 {len(upload_data)}개의 노래 정보 업로드 완료!"
        )
        return True
    else:
        print("Supabase 업로드에 실패했습니다.")
        return False


if __name__ == "__main__":
    crawl_and_save()
