import time
from datetime import datetime

def time_check(store_name, start, end):
    """크롤링 소요시간 체크 파일

    Args:
        store_name (str): 사이트 명
        start (int): 시작 시간
        end (int): 종료 시간
    """
    delta = end - start
    start = datetime.fromtimestamp(start)
    end = datetime.fromtimestamp(end)
    duration = end - start

    print('start:', start)
    print('end:', end)
    print('duration:', duration)

    with open(f'{store_name}_log.txt', 'w', encoding='utf-8') as f:
        f.write(f'start time: {start}\n')
        f.write(f'end time: {end}\n')
        f.write(f'duration: {duration}\n')
        f.write(f'total second: {int(delta)} sec')

if __name__ == '__main__':
    time_check('test', time.time(), time.time() + 1)