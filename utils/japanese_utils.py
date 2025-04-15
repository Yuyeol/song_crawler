"""
일본어 발음 변환 유틸리티
"""

import re
import pykakasi


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


def has_japanese(text):
    """
    텍스트에 일본어가 포함되어 있는지 확인합니다.

    Args:
        text (str): 확인할 텍스트

    Returns:
        bool: 일본어가 포함된 경우 True, 아니면 False
    """
    if not text or not isinstance(text, str):
        return False

    return any(is_japanese_char(char) for char in text)


def romanize_japanese(text):
    """
    일본어 텍스트를 로마자로 변환합니다.
    일본어 이외의 문자는 그대로 유지합니다.

    Args:
        text (str): 변환할 텍스트

    Returns:
        str: 로마자로 변환된 텍스트
    """
    if not text or not isinstance(text, str):
        return None

    if not has_japanese(text):
        return None

    # 텍스트를 일본어와 비일본어 부분으로 분리
    parts = []
    current_part = ""
    current_is_japanese = None

    for char in text:
        is_jp = is_japanese_char(char)

        # 새로운 그룹 시작
        if current_is_japanese is None:
            current_is_japanese = is_jp
            current_part = char
        # 같은 종류의 문자 계속
        elif current_is_japanese == is_jp:
            current_part += char
        # 다른 종류의 문자 시작
        else:
            parts.append((current_part, current_is_japanese))
            current_is_japanese = is_jp
            current_part = char

    # 마지막 부분 추가
    if current_part:
        parts.append((current_part, current_is_japanese))

    # pykakasi 초기화
    kks = pykakasi.kakasi()

    # 각 부분 변환
    result = []
    for part, is_jp in parts:
        if is_jp:
            # 일본어 부분 변환
            converted = kks.convert(part)
            # 로마자를 소문자로 변환하여 일관성 유지
            romaji = "".join(item["hepburn"].lower() for item in converted)
            result.append(romaji)
        else:
            # 비일본어 부분은 그대로 유지
            result.append(part)

    return "".join(result)


def korean_pronunciation_from_romaji(romaji):
    """
    로마자를 한국어 발음으로 변환합니다.

    Args:
        romaji (str): 변환할 로마자

    Returns:
        str: 한국어 발음으로 변환된 텍스트
    """
    if not romaji or not isinstance(romaji, str):
        return None

    # 로마자를 소문자로 변환하여 일관성 유지
    romaji = romaji.lower()

    # 일본어 장음 패턴 전처리
    # ou -> o, ei -> e 등의 장음 패턴을 단일 모음으로 처리
    romaji = re.sub(r"ou", "o", romaji)
    romaji = re.sub(r"ei", "e", romaji)
    romaji = re.sub(r"aa", "a", romaji)
    romaji = re.sub(r"ii", "i", romaji)
    romaji = re.sub(r"uu", "u", romaji)
    romaji = re.sub(r"ee", "e", romaji)
    romaji = re.sub(r"oo", "o", romaji)

    # 특수 패턴 전처리
    # 촉음(っ)과 같은 특수 패턴
    romaji = re.sub(r"([kstpm])\1", r"\1\1", romaji)  # kk -> kk (촉음)

    # 응음(ん) 처리 개선 - 음절 끝에 오는 n을 받침으로 처리
    # n뒤에 자음이 오는 경우 처리 (ex: genki -> 겐키, sanpo -> 산포)
    romaji = re.sub(
        r"n([kgsztdhbpmrjn])", r"N\1", romaji
    )  # n+자음 -> N+자음 (N은 받침 'ㄴ'을 의미)
    # n뒤에 모음이 아닌 경우 (단어 끝) 처리
    romaji = re.sub(r"n$", r"N", romaji)  # 끝에 오는 n -> N

    # 로마자-한국어 발음 맵핑 (확장된 버전)
    mapping = {
        # 모음
        "a": "아",
        "i": "이",
        "u": "우",
        "e": "에",
        "o": "오",
        "ya": "야",
        "yu": "유",
        "yo": "요",
        # 자음+모음
        "ka": "카",
        "ki": "키",
        "ku": "쿠",
        "ke": "케",
        "ko": "코",
        "ga": "가",
        "gi": "기",
        "gu": "구",
        "ge": "게",
        "go": "고",
        "sa": "사",
        "shi": "시",
        "su": "스",
        "se": "세",
        "so": "소",
        "za": "자",
        "zi": "지",
        "zu": "즈",
        "ze": "제",
        "zo": "조",
        "ta": "타",
        "chi": "치",
        "tsu": "츠",
        "te": "테",
        "to": "토",
        "da": "다",
        "di": "디",
        "du": "두",
        "de": "데",
        "do": "도",
        "na": "나",
        "ni": "니",
        "nu": "누",
        "ne": "네",
        "no": "노",
        "ha": "하",
        "hi": "히",
        "fu": "후",
        "he": "헤",
        "ho": "호",
        "ba": "바",
        "bi": "비",
        "bu": "부",
        "be": "베",
        "bo": "보",
        "pa": "파",
        "pi": "피",
        "pu": "푸",
        "pe": "페",
        "po": "포",
        "ma": "마",
        "mi": "미",
        "mu": "무",
        "me": "메",
        "mo": "모",
        "ra": "라",
        "ri": "리",
        "ru": "루",
        "re": "레",
        "ro": "로",
        "wa": "와",
        "wi": "위",
        "we": "웨",
        "wo": "워",
        # 추가된 패턴
        "ji": "지",
        "ja": "자",
        "ju": "주",
        "jo": "조",
        "tsa": "차",
        "tsi": "치",
        "tse": "체",
        "tso": "초",
        "che": "체",
        "chu": "추",
        "cho": "초",
        "cha": "차",
        "she": "셰",
        "shu": "슈",
        "sho": "쇼",
        "sha": "샤",
        "je": "제",
        "si": "시",
        # 요음
        "kya": "캬",
        "kyu": "큐",
        "kyo": "쿄",
        "kye": "켸",
        "gya": "갸",
        "gyu": "규",
        "gyo": "교",
        "gye": "계",
        "sha": "샤",
        "shu": "슈",
        "sho": "쇼",
        "she": "셰",
        "ja": "자",
        "ju": "주",
        "jo": "조",
        "je": "제",
        "cha": "차",
        "chu": "추",
        "cho": "초",
        "che": "체",
        "nya": "냐",
        "nyu": "뉴",
        "nyo": "뇨",
        "nye": "녜",
        "hya": "햐",
        "hyu": "휴",
        "hyo": "효",
        "hye": "혜",
        "bya": "뱌",
        "byu": "뷰",
        "byo": "뵤",
        "bye": "볘",
        "pya": "퍄",
        "pyu": "퓨",
        "pyo": "표",
        "pye": "폐",
        "mya": "먀",
        "myu": "뮤",
        "myo": "묘",
        "mye": "며",
        "rya": "랴",
        "ryu": "류",
        "ryo": "료",
        "rye": "례",
        # 특수 자음
        "ts": "츠",
        "ch": "치",
        "sh": "시",
        "th": "스",
        # 촉음
        "kka": "까",
        "kki": "끼",
        "kku": "꾸",
        "kke": "께",
        "kko": "꼬",
        "ssa": "싸",
        "sshi": "씨",
        "ssu": "쓰",
        "sse": "쎄",
        "sso": "쏘",
        "tta": "따",
        "cchi": "찌",
        "ttsu": "쯔",
        "tte": "떼",
        "tto": "또",
        "ppa": "빠",
        "ppi": "삐",
        "ppu": "뿌",
        "ppe": "뻬",
        "ppo": "뽀",
        # 특수 발음
        "n": "은",
        "N": "ㄴ",  # 받침으로 처리할 n 발음 (N으로 표시)
    }

    # 우선순위가 높은 패턴 목록
    priority_patterns = [
        "sha",
        "shu",
        "sho",
        "she",
        "cha",
        "chu",
        "cho",
        "che",
        "kya",
        "kyu",
        "kyo",
        "kye",
        "tsu",
        "ttsu",
        "shi",
        "chi",
    ]

    # 우선순위 패턴 먼저 처리
    for pattern in priority_patterns:
        if pattern in romaji and pattern in mapping:
            romaji = romaji.replace(pattern, f"__{mapping[pattern]}__")

    # __ 로 감싸진 부분을 다시 원래대로 변환
    romaji = re.sub(r"__(.+?)__", r"\1", romaji)

    # 나머지 패턴 처리 (3글자, 2글자, 1글자 순)
    result = []
    i = 0
    while i < len(romaji):
        if i + 3 <= len(romaji) and romaji[i : i + 3] in mapping:
            result.append(mapping[romaji[i : i + 3]])
            i += 3
        elif i + 2 <= len(romaji) and romaji[i : i + 2] in mapping:
            result.append(mapping[romaji[i : i + 2]])
            i += 2
        elif i + 1 <= len(romaji) and romaji[i : i + 1] in mapping:
            result.append(mapping[romaji[i : i + 1]])
            i += 1
        else:
            # 맵핑에 없는 문자는 그대로 추가
            result.append(romaji[i])
            i += 1

    # 결과 문자열에서 알파벳 제거 (최종 정리)
    korean_text = "".join(result)
    korean_text = re.sub(r"[a-zA-Z]", "", korean_text)

    # 분리된 받침을 앞의 음절과 합치는 처리
    # 1. 정규 표현식으로 '자모음+받침' 패턴 찾기
    def combine_jamo(match):
        char = match.group(1)
        batchim = match.group(2)

        # 완성형 한글 원리: (초성 인덱스 * 588) + (중성 인덱스 * 28) + 종성 인덱스 + 44032
        if "가" <= char <= "힣":
            # 현재 글자의 유니코드 값
            char_code = ord(char)
            # 초성과 중성 정보 (종성 없음)
            base = (char_code - 44032) // 28 * 28 + 44032

            # 받침 변환
            batchim_idx = 0
            if batchim == "ㄱ":
                batchim_idx = 1
            elif batchim == "ㄴ":
                batchim_idx = 4
            elif batchim == "ㄷ":
                batchim_idx = 7
            elif batchim == "ㄹ":
                batchim_idx = 8
            elif batchim == "ㅁ":
                batchim_idx = 16
            elif batchim == "ㅂ":
                batchim_idx = 17
            elif batchim == "ㅅ":
                batchim_idx = 19
            elif batchim == "ㅇ":
                batchim_idx = 21
            elif batchim == "ㅈ":
                batchim_idx = 22
            elif batchim == "ㅊ":
                batchim_idx = 23
            elif batchim == "ㅋ":
                batchim_idx = 24
            elif batchim == "ㅌ":
                batchim_idx = 25
            elif batchim == "ㅍ":
                batchim_idx = 26
            elif batchim == "ㅎ":
                batchim_idx = 27

            # 새 문자 생성
            return chr(base + batchim_idx)
        return match.group(0)

    # 모든 가능한 받침에 대해 패턴 적용
    for jamo in [
        "ㄱ",
        "ㄴ",
        "ㄷ",
        "ㄹ",
        "ㅁ",
        "ㅂ",
        "ㅅ",
        "ㅇ",
        "ㅈ",
        "ㅊ",
        "ㅋ",
        "ㅌ",
        "ㅍ",
        "ㅎ",
    ]:
        korean_text = re.sub(f"([가-힣])({jamo})", combine_jamo, korean_text)

    return korean_text


def extract_japanese_pronunciation(text):
    """
    텍스트에서 일본어를 감지하고 로마자와 한국어 발음으로 변환합니다.

    Args:
        text (str): 변환할 텍스트

    Returns:
        tuple or None: (원본 텍스트, 로마자, 한국어 발음) 또는 일본어가 없는 경우 None
    """
    if not text or not isinstance(text, str):
        return None

    if not has_japanese(text):
        return None

    romaji = romanize_japanese(text)
    korean_pron = korean_pronunciation_from_romaji(romaji)

    return (text, romaji, korean_pron)
