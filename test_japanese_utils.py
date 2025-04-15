#!/usr/bin/env python

"""
일본어 발음 변환 테스트 스크립트
"""

import sys
from all_songs.utils.japanese_utils import extract_japanese_pronunciation


def print_test_result(text):
    """
    텍스트를 변환하고 결과를 출력합니다.

    Args:
        text (str): 테스트할 텍스트
    """
    result = extract_japanese_pronunciation(text)

    if result:
        original, romaji, korean = result
        print(f"원본: {original}")
        print(f"로마자: {romaji}")
        print(f"한국어 발음: {korean}")
        print("-" * 50)
    else:
        print(f"'{text}'에 일본어가 포함되어 있지 않습니다.")
        print("-" * 50)


def main():
    # 순수 일본어 테스트 케이스
    test_cases = [
        # 기본 발음 테스트
        "こんにちは",  # 안녕하세요
        "ありがとう",  # 감사합니다
        "さようなら",  # 안녕히 가세요
        "おはよう",  # 좋은 아침
        "こんばんは",  # 안녕하세요(저녁)
        "すみません",  # 죄송합니다
        "いただきます",  # 잘 먹겠습니다
        "ごちそうさま",  # 잘 먹었습니다
        "はじめまして",  # 처음 뵙겠습니다
        "どうぞよろしく",  # 잘 부탁드립니다
        # 가타카나
        "アイドル",  # 아이돌
        "チェリー",  # 체리
        "ポケットモンスター",  # 포켓몬스터
        "テレビ",  # 텔레비
        "サンキュー",  # 땡큐
        "アニメ",  # 애니메
        "カラオケ",  # 가라오케
        "パソコン",  # 파소콘(컴퓨터)
        "ケーキ",  # 케이크
        "スマホ",  # 스마호(스마트폰)
        "コンビニ",  # 편의점
        "エレベーター",  # 엘리베이터
        "パーティー",  # 파티
        "インターネット",  # 인터넷
        "バイク",  # 바이크
        "ゲーム",  # 게임
        "ソフト",  # 소프트
        # 한자
        "東京",  # 도쿄
        "山本桜",  # 야마모토 사쿠라
        "小林こうき",  # 코바야시 코우키
        "世界に一つだけの花",  # 세상에 하나뿐인 꽃
        "大阪",  # 오사카
        "京都",  # 교토
        "富士山",  # 후지산
        "新幹線",  # 신칸센
        "寿司",  # 스시
        "食べ物",  # 타베모노(음식)
        "飲み物",  # 노미모노(음료)
        "日本語",  # 니혼고(일본어)
        "学校",  # 가쿠코(학교)
        "先生",  # 센세이(선생님)
        "学生",  # 가쿠세이(학생)
        "図書館",  # 토쇼칸(도서관)
        "会社",  # 카이샤(회사)
        "電車",  # 덴샤(전철)
        "自転車",  # 지텐샤(자전거)
        "天気",  # 텐키(날씨)
        "雨",  # 아메(비)
        "雪",  # 유키(눈)
        # 촉음(ッ) 테스트
        "ニッポン",  # 닛폰
        "サッカー",  # 사커
        "バッグ",  # 백
        "ロッカー",  # 로커
        "キッチン",  # 키친
        "マッチ",  # 매치
        "ガッツ",  # 갓츠
        "アップル",  # 애플
        "ベッド",  # 베드
        "コップ",  # 컵
        "チケット",  # 티켓
        "ホッケー",  # 하키
        "ハッピー",  # 해피
        "バッテリー",  # 배터리
        "ラッパ",  # 랍파(나팔)
        "シャッター",  # 셔터
        # 장음(ー) 테스트
        "コーヒー",  # 커피
        "スーパー",  # 슈퍼
        "セーター",  # 스웨터
        "ケーキ",  # 케이크
        "トースト",  # 토스트
        "カレー",  # 카레
        "ビール",  # 비루
        "カード",  # 카드
        "ノート",  # 노트
        "ボール",  # 볼
        "ジュース",  # 주스
        "シャツ",  # 셔츠
        "サービス",  # 서비스
        "ソース",  # 소스
        "スポーツ",  # 스포츠
        "ケータイ",  # 휴대폰
        "ビューティー",  # 뷰티
        "シャワー",  # 샤워
        "ドアー",  # 도어
        "カーテン",  # 커튼
        # 요음(ャュョ) 테스트
        "キャラメル",  # 캬라멜
        "キュート",  # 큐트
        "チョコレート",  # 초콜릿
        "シャワー",  # 샤워
        "ニュース",  # 뉴스
        "シャツ",  # 셔츠
        "チョーク",  # 초크
        "チャンス",  # 찬스
        "ジュース",  # 주스
        "リュック",  # 류크(배낭)
        "ミュージック",  # 뮤직
        "キャッシュ",  # 캐시
        "シャンプー",  # 샴푸
        "チャレンジ",  # 챌린지
        "ヒューマン",  # 휴먼
        "シュークリーム",  # 슈크림
        "ジョギング",  # 조깅
        "ミョウバン",  # 묘반
        # 변형 발음 테스트
        "わたしは",  # 와타시와(조사 は는 wa로 발음)
        "へや",  # 헤야
        "おとうと",  # 오토토(동생)
        "きょうと",  # 교토
        "うきよ",  # 우키요
        "これは",  # 코레와
        "それでは",  # 소레데와
        "いまは",  # 이마와
        "なにを",  # 나니오
        "いぬが",  # 이누가
        "だれの",  # 다레노
        "どこへ",  # 도코에
        # 복합 발음 테스트
        "やっぱり",  # 야빠리
        "きょうは",  # 쿄와
        "ちょっと",  # 쵸또
        "にゃんこ",  # 냥코
        "しゅっきん",  # 슛킨(출근)
        "きゅうに",  # 규니(갑자기)
        "ひゃくえん",  # 햐쿠엔(백엔)
        "びょういん",  # 뵤인(병원)
        "しゃしん",  # 샤신(사진)
        "りょこう",  # 료코(여행)
        "ぎゅうにく",  # 규니쿠(소고기)
        "にゅうがく",  # 뉴가쿠(입학)
        "みょうじ",  # 묘지(성씨)
        "ひゃっかじてん",  # 햐카지텐(백과사전)
        # 특수 발음 패턴
        "げんき",  # 겐키
        "はんのう",  # 한노
        "さんぽ",  # 산포
        "おんがく",  # 온가쿠
        "きんようび",  # 킨요비
        "しんぶん",  # 신분(신문)
        "かんたん",  # 칸탄(간단)
        "てんき",  # 텐키(날씨)
        "じんせい",  # 진세이(인생)
        "べんきょう",  # 벤쿄(공부)
        "せんせい",  # 센세이(선생님)
        "こんばん",  # 콘반(오늘 밤)
        "しんかんせん",  # 신칸센
        "せんしゅ",  # 센슈(선수)
        "てんぷら",  # 텐푸라
        # 연음 및 특수 발음 케이스
        "ありません",  # 아리마센
        "かいます",  # 카이마스(삽니다)
        "といあわせ",  # 토이아와세(문의)
        "あおい",  # 아오이(파란)
        "まあまあ",  # 마아마아(그럭저럭)
        "まいにち",  # 마이니치(매일)
        "かういん",  # 카우인(회원)
        "きいて",  # 키이테(들어)
        "しつれい",  # 시츠레이(실례)
        # 일본어 노래 제목
        "君の名は",  # 키미노나와(너의 이름은)
        "千と千尋の神隠し",  # 센과 치히로의 행방불명
        "君がくれた夏",  # 키미가쿠레타나츠(네가 준 여름)
        "夜に駆ける",  # 요루니카케루(밤을 달리다)
        "打上花火",  # 우치아게하나비(쏘아올린 불꽃)
        "恋",  # 코이(사랑)
        "前前前世",  # 젠젠젠세(전전전세)
        "炎",  # 호노오(불꽃)
        "紅蓮華",  # 구렌카(홍련)
        "残酷な天使のテーゼ",  # 잔쿠쿠나텐시노테제(잔혹한 천사의 테제)
        "天ノ弱",  # 아마노자쿠(천약자)
        "カタオモイ",  # 카타오모이(짝사랑)
        "告白",  # 코쿠하쿠(고백)
        "花に亡霊",  # 하나니보레이(꽃의 망령)
        "さくら",  # 사쿠라(벚꽃)
        "群青",  # 군죠(군청)
        "嘘つき",  # 우소츠키(거짓말쟁이)
        "愛にできることはまだあるかい",  # 아이니데키루코토와마다아루카이
        # 일본 게임 및 애니메이션 제목
        "進撃の巨人",  # 신게키노쿄진(진격의 거인)
        "鬼滅の刃",  # 키메츠노야이바(귀멸의 칼날)
        "呪術廻戦",  # 주쥬츠카이센(주술회전)
        "ファイナルファンタジー",  # 파이널판타지
        "ドラゴンクエスト",  # 드래곤퀘스트
        "ポケットモンスター",  # 포켓몬스터
        "ワンピース",  # 원피스
        "ナルト",  # 나루토
        "ドラえもん",  # 도라에몽
        "スラムダンク",  # 슬램덩크
        "ジョジョの奇妙な冒険",  # 조조의 기묘한 모험
        "転生したらスライムだった件",  # 전생했더니 슬라임이었던 건
        # 일본 지역 및 유명 장소
        "北海道",  # 홋카이도
        "本州",  # 혼슈
        "四国",  # 시코쿠
        "九州",  # 큐슈
        "沖縄",  # 오키나와
        "東京タワー",  # 도쿄타워
        "秋葉原",  # 아키하바라
        "渋谷",  # 시부야
        "新宿",  # 신주쿠
        "浅草",  # 아사쿠사
        "浅草寺",  # 아사쿠사데라(센소지)
        "横浜",  # 요코하마
        "富士山",  # 후지산
        "奈良",  # 나라
        # 일본 음식 및 요리
        "お寿司",  # 오스시
        "ラーメン",  # 라멘
        "うどん",  # 우동
        "そば",  # 소바
        "天ぷら",  # 텐푸라
        "とんかつ",  # 돈카츠
        "おにぎり",  # 오니기리
        "たこやき",  # 타코야키
        "焼肉",  # 야키니쿠
        "すき焼き",  # 스키야키
        "お好み焼き",  # 오코노미야키
        "味噌汁",  # 미소시루
        "抹茶",  # 말차
    ]

    # 커맨드 라인에서 텍스트를 받은 경우
    if len(sys.argv) > 1:
        test_text = " ".join(sys.argv[1:])
        print_test_result(test_text)
    # 샘플 테스트 케이스 사용
    else:
        print("==== 일본어 발음 변환 테스트 ====")
        print("순수 일본어 테스트 케이스를 사용합니다.")
        print("직접 테스트하려면: python test_japanese_utils.py <일본어 텍스트>\n")

        for case in test_cases:
            print_test_result(case)


if __name__ == "__main__":
    main()
