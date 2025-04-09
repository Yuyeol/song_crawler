"""
크롤러 메인 실행 유틸리티 함수
"""

import time
from utils import calculate_elapsed_time
from .result_utils import process_results, print_failed_results
from .process_utils import crawl_with_multiprocessing
from .data_utils import save_and_upload_results


def run_crawler(
    crawler_func,
    start_number,
    end_number,
    processes,
    output_file,
    table_name,
    data_fields,
    service_name="노래방",
):
    """
    크롤러를 실행하고 결과를 처리합니다.

    Args:
        crawler_func (function): 각 번호를 크롤링하는 함수
        start_number (int): 시작 번호
        end_number (int): 종료 번호
        processes (int): 사용할 프로세스 수
        output_file (str): 저장할 엑셀 파일 이름
        table_name (str): 업로드할 Supabase 테이블 이름
        data_fields (list): 데이터 필드 목록
        service_name (str): 크롤링 대상 서비스 이름

    Returns:
        bool: 크롤링 및 저장 성공 여부
    """
    print(
        f"{start_number}번부터 {end_number}번까지 {service_name} 곡 정보 크롤링을 시작합니다..."
    )
    print(f"사용 프로세스 수: {processes}")

    # 시작 시간 기록
    start_time = time.time()

    # 멀티프로세싱으로 크롤링
    results = crawl_with_multiprocessing(
        crawler_func, start_number, end_number, processes
    )
    if results is None:
        return False

    # 결과 처리
    success_results, failed_results = process_results(results)

    # 실패한 결과 출력
    print_failed_results(failed_results)

    # 저장 및 업로드
    success = save_and_upload_results(
        success_results, output_file, table_name, data_fields
    )

    # 경과 시간 계산
    elapsed_time = calculate_elapsed_time(start_time)
    print(f"크롤링 완료! 소요 시간: {elapsed_time:.2f}초")

    return success
