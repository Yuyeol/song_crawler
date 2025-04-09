"""
인기곡 크롤러 메인 실행 유틸리티 함수
"""

import time
from utils import (
    save_to_excel,
    upload_to_supabase,
    filter_data_fields,
    calculate_elapsed_time,
)


def run_chart_crawler(
    crawler_func,
    output_file,
    table_name,
    data_fields,
    service_name="노래방 인기 차트",
    update_mode="truncate",
):
    """
    인기 차트 크롤러를 실행하고 결과를 처리합니다.

    Args:
        crawler_func (function): 인기 차트를 크롤링하는 함수
        output_file (str): 저장할 엑셀 파일 이름
        table_name (str): 업로드할 Supabase 테이블 이름
        data_fields (list): 데이터 필드 목록
        service_name (str): 크롤링 대상 서비스 이름
        update_mode (str): Supabase 업로드 모드 (기본값: "truncate")

    Returns:
        bool: 크롤링 및 저장 성공 여부
    """
    print(f"{service_name} 크롤링을 시작합니다...")

    # 시작 시간 기록
    start_time = time.time()

    # 크롤링 실행
    chart_results = crawler_func()

    # 결과가 없으면 종료
    if not chart_results:
        print(f"크롤링에 성공한 {service_name} 정보가 없습니다.")
        return False

    # 엑셀 파일로 저장
    save_to_excel(chart_results, output_file, data_fields)

    # 경과 시간 계산
    elapsed_time = calculate_elapsed_time(start_time)
    print(f"크롤링 완료! 총 {len(chart_results)}개 곡, 소요 시간: {elapsed_time:.2f}초")

    # Supabase에 업로드
    print("\nSupabase에 데이터 업로드 중...")
    upload_data = filter_data_fields(chart_results, data_fields)

    # 인기차트는 테이블을 비우고 새로 데이터를 삽입하는 것이 기본
    upload_success = upload_to_supabase(
        upload_data, table_name, update_mode=update_mode
    )

    if upload_success:
        print(
            f"Supabase '{table_name}' 테이블에 {len(upload_data)}개의 {service_name} 정보 업로드 완료!"
        )
        return True
    else:
        print("Supabase 업로드에 실패했습니다.")
        return False
