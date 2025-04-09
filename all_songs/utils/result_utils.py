"""
결과 처리 관련 유틸리티 함수
"""


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
