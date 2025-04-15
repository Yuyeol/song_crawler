"""
텍스트 분리 유틸리티

다양한 언어(일본어, 한국어, 영어)와 기타 문자(숫자, 특수문자 등)가 혼합된 텍스트를 구분하는 기능 제공
"""


def is_japanese_char(char):
    """
    문자가 일본어(히라가나, 가타카나, 한자)인지 확인합니다.

    Args:
        char (str): 확인할 문자

    Returns:
        bool: 일본어 문자인 경우 True, 아니면 False
    """
    return (
        ("\u3040" <= char <= "\u309f")  # 히라가나
        or ("\u30a0" <= char <= "\u30ff")  # 가타카나
        or ("\u4e00" <= char <= "\u9fff")  # 한자
    )


def is_korean_char(char):
    """
    문자가 한국어인지 확인합니다.

    Args:
        char (str): 확인할 문자

    Returns:
        bool: 한국어 문자인 경우 True, 아니면 False
    """
    return (
        ("\uac00" <= char <= "\ud7a3")  # 한글 음절
        or ("\u1100" <= char <= "\u11ff")  # 한글 자모
        or ("\u3130" <= char <= "\u318f")  # 한글 호환 자모
    )


def is_english_char(char):
    """
    문자가 영어(알파벳)인지 확인합니다.

    Args:
        char (str): 확인할 문자

    Returns:
        bool: 영어 문자인 경우 True, 아니면 False
    """
    return "A" <= char <= "Z" or "a" <= char <= "z"


def is_numeric_char(char):
    """
    문자가 숫자인지 확인합니다.

    Args:
        char (str): 확인할 문자

    Returns:
        bool: 숫자인 경우 True, 아니면 False
    """
    return "0" <= char <= "9"


def get_char_type(char):
    """
    문자의 타입(일본어, 한국어, 영어, 숫자, 기타)을 반환합니다.

    Args:
        char (str): 타입을 확인할 문자

    Returns:
        str: 'japanese', 'korean', 'english', 'numeric', 'other' 중 하나
    """
    if is_japanese_char(char):
        return "japanese"
    elif is_korean_char(char):
        return "korean"
    elif is_english_char(char):
        return "english"
    elif is_numeric_char(char):
        return "numeric"
    else:
        return "other"


def separate_text(text):
    """
    텍스트를 언어 및 문자 타입에 따라 분리합니다.

    Args:
        text (str): 분리할 텍스트

    Returns:
        list: 분리된 텍스트 세그먼트 리스트, 각 세그먼트는 (텍스트, 타입) 튜플
    """
    if not text or not isinstance(text, str):
        return []

    segments = []
    current_segment = ""
    current_type = None

    for char in text:
        char_type = get_char_type(char)

        # 첫 번째 문자 처리
        if current_type is None:
            current_type = char_type
            current_segment = char
        # 같은 타입의 문자 계속
        elif current_type == char_type:
            current_segment += char
        # 다른 타입의 문자 시작
        else:
            segments.append((current_segment, current_type))
            current_type = char_type
            current_segment = char

    # 마지막 세그먼트 추가
    if current_segment:
        segments.append((current_segment, current_type))

    return segments


def separate_text_extended(text):
    """
    텍스트를 언어 및 문자 타입에 따라 분리하고, 추가 정보를 포함합니다.

    Args:
        text (str): 분리할 텍스트

    Returns:
        dict: 분리된 텍스트와 세그먼트 정보
        {
            'original': 원본 텍스트,
            'segments': [
                {
                    'text': 세그먼트 텍스트,
                    'type': 세그먼트 타입('japanese', 'korean', 'english', 'numeric', 'other'),
                    'start': 세그먼트 시작 인덱스,
                    'end': 세그먼트 끝 인덱스
                },
                ...
            ]
        }
    """
    if not text or not isinstance(text, str):
        return {"original": "", "segments": []}

    result = {"original": text, "segments": []}
    segments = []
    current_segment = ""
    current_type = None
    start_idx = 0

    for idx, char in enumerate(text):
        char_type = get_char_type(char)

        # 첫 번째 문자 처리
        if current_type is None:
            current_type = char_type
            current_segment = char
            start_idx = idx
        # 같은 타입의 문자 계속
        elif current_type == char_type:
            current_segment += char
        # 다른 타입의 문자 시작
        else:
            segments.append(
                {
                    "text": current_segment,
                    "type": current_type,
                    "start": start_idx,
                    "end": idx - 1,
                }
            )
            current_type = char_type
            current_segment = char
            start_idx = idx

    # 마지막 세그먼트 추가
    if current_segment:
        segments.append(
            {
                "text": current_segment,
                "type": current_type,
                "start": start_idx,
                "end": len(text) - 1,
            }
        )

    result["segments"] = segments
    return result
