#!/usr/bin/env python
"""
노래방 크롤링 도구

금영, 태진 등 노래방 정보를 크롤링하는 도구입니다.
"""

import sys
import argparse
from kumyoung.crawler import crawl_and_save as crawl_kumyoung
from taejin.crawler import crawl_and_save as crawl_taejin


def main():
    """
    메인 실행 함수
    """
    # 명령행 인자 파싱
    parser = argparse.ArgumentParser(description="노래방 크롤링 도구")
    parser.add_argument(
        "--target",
        choices=["kumyoung", "taejin", "all"],
        default="kumyoung",
        help="크롤링할 노래방(금영, 태진, 모두)",
    )
    args = parser.parse_args()

    success = True

    # 금영 노래방 크롤링
    if args.target in ["kumyoung", "all"]:
        print("=== 금영 노래방 크롤링 시작 ===")
        kumyoung_success = crawl_kumyoung()
        if not kumyoung_success:
            success = False
        print("=== 금영 노래방 크롤링 완료 ===\n")

    # 태진 노래방 크롤링
    if args.target in ["taejin", "all"]:
        print("=== 태진 노래방 크롤링 시작 ===")
        taejin_success = crawl_taejin()
        if not taejin_success:
            success = False
        print("=== 태진 노래방 크롤링 완료 ===\n")

    # 종료 코드 설정 (성공: 0, 실패: 1)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
