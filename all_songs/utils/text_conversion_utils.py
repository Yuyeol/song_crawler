"""
텍스트 변환 유틸리티

다양한 언어가 혼합된 텍스트를 처리하는 통합 기능 제공
"""

from all_songs.utils.text_separators import separate_text, separate_text_extended
from all_songs.utils.text_normalizers import (
    normalize_english,
    extract_korean_chosung,
    normalize_by_type,
)
from all_songs.utils.japanese_utils import extract_japanese_pronunciation


def convert_mixed_text(text):
    """
    혼합된 텍스트를 변환합니다.
    - 일본어는 한국어 발음으로 변환
    - 영어는 소문자로 변환
    - 한국어 및 기타 문자는 그대로 유지

    Args:
        text (str): 변환할 텍스트

    Returns:
        str: 변환된 텍스트
    """
    if not text or not isinstance(text, str):
        return ""

    # 텍스트를 언어별로 분리
    segments = separate_text(text)

    # 각 세그먼트 변환
    result = []
    for segment, segment_type in segments:
        if segment_type == "japanese":
            # 일본어 부분은 한국어 발음으로 변환
            jp_result = extract_japanese_pronunciation(segment)
            if jp_result:
                _, _, korean_pron = jp_result
                result.append(korean_pron)
            else:
                # 변환 실패 시 원본 유지
                result.append(segment)
        elif segment_type == "english":
            # 영어는 소문자로 변환
            result.append(normalize_english(segment))
        else:
            # 다른 타입은 그대로 유지
            result.append(segment)

    return "".join(result)


def convert_mixed_text_with_info(text):
    """
    혼합된 텍스트를 변환하고 세부 정보를 제공합니다.

    Args:
        text (str): 변환할 텍스트

    Returns:
        dict: 변환 정보와 결과
        {
            'original': 원본 텍스트,
            'converted': 변환된 텍스트,
            'segments': [
                {
                    'text': 원본 세그먼트,
                    'type': 세그먼트 타입,
                    'converted': 변환된 세그먼트,
                    'extras': 추가 정보 (로마자 등)
                },
                ...
            ]
        }
    """
    if not text or not isinstance(text, str):
        return {"original": "", "converted": "", "segments": []}

    # 텍스트를 언어별로 분리 (확장 정보 포함)
    extended_info = separate_text_extended(text)

    # 각 세그먼트 변환
    result = []
    segments_info = []

    for segment in extended_info["segments"]:
        segment_text = segment["text"]
        segment_type = segment["type"]
        converted_segment = ""
        extras = {}

        if segment_type == "japanese":
            # 일본어 부분은 한국어 발음으로 변환
            jp_result = extract_japanese_pronunciation(segment_text)
            if jp_result:
                _, romaji, korean_pron = jp_result
                converted_segment = korean_pron
                extras["romaji"] = romaji
            else:
                # 변환 실패 시 원본 유지
                converted_segment = segment_text
        elif segment_type == "english":
            # 영어는 소문자로 변환
            converted_segment = normalize_english(segment_text)
        elif segment_type == "korean":
            # 한국어는 그대로 유지하되, 초성 정보 추가
            converted_segment = segment_text
            extras["chosung"] = extract_korean_chosung(segment_text)
        else:
            # 다른 타입은 일반 정규화 적용
            converted_segment = normalize_by_type(segment_text, segment_type)

        result.append(converted_segment)

        segment_info = {
            "text": segment_text,
            "type": segment_type,
            "converted": converted_segment,
        }

        # 추가 정보가 있으면 포함
        if extras:
            segment_info["extras"] = extras

        segments_info.append(segment_info)

    return {"original": text, "converted": "".join(result), "segments": segments_info}


def extract_text_normalized_forms(text):
    """
    텍스트의 다양한 정규화 형태를 추출합니다.

    Args:
        text (str): 처리할 텍스트

    Returns:
        dict: 다양한 정규화 형태
        {
            'original': 원본 텍스트,
            'normalized': 기본 정규화 텍스트 (일본어 -> 한국어 발음, 영어 -> 소문자),
            'simplified': 단순화된 텍스트 (한국어 -> 초성, 그 외 기본 정규화),
            'segments': 세그먼트 별 정보
        }
    """
    if not text or not isinstance(text, str):
        return {"original": "", "normalized": "", "simplified": "", "segments": []}

    # 기본 정규화
    basic_info = convert_mixed_text_with_info(text)
    normalized = basic_info["converted"]

    # 단순화 (한국어 초성 추출 등)
    simplified_segments = []
    for segment in basic_info["segments"]:
        if segment["type"] == "korean":
            # 한국어는 초성 추출
            simplified_segments.append(extract_korean_chosung(segment["text"]))
        else:
            # 그 외는 이미 정규화된 형태 사용
            simplified_segments.append(segment["converted"])

    simplified = "".join(simplified_segments)

    return {
        "original": text,
        "normalized": normalized,
        "simplified": simplified,
        "segments": basic_info["segments"],
    }


# 수파베이스 업로드를 위한 함수들 추가
def prepare_for_supabase(text):
    """
    수파베이스 업로드를 위한 텍스트 정보를 준비합니다.

    Args:
        text (str): 처리할 텍스트

    Returns:
        dict: 수파베이스 업로드에 필요한 정보
        {
            'original': 원본 텍스트,
            'pron': 발음 변환 텍스트,
            'chosung': 초성 변환 텍스트,
            'contains_japanese': 일본어 포함 여부,
            'contains_korean': 한국어 포함 여부,
            'contains_english': 영어 포함 여부
        }
    """
    if not text or not isinstance(text, str):
        return {
            "original": "",
            "pron": "",
            "chosung": "",
            "contains_japanese": False,
            "contains_korean": False,
            "contains_english": False,
        }

    # 텍스트 분리 및 변환
    basic_info = convert_mixed_text_with_info(text)

    # 언어 포함 여부 확인
    contains_japanese = any(seg["type"] == "japanese" for seg in basic_info["segments"])
    contains_korean = any(seg["type"] == "korean" for seg in basic_info["segments"])
    contains_english = any(seg["type"] == "english" for seg in basic_info["segments"])

    # 케이스별 처리
    pron = ""
    chosung = ""

    # 1. 순수 영어인 경우
    if contains_english and not contains_japanese and not contains_korean:
        normalized = normalize_english(text)
        pron = normalized
        chosung = normalized

    # 2. 한국어 포함 (일본어 미포함)
    elif contains_korean and not contains_japanese:
        pron = basic_info["converted"]  # 영어 로워케이스, 한국어 원본, 기호 그대로

        # 초성 변환: 한국어는 초성으로, 나머지는 정규화된 형태
        chosung_segments = []
        for segment in basic_info["segments"]:
            if segment["type"] == "korean":
                chosung_segments.append(extract_korean_chosung(segment["text"]))
            else:
                chosung_segments.append(segment["converted"])

        chosung = "".join(chosung_segments)

    # 3. 일본어 포함
    elif contains_japanese:
        pron = basic_info["converted"]  # 한국어 발음 + 정규화

        # 초성 변환: 일본어는 한국어 발음의 초성, 한국어는 초성, 나머지는 정규화
        chosung_segments = []
        for segment in basic_info["segments"]:
            if segment["type"] == "japanese":
                # 일본어 부분의 한국어 발음에서 초성 추출
                jp_converted = segment["converted"]
                chosung_segments.append(extract_korean_chosung(jp_converted))
            elif segment["type"] == "korean":
                chosung_segments.append(extract_korean_chosung(segment["text"]))
            else:
                chosung_segments.append(segment["converted"])

        chosung = "".join(chosung_segments)

    # 4. 기타 경우 (숫자, 특수문자만 있는 경우 등)
    else:
        pron = basic_info["converted"]
        chosung = basic_info["converted"]

    return {
        "original": text,
        "pron": pron,
        "chosung": chosung,
        "contains_japanese": contains_japanese,
        "contains_korean": contains_korean,
        "contains_english": contains_english,
    }


def process_title_singer_for_supabase(title, singer):
    """
    금영/태진 노래방 타이틀과 싱어 정보를 수파베이스 업로드용으로 처리합니다.

    Args:
        title (str): 노래 제목
        singer (str): 가수 이름

    Returns:
        dict: 처리된 정보
        {
            'title': 원본 제목,
            'title_pron': 제목 발음 변환,
            'title_chosung': 제목 초성 변환,
            'singer': 원본 가수,
            'singer_pron': 가수 발음 변환,
            'singer_chosung': 가수 초성 변환
        }
    """
    # 제목 처리
    title_info = prepare_for_supabase(title)

    # 가수 처리
    singer_info = prepare_for_supabase(singer)

    return {
        "title": title,
        "title_pron": title_info["pron"],
        "title_chosung": title_info["chosung"],
        "singer": singer,
        "singer_pron": singer_info["pron"],
        "singer_chosung": singer_info["chosung"],
    }
