import os
import time
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

# 환경 변수 로드
load_dotenv()

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase 클라이언트 초기화
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_to_excel(data, filename, columns=None):
    """
    데이터를 엑셀 파일로 저장합니다.

    Args:
        data (list): 저장할 데이터 리스트
        filename (str): 저장할 파일 이름
        columns (list): 저장할 컬럼 목록. None이면 모든 컬럼 저장

    Returns:
        DataFrame: 저장된 데이터의 DataFrame
    """
    if not data:
        print("저장할 데이터가 없습니다.")
        return None

    df = pd.DataFrame(data)

    if columns:
        df = df[columns]

    df.to_excel(filename, index=False)
    print(f"{len(data)}개의 데이터를 '{filename}' 파일에 저장했습니다.")
    return df


def upload_to_supabase(data, table_name, batch_size=100, conflict_column=None):
    """
    Supabase에 데이터를 업로드합니다.

    Args:
        data (list): 업로드할 데이터 리스트
        table_name (str): 업로드할 테이블 이름
        batch_size (int): 한 번에 업로드할 배치 크기
        conflict_column (str): 충돌 검사 기준 컬럼. None이면 업서트하지 않음

    Returns:
        bool: 업로드 성공 여부
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase 연결 정보가 없습니다. .env 파일을 확인하세요.")
        return False

    if not table_name:
        print("테이블 이름이 설정되지 않았습니다.")
        return False

    success_count = 0
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        try:
            # 업서트 또는 삽입
            if conflict_column:
                response = (
                    supabase.table(table_name)
                    .upsert(batch, on_conflict=conflict_column)
                    .execute()
                )
            else:
                response = supabase.table(table_name).insert(batch).execute()

            # 응답 확인
            if hasattr(response, "error") and response.error:
                print(f"업로드 실패 (배치 {i//batch_size + 1}): {response.error}")
                return False

            success_count += len(batch)
            print(f"업로드 진행 중: {success_count}/{len(data)} 완료")

            # 요청 간 짧은 대기 시간 추가
            time.sleep(0.5)

        except Exception as e:
            print(f"업로드 중 오류 발생: {str(e)}")
            return False

    return True


def filter_data_fields(data, fields):
    """
    데이터에서 지정한 필드만 추출합니다.

    Args:
        data (list): 필터링할 데이터 리스트
        fields (list): 추출할 필드 목록

    Returns:
        list: 필터링된 데이터 리스트
    """
    filtered_data = []
    for item in data:
        filtered_item = {field: item.get(field) for field in fields if field in item}
        filtered_data.append(filtered_item)

    return filtered_data


def calculate_elapsed_time(start_time, end_time=None):
    """
    경과 시간을 계산합니다.

    Args:
        start_time (float): 시작 시간
        end_time (float): 종료 시간. None이면 현재 시간

    Returns:
        float: 경과 시간 (초)
    """
    if end_time is None:
        end_time = time.time()

    return end_time - start_time
