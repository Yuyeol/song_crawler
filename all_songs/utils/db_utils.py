"""
데이터베이스 관련 유틸리티 함수
"""

import os
import requests


def get_all_existing_song_numbers(table_name):
    """
    DB에 존재하는 모든 곡 번호를 한 번에 가져옵니다.

    Args:
        table_name (str): 조회할 Supabase 테이블 이름

    Returns:
        set: 존재하는 모든 곡 번호 세트 또는 None (오류 발생 시)
    """
    try:
        print("DB에서 기존 곡 번호 목록을 가져오는 중...")

        # Supabase 설정
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

        # 번호만 선택 (모든 곡)
        query_params = {"select": "number"}

        response = requests.get(
            f"{supabase_url}/rest/v1/{table_name}", headers=headers, params=query_params
        )

        if response.status_code == 200:
            # 번호 목록을 세트로 변환
            existing_numbers = set(int(item["number"]) for item in response.json())
            print(f"DB에서 총 {len(existing_numbers)}개 기존 곡 번호를 가져왔습니다.")
            return existing_numbers
        else:
            print(f"기존 곡 조회 오류. 상태 코드: {response.status_code}")
            print("오류 내용:", response.text)
            return None
    except Exception as e:
        print(f"기존 곡 목록 조회 중 오류 발생: {str(e)}")
        return None


def get_numbers_to_crawl(table_name, start_number, end_number):
    """
    크롤링이 필요한 번호 목록을 계산합니다.

    Args:
        table_name (str): 조회할 Supabase 테이블 이름
        start_number (int): 시작 번호
        end_number (int): 종료 번호

    Returns:
        list: 크롤링할 번호 목록 또는 None (DB 조회 오류 시)
    """
    # DB에 이미 존재하는 모든 곡 번호 가져오기 (한 번만 조회)
    existing_songs = get_all_existing_song_numbers(table_name)

    if existing_songs is None:
        print("기존 곡 목록을 가져올 수 없어 크롤링을 중단합니다.")
        return None

    # 없는 곡 번호 확인
    print("크롤링이 필요한 번호 확인 중...")
    all_numbers = set(range(start_number, end_number + 1))
    numbers_to_crawl = list(all_numbers - existing_songs)
    numbers_to_crawl.sort()  # 오름차순 정렬

    if not numbers_to_crawl:
        print(f"크롤링할 새 곡이 없습니다. (범위: {start_number}-{end_number})")
        return []

    print(
        f"총 {len(numbers_to_crawl)}개 번호 크롤링 예정 (범위: {start_number}-{end_number})"
    )
    return numbers_to_crawl
