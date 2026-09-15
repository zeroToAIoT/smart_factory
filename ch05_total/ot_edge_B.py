# file name : ot_edge_B.py
# 현장(OT) 파트 : 비전 검수, 환경 모니터링 및 서버 데이터 전송

import cv2
import requests
import time
from picamera2 import Picamera2
from ultralytics import YOLO
import board
import adafruit_dht  # (수정) 구형 Adafruit_DHT 대신 최신 CircuitPython 라이브러리 사용
from RPLCD.i2c import CharLCD

# 1. 서버 주소 설정 (조원 A의 라즈베리파이 IP 주소로 반드시 변경하세요!)
SERVER_URL = 'http://192.168.137.50:5000/api/update'

# 2. 하드웨어 및 AI 초기화
print('[System] 하드웨어 및 AI 모델 초기화 중...')

# DHT11 센서 초기화 (최신 라즈베리파이 5 Bookworm 환경 적용)
dht_device = adafruit_dht.DHT11(board.D21, use_pulseio=False)

# I2C LCD 초기화
lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')
lcd.clear()
lcd.backlight_enabled = True

# 카메라 초기화
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# 사전 학습된 가벼운 YOLO nano 모델 불러오기
model = YOLO('yolo11n.pt') 
defect_count = 0           # 불량품 누적 카운트 변수

cv2.namedWindow('OT Vision Station', cv2.WINDOW_AUTOSIZE)
print('[System] 현장 엣지 노드 가동을 시작합니다.')

# 안정적인 통신을 위한 초기 온습도값 세팅
temperature = 25.0
humidity = 50.0

try:
    while True:
        # 3. 환경 데이터 읽기 (에러가 나도 프로그램이 멈추지 않도록 예외 처리)
        try:
            temp = dht_device.temperature
            hum = dht_device.humidity
            if temp is not None and hum is not None:
                temperature = temp
                humidity = hum
        except RuntimeError as error:
            # DHT11은 타이밍 이슈로 읽기 에러가 자주 발생하므로, 에러 발생 시 무시하고 넘어감
            pass

        # 4. LCD 출력 (화면 깜빡임과 밀림을 방지하기 위해 커서를 맨 앞으로 초기화)
        lcd.cursor_pos = (0, 0)
        # 이전 글자 잔상을 지우기 위해 끝에 여백을 살짝 둡니다.
        lcd.write_string(f'Temp: {temperature:.1f}C   \nHumid: {humidity:.1f}%   ')

        # 5. 카메라 프레임 캡처 및 YOLO 추론
        frame = picam2.capture_array()
        results = model.predict(source=frame, conf=0.6, verbose=False)
        annotated_frame = results[0].plot()

        # 6. 불량품 판별 로직
        detected_classes = [model.names[int(box.cls)] for box in results[0].boxes]
        
        if 'cell phone' in detected_classes:
            defect_count += 1
            cv2.putText(annotated_frame, "DEFECT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            print(f'불량품 감지! (누적: {defect_count}개)')

        # 7. 관제 서버(조원 A)로 데이터 전송 (POST 요청)
        payload = {
            "temperature": temperature,
            "humidity": humidity,
            "defect_count": defect_count
        }
        
        try:
            response = requests.post(SERVER_URL, json=payload, timeout=0.5)
        except requests.exceptions.RequestException:
            # 화면이 스크롤되지 않도록 end='\r' 처리
            print('서버와 통신 실패 (관제 서버 상태를 확인하세요)', end='\r')

        # 8. 현장 모니터(OpenCV 창) 출력
        cv2.imshow('OT Vision Station', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('\n현장 엣지 노드를 종료합니다.')
            break

except Exception as err:
    print(f'시스템 에러 : {err}')

finally:
    cv2.destroyAllWindows()
    picam2.stop()
    lcd.clear()
    dht_device.exit() # DHT 센서 자원 안전 반환