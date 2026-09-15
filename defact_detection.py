# file name : defect_detection.py
# YOLOv11 커스텀 모델을 활용한 실시간 양품/불량품 판별 시스템

from picamera2 import Picamera2
from ultralytics import YOLO
import cv2

# 1. 객체 생성 및 초기화 : Picamera2 
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size" : (640, 480)})
picam2.configure(config)
picam2.start()

# 2. 인공지능 뇌 이식 : 학습된 YOLOv11 모델 불러오기
# Colab에서 학습시킨 나만의 모델 파일(best.pt)을 사용합니다.
model = YOLO('best.pt')

print('=============================================')
print(' 인공지능 비전 검수 시스템 가동')
print(' 카메라 창을 선택 후 "q"를 누르면 종료됩니다.')
print('=============================================')

cv2.namedWindow("Defect Inspector", cv2.WINDOW_AUTOSIZE)

try:
    while True:
        # 3. 실시간 프레임 캡처
        frame = picam2.capture_array()
        
        # 4. YOLOv11 모델에 프레임을 전달하여 추론 (분석) 수행
        # conf=0.6 : 확신도가 60% 이상인 객체만 탐지
        # verbose=False : 터미널 창에 출력되는 불필요한 로그 숨김
        results = model.predict(source=frame, conf=0.6, verbose=False)
        
        # 5. 분석 결과(바운딩 박스, 라벨)가 덧그려진 새로운 이미지를 추출
        # results[0].plot()은 원본 이미지 위에 탐지 결과를 시각화해 줍니다.
        annotated_frame = results[0].plot()
        
        # 6. 화면 출력 및 종료 대기
        cv2.imshow("Defect Inspector", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("비전 검수를 종료합니다.")
            break

except Exception as e:
    print(f"오류 발생 : {e}")

finally:
    # 7. 자원 반환
    cv2.destroyAllWindows()
    picam2.stop()
    print("카메라 자원이 반환되었습니다.")