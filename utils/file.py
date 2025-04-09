import pandas as pd


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
