#!/usr/bin/env python

"""
다국어 텍스트 변환 유틸리티 테스트 스크립트
"""

import sys
import json
from all_songs.utils.text_separators import separate_text_extended
from all_songs.utils.text_normalizers import extract_korean_chosung
from all_songs.utils.text_conversion_utils import (
    convert_mixed_text,
    convert_mixed_text_with_info,
    extract_text_normalized_forms,
)


def print_separator():
    """구분선을 출력합니다."""
    print("=" * 60)


def test_text_separation(text):
    """텍스트 분리 기능을 테스트합니다."""
    print("[테스트 1: 텍스트 분리]")
    print(f"원본: {text}")

    # 텍스트 분리 결과
    separated = separate_text_extended(text)

    print("분리 결과:")
    for segment in separated["segments"]:
        print(
            f"  {segment['type'].upper()}: '{segment['text']}' (위치: {segment['start']}-{segment['end']})"
        )
    print_separator()


def test_text_conversion(text):
    """텍스트 변환 기능을 테스트합니다."""
    print("[테스트 2: 기본 텍스트 변환]")
    print(f"원본: {text}")

    # 기본 변환 결과
    converted = convert_mixed_text(text)
    print(f"변환: {converted}")
    print_separator()


def test_text_conversion_with_info(text):
    """세부 정보가 포함된 텍스트 변환을 테스트합니다."""
    print("[테스트 3: 세부 정보가 포함된 텍스트 변환]")
    print(f"원본: {text}")

    # 상세 정보 포함 변환 결과
    result = convert_mixed_text_with_info(text)
    print(f"변환: {result['converted']}")

    print("세그먼트 정보:")
    for segment in result["segments"]:
        segment_type = segment["type"].upper()
        text = segment["text"]
        converted = segment["converted"]
        extras = segment.get("extras", {})

        # 타입별 추가 정보 표시
        extra_info = ""
        if segment_type == "JAPANESE" and "romaji" in extras:
            extra_info = f", 로마자: {extras['romaji']}"
        elif segment_type == "KOREAN" and "chosung" in extras:
            extra_info = f", 초성: {extras['chosung']}"

        print(f"  {segment_type}: '{text}' -> '{converted}'{extra_info}")
    print_separator()


def test_normalized_forms(text):
    """다양한 정규화 형태를 테스트합니다."""
    print("[테스트 4: 다양한 정규화 형태]")
    print(f"원본: {text}")

    # 다양한 정규화 형태
    forms = extract_text_normalized_forms(text)
    print(f"기본 정규화: {forms['normalized']}")
    print(f"단순화: {forms['simplified']}")
    print_separator()


def test_korean_chosung(text):
    """한국어 초성 추출을 테스트합니다."""
    print("[테스트 5: 한국어 초성 추출]")
    print(f"원본: {text}")

    # 초성 추출 결과
    chosung = extract_korean_chosung(text)
    print(f"초성: {chosung}")
    print_separator()


def main():
    """메인 함수"""
    # 테스트 케이스
    test_cases = [
        # 다양한 언어 혼합
        "안녕하세요こんにちはHello",  # 한국어 + 일본어 + 영어
        "NARUTO忍者는 뛰어나다",  # 영어 + 일본어 + 한국어
        "東京TOKYO서울",  # 일본어 + 영어 + 한국어
        "進撃のTITAN은 인기있다",  # 일본어 + 영어 + 한국어
        "銀魂 GINTAMA 은혼",  # 일본어 + 영어 + 한국어
        "나루토(NARUTO、ナルト)",  # 한국어 + 영어 + 일본어 + 특수문자
        "ワンピース(One Piece, 원피스)",  # 일본어 + 영어 + 한국어 + 특수문자
        "鬼滅の刃(Demon Slayer, 귀멸의 칼날)",  # 일본어 + 영어 + 한국어 + 특수문자
        "BTS(방탄소년단)のファン",  # 영어 + 한국어 + 특수문자 + 일본어
        "123테스트テストTest",  # 숫자 + 한국어 + 일본어 + 영어
    ]

    # 커맨드 라인에서 텍스트를 받은 경우
    if len(sys.argv) > 1:
        test_text = " ".join(sys.argv[1:])
        print("***** 단일 텍스트 테스트 *****")
        test_text_separation(test_text)
        test_text_conversion(test_text)
        test_text_conversion_with_info(test_text)
        test_normalized_forms(test_text)
        if any(is_korean_char(char) for char in test_text):
            test_korean_chosung(test_text)
    # 샘플 테스트 케이스 사용
    else:
        print("==== 다국어 텍스트 변환 유틸리티 테스트 ====")
        print("샘플 테스트 케이스를 사용합니다.")
        print(
            "직접 테스트하려면: python test_multilingual_utils.py <테스트할 텍스트>\n"
        )

        for idx, case in enumerate(test_cases):
            print(f"\n***** 테스트 케이스 #{idx+1} *****")
            test_text_separation(case)
            test_text_conversion(case)
            test_text_conversion_with_info(case)
            test_normalized_forms(case)
            if any(is_korean_char(char) for char in case):
                test_korean_chosung(case)


# 한국어 문자 확인 함수
def is_korean_char(char):
    """
    문자가 한국어인지 확인합니다.
    """
    return (
        ("\uac00" <= char <= "\ud7a3")  # 한글 음절
        or ("\u1100" <= char <= "\u11ff")  # 한글 자모
        or ("\u3130" <= char <= "\u318f")  # 한글 호환 자모
    )


if __name__ == "__main__":
    main()
