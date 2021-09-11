import json
def transform_datatype_and_soldout(file_name):
    """ 데이터 타입 변경과 soldout 판별하는 함수
    
    :param file_name: 파일 이름
    :return: json_data: 데이터 타입이 변경된 전체 파일 리스트
    :return: exclude_soldout_list: 데이터 타입 변경 후 판매중인 상품만 담은 파일 리스트
    """
    with open(file_name, 'r', encoding='utf-8') as json_data:
        json_data = json.load(json_data)
        print(f'json file length: {len(json_data)}')
        for i in range(len(json_data)):
            print(json_data[i])
            if i == 2:
                break
        
    exclude_soldout_list = []
    n = 0
    for i in range(len(json_data)):
        try:
            json_data[i]['originalPrice'] = int(json_data[i]['originalPrice'])
            json_data[i]['salePrice'] = int(json_data[i]['salePrice'])

            for key, _ in json_data[i]['size'].items():
                if key == 'chest':
                    json_data[i]['size']['chest'] = float(json_data[i]['size']['chest'])
                elif key == 'waist':
                    json_data[i]['size']['waist'] = float(json_data[i]['size']['waist'])
        except ValueError:
            continue
        if not json_data[i]['isSoldOut']:
            exclude_soldout_list.append(json_data[i])
    print(f'original data length: {len(json_data)}')
    print(f'sales data length: {len(exclude_soldout_list)}')
    return json_data, exclude_soldout_list

