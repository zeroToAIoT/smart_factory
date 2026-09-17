# file name: test_video.py
# Picamera2를 활용한 5초간의 동영상 녹화

from picamera2 import Picamera2
from time import sleep

# 1. 카메라 객체 생성 및 동영상용 해상도 설정
picam2 = Picamera2()
# 사진(create_still_configuration)이 아닌 동영상(create_video_configuration) 모드를 사용합니다.
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))

# 2. 카메라 렌즈 열기
picam2.start()
print('카메라 예열 중...')
sleep(2)

# 3. 동영상 녹화 시작
file_name = "test_video.h264"
print(f'{file_name} 파일로 동영상 촬영을 시작합니다. (5초간 진행)')

# start_recording 명령으로 백그라운드에서 녹화가 시작됩니다.
picam2.start_recording(file_name)

# 4. 녹화 시간 설정 (이 sleep 시간 동안 카메라가 쉴 새 없이 프레임을 파일에 기록합니다)
sleep(5)

# 5. 녹화 종료 및 하드웨어 자원 반환
picam2.stop_recording()
print('동영상 촬영 완료 및 저장 성공!')

picam2.stop()