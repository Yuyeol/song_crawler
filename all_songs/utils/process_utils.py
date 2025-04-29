"""
멀티프로세싱 관련 유틸리티 함수
"""

from multiprocessing import Pool


def crawl_with_multiprocessing(crawler_func, numbers, processes=4):
    """
    멀티프로세싱으로 크롤링을 실행합니다.

    Args:
        crawler_func (function): 각 번호를 크롤링하는 함수
        numbers (list or range): 크롤링할 번호 목록
        processes (int): 사용할 프로세스 수

    Returns:
        list: 크롤링 결과 리스트 또는 None (오류 발생 시)
    """
    try:
        pool = Pool(processes=processes)
        results = pool.map(crawler_func, numbers)
        pool.close()
        pool.join()
        return results
    except Exception as e:
        print(f"크롤링 중 오류 발생: {str(e)}")
        return None
