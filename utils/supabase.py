import os
import time
from dotenv import load_dotenv
from supabase import create_client

# 환경 변수 로드
load_dotenv()

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase 클라이언트 초기화
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_to_supabase(
    data, table_name, batch_size=100, conflict_column=None, update_mode="insert"
):
    """
    Supabase에 데이터를 업로드합니다.

    Args:
        data (list): 업로드할 데이터 리스트
        table_name (str): 업로드할 테이블 이름
        batch_size (int): 한 번에 업로드할 배치 크기
        conflict_column (str): 충돌 검사 기준 컬럼. 'upsert' 모드에서 사용
        update_mode (str): 업데이트 방식
            - "insert": 기본값. 새 데이터 삽입
            - "upsert": conflict_column을 기준으로 업서트
            - "truncate": 테이블을 비우고 새 데이터 삽입

    Returns:
        bool: 업로드 성공 여부
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase 연결 정보가 없습니다. .env 파일을 확인하세요.")
        return False

    if not table_name:
        print("테이블 이름이 설정되지 않았습니다.")
        return False

    # 업데이트 모드 검증
    valid_modes = ["insert", "upsert", "truncate"]
    if update_mode not in valid_modes:
        print(f"유효하지 않은 업데이트 모드입니다. {valid_modes} 중 하나를 사용하세요.")
        return False

    # upsert 모드에서 conflict_column 검증
    if update_mode == "upsert" and not conflict_column:
        print("upsert 모드에서는 conflict_column이 필요합니다.")
        return False

    # truncate 모드에서 테이블 비우기
    if update_mode == "truncate":
        try:
            # 항상 true인 조건으로 모든 레코드 삭제
            supabase.table(table_name).delete().neq("id", -99999).execute()
            print(f"'{table_name}' 테이블의 기존 데이터를 삭제했습니다.")
        except Exception as e:
            print(f"테이블 데이터 삭제 중 오류 발생: {str(e)}")
            return False

    success_count = 0
    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        try:
            # 업서트 또는 삽입
            if update_mode == "upsert":
                response = (
                    supabase.table(table_name)
                    .upsert(batch, on_conflict=conflict_column)
                    .execute()
                )
            else:  # insert or truncate
                response = supabase.table(table_name).insert(batch).execute()
            if hasattr(response, "error") and response.error:
                print(f"업로드 실패 (배치 {i//batch_size + 1}): {response.error}")
                return False

            success_count += len(batch)
            print(f"업로드 진행 중: {success_count}/{len(data)} 완료")

            time.sleep(0.5)

        except Exception as e:
            print(f"업로드 중 오류 발생: {str(e)}")
            return False

    return True
