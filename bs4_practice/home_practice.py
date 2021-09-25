from bs4 import BeautifulSoup

with open('home.html', 'r') as html_file:
    contents = html_file.read()
    # print(contents)

    soup = BeautifulSoup(contents, 'lxml') # beautifulsoup 객체 정의
    # print(soup.prettify())

    tags = soup.find('h5') # 첫번쨰 h5 태그만 찾음
    tags = soup.find_all('h5') # 모든 h5 태그를 찾음
    # print(tags)

    # for tag in tags:
        # print(tag.text)

    course_cards = soup.find_all('div', class_='card') # class 는 built-in 키워드이므로 _를 붙여서 명시해야 함.
    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]
        print(f'{course_name} costs {course_price}')