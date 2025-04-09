"""
데이터 저장 및 업로드 관련 유틸리티 함수
"""

from utils import (
    save_to_excel,
    upload_to_supabase,
    filter_data_fields,
)


def save_and_upload_results(
    success_results, output_file, table_name, data_fields, conflict_column="number"
):
    """
    성공한 크롤링 결과를 저장하고 업로드합니다.

    Args:
        success_results (list): 성공한 크롤링 결과 리스트
        output_file (str): 저장할 엑셀 파일 이름
        table_name (str): 업로드할 Supabase 테이블 이름
        data_fields (list): 데이터 필드 목록
        conflict_column (str): 충돌 컬럼 이름 (기본값: "number")

    Returns:
        bool: 저장 및 업로드 성공 여부
    """
    # 성공한 결과가 없으면 종료
    if not success_results:
        print("크롤링에 성공한 노래 정보가 없습니다.")
        return False

    # 엑셀 파일로 저장
    save_to_excel(success_results, output_file, data_fields)

    # Supabase에 업로드
    print("\nSupabase에 데이터 업로드 중...")
    upload_data = filter_data_fields(success_results, data_fields)
    upload_success = upload_to_supabase(
        upload_data, table_name, conflict_column=conflict_column, update_mode="upsert"
    )

    if upload_success:
        print(
            f"Supabase '{table_name}' 테이블에 {len(upload_data)}개의 노래 정보 업로드 완료!"
        )
        return True
    else:
        print("Supabase 업로드에 실패했습니다.")
        return False
