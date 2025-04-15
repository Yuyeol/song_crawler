def extract_chosung(text):
    if not text or not isinstance(text, str):
        return ""

    result = []

    # 한글 유니코드 범위: AC00-D7A3
    # 초성 배열
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
        # 한글인 경우
        if "가" <= char <= "힣":
            # 한글 유니코드에서 초성 인덱스 계산
            char_code = ord(char) - ord("가")
            chosung_index = char_code // (21 * 28)
            result.append(CHOSUNG[chosung_index])
        # 영어인 경우 소문자로 변환
        elif "A" <= char <= "Z" or "a" <= char <= "z":
            result.append(char.lower())
        # 그 외 문자는 그대로 추가
        else:
            result.append(char)

    return "".join(result)


def add_chosung_fields(data):
    if "title" in data and data["title"] and data["title"] != "정보 없음":
        data["title_chosung"] = extract_chosung(data["title"])

    if "singer" in data and data["singer"] and data["singer"] != "정보 없음":
        data["singer_chosung"] = extract_chosung(data["singer"])

    return data
