import json
from tqdm import tqdm
from utils.data_to_json import DataToJson
def transform(file_name):
    """ 데이터 타입 변경과 soldout 판별하는 함수
    
    :param file_name: 파일 이름
    :return: load_data: 데이터 타입이 변경된 전체 파일 리스트
    :return: exclude_soldout_list: 데이터 타입 변경 후 판매중인 상품만 담은 파일 리스트
    """
    data = DataToJson(file_name)
    load_data = data.load_json()
        
    exclude_soldout_list = []
    n = 0
    for i in tqdm(range(len(load_data)), desc='데이터 변환중...'):
        try:
            load_data[i]['originalPrice'] = int(load_data[i]['originalPrice'])
            load_data[i]['salePrice'] = int(load_data[i]['salePrice'])

            for key, _ in load_data[i]['size'].items():
                if key == 'chest':
                    load_data[i]['size']['chest'] = float(load_data[i]['size']['chest'])
                elif key == 'waist':
                    load_data[i]['size']['waist'] = float(load_data[i]['size']['waist'])
        except ValueError:
            continue
        if not load_data[i]['isSoldOut']:
            exclude_soldout_list.append(load_data[i])
    print(f'original data length: {len(load_data)}')
    print(f'sales data length: {len(exclude_soldout_list)}')
    return load_data, exclude_soldout_list

if __name__ == '__main__':
    total_list, exclude_soldout_list = transform('릴리즘.json')
    DataToJson('릴리즘.json').save_json(total_list)

