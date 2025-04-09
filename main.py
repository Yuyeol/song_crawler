#!/usr/bin/env python

import sys
import argparse
from datetime import datetime
from all_songs import crawl_kumyoung, crawl_taejin
from popular_songs import crawl_kumyoung_popular, crawl_taejin_popular


def main():
    parser = argparse.ArgumentParser(description="노래방 크롤링 도구")
    parser.add_argument(
        "service",
        choices=["kumyoung", "taejin", "all", "ky_popular", "tj_popular"],
        help="크롤링할 노래방 서비스: 'kumyoung', 'taejin', 'all', 'ky_popular', 'tj_popular'",
    )

    args = parser.parse_args()
    service = args.service

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n--- 크롤링 시작: {start_time} ---\n")

    success = False

    if service == "kumyoung":
        success = crawl_kumyoung()
    elif service == "taejin":
        success = crawl_taejin()
    elif service == "ky_popular":
        success = crawl_kumyoung_popular()
    elif service == "tj_popular":
        success = crawl_taejin_popular()
    elif service == "all":
        tj_success = crawl_taejin()
        ky_success = crawl_kumyoung()
        success = tj_success and ky_success

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n--- 크롤링 종료: {end_time} ---\n")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
