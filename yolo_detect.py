# file name : agv_yolo_pretrained.py
# 사전 학습된 YOLO 모델을 활용한 실시간 객체 탐지

from picamera2 import Picamera2
from ultralytics import YOLO
import cv2

# 1. Picamera2 초기화 및 스트리밍 시작
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size" : (640, 480)})
picam2.configure(config)
picam2.start()

print('=============================================')
print(' AGV 인공지능 시력 가동 준비 중...')
print(' (최초 실행 시 yolo11n.pt 다운로드로 수 초 소요)')
print('=============================================')

# 2. 인공지능 뇌 이식 : 사전 학습된 모델 자동 다운로드 및 불러오기
# 경로에 파일이 없으면 ultralytics 서버에서 자동으로 받아옵니다.
model = YOLO('yolo11n.pt')

cv2.namedWindow("AGV AI Vision", cv2.WINDOW_AUTOSIZE)

try:
    while True:
        # 3. 카메라에서 프레임 읽기
        frame = picam2.capture_array()
        
        # 4. YOLO 모델에 프레임을 전달하여 사물 탐지 수행
        # conf=0.5 : 인공지능이 50% 이상 확신하는 사물만 표시합니다.
        # verbose=False : 터미널에 출력되는 복잡한 연산 과정을 숨깁니다.
        results = model.predict(source=frame, conf=0.5, verbose=False)
        
        # 5. 분석 결과(바운딩 박스, 사물 이름, 확률)가 덧그려진 이미지 추출
        annotated_frame = results[0].plot()
        
        # 6. 화면 출력
        cv2.imshow("AGV AI Vision", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n인공지능 비전 테스트를 종료합니다.")
            break

except Exception as e:
    print(f"오류 발생 : {e}")

finally:
    # 7. 자원 반환
    cv2.destroyAllWindows()
    picam2.stop()