def get_brand_list(keyword):
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
    except IndexError:
        value = 'etc'

    return value

if __name__ == '__main__':
    print(get_brand_list('카카오'))
    print(get_brand_list('게스'))
    print(get_brand_list('gu'))
    print(get_brand_list('GU'))
    print(get_brand_list("levi's"))