"""
멀티프로세싱 관련 유틸리티 함수
"""

from multiprocessing import Pool


def crawl_with_multiprocessing(crawler_func, start_number, end_number, processes=4):
    """
    멀티프로세싱으로 크롤링을 실행합니다.

    Args:
        crawler_func (function): 각 번호를 크롤링하는 함수
        start_number (int): 시작 번호
        end_number (int): 종료 번호
        processes (int): 사용할 프로세스 수

    Returns:
        list: 크롤링 결과 리스트 또는 None (오류 발생 시)
    """
    try:
        pool = Pool(processes=processes)
        results = pool.map(crawler_func, range(start_number, end_number + 1))
        pool.close()
        pool.join()
        return results
    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")
        return None
