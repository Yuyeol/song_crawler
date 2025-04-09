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
