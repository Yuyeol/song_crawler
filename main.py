#!/usr/bin/env python
"""
노래방 크롤링 도구

금영, 태진 등 노래방 정보를 크롤링하는 도구입니다.
"""

import sys
import argparse
from datetime import datetime
from all_songs import crawl_kumyoung, crawl_taejin
from popular_songs import crawl_kumyoung_popular


def main():
    """
    노래방 크롤링 도구
    크롤링할 노래방 서비스를 결정하고 실행합니다.
    'kumyoung', 'taejin', 'all', 'ky_popular' 중 선택
    """
    # 명령줄 인자 파싱
    parser = argparse.ArgumentParser(description="노래방 크롤링 도구")
    parser.add_argument(
        "service",
        choices=["kumyoung", "taejin", "all", "ky_popular"],
        help="크롤링할 노래방 서비스: 'kumyoung', 'taejin', 'all', 'ky_popular'",
    )

    # 인자 해석
    args = parser.parse_args()
    service = args.service

    # 시작 시간 출력
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n--- 크롤링 시작: {start_time} ---\n")

    # 서비스별 크롤링 실행
    success = False

    if service == "kumyoung":
        success = crawl_kumyoung()
    elif service == "taejin":
        success = crawl_taejin()
    elif service == "ky_popular":
        success = crawl_kumyoung_popular()
    elif service == "all":
        # 두 서비스 모두 실행
        tj_success = crawl_taejin()
        ky_success = crawl_kumyoung()
        success = tj_success and ky_success

    # 종료 시간 출력
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n--- 크롤링 종료: {end_time} ---\n")

    # 성공 여부에 따른 종료 코드 반환
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
