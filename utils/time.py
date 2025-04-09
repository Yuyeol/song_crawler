import time


def calculate_elapsed_time(start_time, end_time=None):
    """
    경과 시간을 계산합니다.

    Args:
        start_time (float): 시작 시간
        end_time (float): 종료 시간. None이면 현재 시간

    Returns:
        float: 경과 시간 (초)
    """
    if end_time is None:
        end_time = time.time()

    return end_time - start_time
