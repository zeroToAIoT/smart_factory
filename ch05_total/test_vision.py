# file name : test_vision_inspector.py
# YOLOv11 모델을 활용한 특정 객체(불량품) 감지 및 카운팅

import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

# 1. 카메라 초기화 (연산 속도를 위해 640x480 해상도 사용)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# 2. 사전 학습된 인공지능 두뇌 불러오기
model = YOLO('yolo11n.pt') 

defect_count = 0  # 불량품을 발견할 때마다 1씩 증가할 변수

print("=============================================")
print(" 비전 검수 시스템 단독 테스트 시작")
print(" 카메라 렌즈 앞에 '스마트폰'을 보여주세요.")
print("=============================================")

cv2.namedWindow("Vision Inspector", cv2.WINDOW_AUTOSIZE)

try:
    while True:
        # 3. 실시간 프레임 캡처 및 AI 추론
        frame = picam2.capture_array()
        
        # conf=0.6 : 60% 이상 확신할 때만 인식하도록 기준을 높여 오작동 방지
        results = model.predict(source=frame, conf=0.6, verbose=False)
        
        # 4. 분석 결과(바운딩 박스)가 덧그려진 도화지(이미지) 생성
        annotated_frame = results[0].plot()

        # 5. [핵심] 화면에 인식된 사물들의 '이름'만 뽑아서 리스트로 만들기
        # 예: ['person', 'cell phone', 'bottle']
        detected_classes = [model.names[int(box.cls)] for box in results[0].boxes]
        
        # 6. 불량품 판별 로직 (스마트폰을 불량품으로 가정)
        if 'cell phone' in detected_classes:
            defect_count += 1
            
            # 빨간색 굵은 글씨로 화면에 경고 문구 출력
            cv2.putText(annotated_frame, "DEFECT DETECTED!", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            print(f"🚨 불량품 감지! (현재까지 누적: {defect_count}개)")

        # 7. 모니터에 최종 화면 출력
        cv2.imshow("Vision Inspector", annotated_frame)
        
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("비전 검수 테스트를 종료합니다.")
            break

except Exception as err:
    print(f"오류 발생 : {err}")

finally:
    cv2.destroyAllWindows()
    picam2.stop()