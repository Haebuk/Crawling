def get_clothes_info(store_name, sale_price, product_name, product_category, product_gender,
 product_brand_after, product_price, product_thumbnail, product_link, is_sold_out, product_size, product_type):    
    """우리 json 형식에 맞게 포매팅하는 함수
    
    Keyword arguments:
    store_name: 사이트 이름(여기서는 프롬노웨어)
    sale_price: 세일 가(여기는 세일 상품이 없음 -> '0'으로 표기)
    Return: 딕셔너리
    """
    
    info_dict = {}
    # 위에서 값들 받아옴
    values = [product_name, store_name, product_category, product_gender, product_brand_after, product_price, sale_price, product_thumbnail, product_link, is_sold_out, product_size]
    # 우리 형식에 맞는 key 값 리스트 정의
    keys = ['name', 'storeName', 'category', 'gender', 'brand', 'originalPrice', 'salePrice', 'thumbnailUrl', 'contentUrl', 'isSoldOut', 'size']
    if product_type == '가슴': # 가슴 -> key: chest
        product_type_ = 'chest'
    else:
        product_type_ = 'waist' # 허리 -> key: waist
    for i in range(len(keys)):
        if keys[i] == 'size':
            info_dict[keys[i]] = {}
            info_dict[keys[i]][product_type_] = product_size 
        else:
            info_dict[keys[i]] = values[i]
    return info_dict