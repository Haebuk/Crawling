def category_filter(category_name, product_name):
    changed = False
    if category_name == 'OUTERS':
        if '세트' in product_name:
            category = 'others'
        else:
            category = 'outer'
        changed = True

    if not changed:
        for c in ['코트', '아우터', '사파리', '패딩', '데님자켓', '블레이저', '후드집업/후리스', '가디건']:
            if c == category_name:
                category = 'outer'
                changed = True

    if not changed:
        for c in ['팬츠', '1/2 팬츠', '데님팬츠']:
            if c == category_name:
                category = 'bottom'
                changed = True

    if not changed:
        if category_name == 'PANT':
            if '스커트' in product_name:
                category = 'skirt'
            else:
                category = 'bottom'
            changed = True
    
    if not changed:
        if category_name == '드레스':
            category = 'dress'
            changed = True

    if not changed:
        if category_name == '스포츠':
            if '팬츠' in product_name:
                category = 'bottom'
            else:
                category = 'top'
            changed = True

    if not changed:
        category = 'top'
        
    print('category:', category)
    return category