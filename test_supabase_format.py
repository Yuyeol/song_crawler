#!/usr/bin/env python

"""
수파베이스 업로드용 텍스트 변환 테스트 스크립트
"""

import sys
import json
from all_songs.utils.text_conversion_utils import (
    prepare_for_supabase,
    process_title_singer_for_supabase,
)


def print_separator():
    """구분선을 출력합니다."""
    print("=" * 60)


def test_prepare_for_supabase(text):
    """수파베이스 준비 함수를 테스트합니다."""
    print(f"원본: '{text}'")

    result = prepare_for_supabase(text)

    print(f"변환 결과:")
    print(f"  발음(pron): '{result['pron']}'")
    print(f"  초성(chosung): '{result['chosung']}'")
    print(
        f"  포함 언어: 일본어({result['contains_japanese']}), 한국어({result['contains_korean']}), 영어({result['contains_english']})"
    )
    print_separator()


def test_process_title_singer(title, singer):
    """타이틀과 싱어 처리 함수를 테스트합니다."""
    print(f"원본 제목: '{title}'")
    print(f"원본 가수: '{singer}'")

    result = process_title_singer_for_supabase(title, singer)

    print(f"제목 발음(title_pron): '{result['title_pron']}'")
    print(f"제목 초성(title_chosung): '{result['title_chosung']}'")
    print(f"가수 발음(singer_pron): '{result['singer_pron']}'")
    print(f"가수 초성(singer_chosung): '{result['singer_chosung']}'")
    print_separator()


def main():
    # 테스트 케이스: 제목과 가수 쌍
    test_cases = [
        # 순수 한국어
        {"title": "사랑을 했다", "singer": "아이콘"},
        # 순수 영어
        {"title": "LOVE YOURSELF", "singer": "BTS"},
        # 한국어 + 영어
        {"title": "작은 것들을 위한 시 Boy With Luv", "singer": "방탄소년단 BTS"},
        # 일본어 포함
        {"title": "東京TOKYO서울", "singer": "가수名無し"},
        # 일본어 + 영어 + 한국어
        {"title": "ワンピース(One Piece, 원피스)", "singer": "애니메이션"},
        # 특수문자, 숫자 포함
        {"title": "2002年の日記", "singer": "K-POP 가수"},
        # 일본어 가수명
        {"title": "벚꽃 엔딩", "singer": "버스커버스커(バスカーバスカー)"},
        # 영어 + 일본어
        {"title": "NARUTO忍者", "singer": "JPOP 가수"},
        # 복잡한 혼합
        {
            "title": "鬼滅の刃(Demon Slayer, 귀멸의 칼날)",
            "singer": "애니 OST - アニソン",
        },
    ]

    # 커맨드 라인에서 텍스트를 받은 경우
    if len(sys.argv) > 2:
        test_title = sys.argv[1]
        test_singer = sys.argv[2]
        print("***** 단일 케이스 테스트 *****")
        test_prepare_for_supabase(test_title)
        test_prepare_for_supabase(test_singer)
        test_process_title_singer(test_title, test_singer)
    # 샘플 테스트 케이스 사용
    else:
        print("==== 수파베이스 업로드용 변환 테스트 ====")
        print("샘플 테스트 케이스를 사용합니다.")
        print("직접 테스트하려면: python test_supabase_format.py <제목> <가수>\n")

        for idx, case in enumerate(test_cases):
            print(f"\n***** 테스트 케이스 #{idx+1} *****")
            print("--- 제목 변환 테스트 ---")
            test_prepare_for_supabase(case["title"])
            print("--- 가수 변환 테스트 ---")
            test_prepare_for_supabase(case["singer"])
            print("--- 통합 처리 테스트 ---")
            test_process_title_singer(case["title"], case["singer"])


if __name__ == "__main__":
    main()
