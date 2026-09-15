# file name: filtering_ultra.py
# 이동 평균 필터를 적용한 초음파 센서 노이즈 제거 테스트

from gpiozero import DistanceSensor
from time import sleep

# 전방 초음파 센서 객체 생성 (Echo: 12, Trig: 13)
front_ultra = DistanceSensor(echo=12, trigger=13, max_distance=1.0)

# 이동 평균 필터를 위한 설정
WINDOW_SIZE = 5       # 최근 측정값 5개를 모아서 평균을 냅니다.
history_data = []     # 측정된 데이터들을 담아둘 빈 리스트(주머니) 생성

def get_filtered_distance(raw_distance):
    """
    들어온 raw_distance를 리스트에 넣고, 최근 5개의 평균값을 반환하는 함수
    """
    # 1. 새 데이터를 리스트 맨 끝에 추가 (단위 변환: m -> cm)
    history_data.append(raw_distance * 100)
    
    # 2. 리스트의 개수가 WINDOW_SIZE(5개)를 넘어가면, 가장 앞쪽(오래된) 데이터 삭제
    if len(history_data) > WINDOW_SIZE:
        history_data.pop(0)
    
    # 3. 리스트에 담긴 데이터들의 합을 개수로 나누어 평균(Average) 계산
    average_distance = sum(history_data) / len(history_data)
    
    return average_distance

print('=============================================')
print(' 초음파 센서 필터링 테스트 시작 (Ctrl+C 종료)')
print('=============================================')

try:
    while True:
        # 센서에서 거리를 한 번 읽어옴 (Raw 데이터)
        raw_val = front_ultra.distance
        
        # 필터 함수를 거쳐 부드러워진 평균 거리를 얻어옴
        filtered_val = get_filtered_distance(raw_val)
        
        # 원본 데이터와 필터링된 데이터를 나란히 출력하여 비교해 봅니다.
        # \r을 사용하여 화면이 아래로 내려가지 않고 한 줄에서 계속 갱신되게 합니다.
        print(f'[원본] {raw_val*100:5.1f}cm | [필터 적용] {filtered_val:5.1f}cm', end='\r')
        
        sleep(0.1) # 0.1초마다 측정

except KeyboardInterrupt:
    print('\n테스트가 종료되었습니다.')