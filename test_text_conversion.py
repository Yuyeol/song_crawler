#!/usr/bin/env python

"""
텍스트 변환 유틸리티 테스트 스크립트
"""

import sys
from all_songs.utils.text_conversion_utils import (
    convert_mixed_text,
    convert_mixed_text_with_info,
)


def print_test_result(text):
    """
    텍스트를 변환하고 결과를 출력합니다.

    Args:
        text (str): 테스트할 텍스트
    """
    # 기본 변환 결과
    converted = convert_mixed_text(text)
    print(f"원본: {text}")
    print(f"변환: {converted}")
    print("-" * 50)

    # 상세 정보 포함 변환 결과
    detailed = convert_mixed_text_with_info(text)
    print("상세 정보:")
    for segment in detailed["segments"]:
        if segment["is_japanese"]:
            print(
                f"  일본어: {segment['text']} -> {segment['converted']} (로마자: {segment.get('romaji', '')})"
            )
        else:
            print(f"  영어/숫자: {segment['text']} -> {segment['converted']}")
    print("=" * 50)


def main():
    # 테스트 케이스
    test_cases = [
        "こんにちは",  # 순수 일본어
        "HELLO",  # 순수 영어 (대문자)
        "hello123",  # 영어와 숫자
        "こんにちはWorld",  # 일본어 + 영어
        "ハローWorld123",  # 일본어 + 영어 + 숫자
        "NARUTO忍者",  # 영어 + 일본어
        "ワンPIECE海賊王",  # 일본어 + 영어 + 일본어
        "進撃のTITAN",  # 일본어 + 영어
        "DEMON SLAYER: 鬼滅の刃",  # 영어 + 특수문자 + 일본어
        "ジョジョJOJO奇妙な冒険",  # 일본어 + 영어 + 일본어
        "FATE/stay night",  # 영어 + 특수문자 + 영어
        "RE:ゼロから始める異世界生活",  # 영어 + 특수문자 + 일본어
        "SPY×FAMILY",  # 영어 + 특수문자 + 영어
        "僕のヒーローACADEMIA",  # 일본어 + 영어
        "東京TOKYO",  # 일본어 + 영어
    ]

    # 커맨드 라인에서 텍스트를 받은 경우
    if len(sys.argv) > 1:
        test_text = " ".join(sys.argv[1:])
        print_test_result(test_text)
    # 샘플 테스트 케이스 사용
    else:
        print("==== 혼합 텍스트 변환 테스트 ====")
        print("샘플 테스트 케이스를 사용합니다.")
        print("직접 테스트하려면: python test_text_conversion.py <테스트할 텍스트>\n")

        for case in test_cases:
            print_test_result(case)


if __name__ == "__main__":
    main()
