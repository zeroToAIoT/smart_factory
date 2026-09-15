# file name: test_camera_stream.py
# Picamera2와 OpenCV를 활용한 실시간 영상 스트리밍

from picamera2 import Picamera2
import cv2
from time import sleep

# 1. Picamera2 객체 생성 및 초기화
picam2 = Picamera2()

# 2. 카메라 해상도 및 포맷 설정
# 스마트 팩토리 실시간 비전 처리는 연산 속도가 생명이므로, 
# 해상도를 640x480으로 낮춰서 설정합니다. (FHD 1080p는 연산이 느려짐)
config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(config)

# 3. 카메라 가동 시작
picam2.start()
print('=============================================')
print(' AI-Rover 시신경 가동 완료! (스트리밍 시작)')
print(' 비디오 창을 선택한 후 "q" 키를 누르면 종료됩니다.')
print('=============================================')

# 영상 출력을 위한 창 생성
cv2.namedWindow("AI-Rover Vision", cv2.WINDOW_AUTOSIZE)

try:
    while True:
        # 4. 카메라로부터 현재 프레임(한 장의 사진)을 넘파이 배열(Array) 형태로 캡처
        # 이 frame 변수 안에 수십만 개의 픽셀(색상 데이터)이 숫자로 담겨 있습니다.
        frame = picam2.capture_array()
        
        # 5. OpenCV를 이용해 화면에 프레임 출력
        cv2.imshow("AI-Rover Vision", frame)
        
        # 6. 종료 조건: 1ms 동안 키보드 입력을 대기하며, 'q' 키가 눌리면 루프 탈출
        # (주의: VNC 환경에서 비디오 창을 마우스로 클릭하여 활성화한 상태에서 눌러야 함)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("사용자에 의해 영상 스트리밍을 종료합니다.")
            break

except Exception as e:
    print(f"카메라 스트리밍 중 오류 발생: {e}")

finally:
    # 7. 하드웨어 자원 안전 반환
    cv2.destroyAllWindows() # 열려있는 모든 OpenCV 창 닫기
    picam2.stop()           # 카메라 렌즈 닫기
    print("카메라 자원이 안전하게 반환되었습니다.")