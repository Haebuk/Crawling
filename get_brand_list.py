def get_brand_list(keyword):
    """sumary_line: 사이트에서 그대로 가져온 브랜드명을 우리 브랜드명에 맞게 바꿔준다.
    
    Keyword arguments:
    keyword: 사이트에서 가져온 브랜드명
    Return: 변환된 브랜드명
    """
    
    import pandas as pd
    df = pd.read_csv('brand_list.csv')
    try:
        value = df.loc[
            (df['키워드1'] == keyword.lower()) |
            (df['키워드2'] == keyword.lower()) |
            (df['키워드3'] == keyword.lower()) |
            (df['키워드4'] == keyword.lower()) |
            (df['브랜드명'] == keyword.lower()),
            '브랜드명'
        ].values[0]
    except IndexError: # 우리 브랜드명에 포함이 되지 않는다면 etc
        value = 'etc'

    return value

# testing
if __name__ == '__main__':
    print(get_brand_list('카카오'))
    print(get_brand_list('게스'))
    print(get_brand_list('gu'))
    print(get_brand_list('GU'))
    print(get_brand_list("levi's"))