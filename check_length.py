def check_length(filename):
    """
    json 파일의 길이 체크
    :param filename: json 파일명
    """
    import json

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"{filename} length: {len(data)}")

if __name__ == '__main__':
    check_length('릴리즘_판매중.json')
    check_length('릴리즘_전체.json')