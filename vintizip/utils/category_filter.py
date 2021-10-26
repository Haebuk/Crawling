def category_filter(category_name, product_name):
    changed = False
    product_name = product_name.lower()
    category_name = category_name.lower()
    if '세트' in product_name:
        changed = True
        category = 'others'

    if not changed:
        for c in ['skirt', '스커트']:
            if c in product_name:
                category = 'skirt'
                changed = True

    if not changed:
        for c in ['코트', '아우터', '사파리', '패딩', '데님자켓', '블레이저', '집업', '후리스', '가디건', 'outer', 'outers', 'coat', 'padding', 'jacket', 'cardigan', 'fleece']:
            if c in product_name:
                category = 'outer'
                changed = True

    if not changed:
        for c in ['팬츠', '1/2 팬츠', '데님팬츠', '바지', '쇼츠', 'pants', 'bottom', 'shorts']:
            if c in product_name:
                category = 'bottom'
                changed = True
    
    if not changed:
        for c in ['드레스', 'dress', '원피스', 'onepiece']:
            if c in product_name:
                category = 'dress'
                changed = True
    
    if not changed:
        category = 'top'
        
    print('category:', category)
    return category