"""
텍스트 정규화 유틸리티

다양한 언어 텍스트의 정규화 및 변환 기능 제공
"""


def normalize_english(text):
    """
    영어 텍스트를 소문자로 정규화합니다.

    Args:
        text (str): 정규화할 영어 텍스트

    Returns:
        str: 소문자로 정규화된 텍스트
    """
    if not text or not isinstance(text, str):
        return ""

    return text.lower()


def extract_korean_chosung(text):
    """
    한글 텍스트에서 초성을 추출합니다.

    Args:
        text (str): 초성을 추출할 한글 텍스트

    Returns:
        str: 추출된 초성
    """
    if not text or not isinstance(text, str):
        return ""

    result = []

    # 한글 초성 리스트
    CHOSUNG = [
        "ㄱ",
        "ㄲ",
        "ㄴ",
        "ㄷ",
        "ㄸ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅃ",
        "ㅅ",
        "ㅆ",
        "ㅇ",
        "ㅈ",
        "ㅉ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]

    for char in text:
        # 한글인 경우만 처리
        if "가" <= char <= "힣":
            # 한글 유니코드에서 초성 인덱스 계산
            char_code = ord(char) - ord("가")
            chosung_index = char_code // (21 * 28)
            result.append(CHOSUNG[chosung_index])
        else:
            # 한글이 아닌 경우 그대로 유지
            result.append(char)

    return "".join(result)


def normalize_numeric(text):
    """
    숫자가 포함된 텍스트를 정규화합니다.
    현재는 그대로 반환하지만, 필요에 따라 확장 가능합니다.

    Args:
        text (str): 정규화할 숫자 텍스트

    Returns:
        str: 정규화된 텍스트
    """
    if not text or not isinstance(text, str):
        return ""

    # 현재는 단순 반환, 필요시 로직 추가
    return text


def normalize_other(text):
    """
    기타 문자(특수 문자, 기호 등)가 포함된 텍스트를 정규화합니다.
    현재는 그대로 반환하지만, 필요에 따라 확장 가능합니다.

    Args:
        text (str): 정규화할 텍스트

    Returns:
        str: 정규화된 텍스트
    """
    if not text or not isinstance(text, str):
        return ""

    # 현재는 단순 반환, 필요시 로직 추가
    return text


def normalize_by_type(text, text_type):
    """
    텍스트 타입에 따라 적절한 정규화 함수를 호출합니다.

    Args:
        text (str): 정규화할 텍스트
        text_type (str): 텍스트 타입('japanese', 'korean', 'english', 'numeric', 'other')

    Returns:
        str: 정규화된 텍스트
    """
    if not text or not isinstance(text, str):
        return ""

    if text_type == "english":
        return normalize_english(text)
    elif text_type == "korean":
        return text  # 한국어는 기본적으로 유지, 초성 추출은 별도 함수 사용
    elif text_type == "numeric":
        return normalize_numeric(text)
    elif text_type == "other":
        return normalize_other(text)
    else:
        return text  # 기본적으로 텍스트 유지
