# file name: test_snapshot.py
# Picamera2를 활용한 단일 사진 촬영 및 파일 저장

from picamera2 import Picamera2
from time import sleep

# 1. 카메라 객체 생성 및 사진용 해상도 자동 설정
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

# 2. 카메라 렌즈 열기 (가동)
picam2.start()
print('카메라 센서 예열 중...')

# [중요] 카메라가 켜진 직후에는 빛을 조절(자동 노출 및 화이트 밸런스)할 시간이 필요합니다.
# 이 대기 시간이 없으면 사진이 시커멓게 찍힐 수 있습니다.
sleep(2) 

# 3. 사진 촬영 및 파일로 바로 저장
file_name = "test_photo.jpg"
picam2.capture_file(file_name)
print(f'사진 촬영 완료! 현재 폴더에 {file_name} 파일이 저장되었습니다.')

# 4. 하드웨어 자원 반환 (카메라 렌즈 닫기)
picam2.stop()