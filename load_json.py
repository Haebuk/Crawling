def load_json(filename):
    """
    json 파일 로드하는 함수

    param: filename: json 파일 이름(확장자까지 포함해야함. ex: 'filename.json')
    return: data: json 파일 내용. 리스트에 담겨있는 형태
    """
    import json
    try: # 해당 파일이 이미 존재하는 경우
        with open(filename, 'r', encoding='utf-8') as f: # 그대로 파일 로드
            data = json.load(f)
    except: # 해당 파일이 존재하지 않는 경우(처음 여는 경우)
        empty_list = []
        with open(filename, 'w', encoding='utf-8') as f: # 새로 생성한 파일에 빈 리스트 저장
            json.dump(empty_list, f, ensure_ascii=False, indent=4)
        with open(filename, 'r', encoding='utf-8') as f: # 새로 생성한 파일 열기
            data = json.load(f) 
    return data