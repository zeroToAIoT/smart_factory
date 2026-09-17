# file name : vision_defect_check.py
# 탐지된 객체 이름을 추출하여 특정 사물(불량품) 판별하기

from picamera2 import Picamera2
from ultralytics import YOLO
import cv2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size" : (640, 480)}))
picam2.start()

model = YOLO('yolo11n.pt')

print('=============================================')
print(' 비전 검수 로직 테스트 가동')
print(' 카메라 앞에 스마트폰을 비춰보세요.')
print('=============================================')

cv2.namedWindow('Vision Inspector', cv2.WINDOW_AUTOSIZE)

try:
    while True:
        frame = picam2.capture_array()
        results = model.predict(source=frame, conf=0.6, verbose=False)
        annotated_frame = results[0].plot()
        
        # [핵심] 화면에 인식된 사물들의 '이름'만 뽑아서 리스트로 만들기
        # 예: ['person', 'cell phone']
        detected_classes = [model.names[int(box.cls)] for box in results[0].boxes]
        
        # 판별 로직: 리스트 안에 'cell phone'이 포함되어 있는지 확인
        if 'cell phone' in detected_classes:
            # 화면 좌측 상단에 붉은색 글씨로 경고 출력
            cv2.putText(annotated_frame, 'DEFECT DETECTED!', (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            print('불량품(스마트폰) 감지!')
            
        cv2.imshow('Vision Inspector', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as err:
    print(f'오류 발생 : {err}')
finally:
    cv2.destroyAllWindows()
    picam2.stop()