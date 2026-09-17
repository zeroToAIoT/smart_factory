# file name : agv_yolo_flask.py
# 사전 학습된 YOLO 탐지 결과를 Flask로 실시간 웹 스트리밍 (SSH 환경용)
# 브라우저에서 http://라즈베리파이IP:5000 으로 접속하여 실시간 AI 탐지 영상을 확인합니다.

import cv2
from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
from ultralytics import YOLO

# 1. 카메라 초기화 (빠른 전송을 위해 해상도를 640x480으로 설정)
print("[System] 카메라 초기화 중...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# 2. 인공지능 뇌 이식 : 사전 학습된 모델 자동 다운로드 및 불러오기
# 경로에 파일이 없으면 ultralytics 서버에서 자동으로 받아옵니다.
print("[System] YOLO 모델 로딩 중... (최초 실행 시 yolo11n.pt 다운로드로 수 초 소요)")
model = YOLO('yolo11n.pt')

# 3. Flask 서버 초기화
app = Flask(__name__)

# 4. 사용자 화면(HTML) 구성
# <img> 태그의 src(출처)를 일반 이미지 파일이 아닌 '/video_feed' 주소로 연결합니다.
HTML_VIDEO = """
<!DOCTYPE html>
<html>
<head>
    <title>AGV AI Vision</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { text-align: center; background-color: #2c3e50; color: white; margin-top: 20px; font-family: sans-serif; }
        img { width: 90%; max-width: 640px; border: 5px solid #34495e; border-radius: 10px; }
        .recording { color: #e74c3c; font-weight: bold; animation: blink 1s step-start 0s infinite; }
        @keyframes blink { 50% { opacity: 0.0; } }
    </style>
</head>
<body>
    <h2>🤖 AGV 인공지능 비전 관제 화면</h2>
    <p class="recording">● LIVE AI DETECTION</p>

    <!-- 이 이미지 태그가 파이썬이 보내주는 AI 탐지 영상을 끊임없이 받아옵니다 -->
    <img src="/video_feed" alt="AI Video Stream">
</body>
</html>
"""

# 5. 카메라 프레임 생성 엔진 : 캡처 -> YOLO 추론 -> 결과 그리기 -> JPEG 전송
def generate_frames():
    """카메라 프레임에 YOLO 탐지 결과를 그린 뒤, JPEG로 압축하여 브라우저로 끊임없이 밀어내는(yield) 함수"""
    while True:
        # 카메라에서 한 장면(Frame) 찰칵!
        frame = picam2.capture_array()

        # YOLO 모델에 프레임을 전달하여 사물 탐지 수행
        # conf=0.5 : 50% 이상 확신하는 사물만 표시 / verbose=False : 연산 로그 숨김
        results = model.predict(source=frame, conf=0.5, verbose=False)

        # 분석 결과(바운딩 박스, 사물 이름, 확률)가 덧그려진 이미지 추출
        annotated_frame = results[0].plot()

        # 이미지를 전송하기 쉬운 JPEG 포맷으로 압축
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        # MJPEG 포맷 규격에 맞게 포장하여 브라우저로 전송 (yield: 끊기지 않고 계속 보냄)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 6. 접속 라우팅
@app.route('/')
def index():
    """접속 시 HTML 화면 제공"""
    return render_template_string(HTML_VIDEO)

@app.route('/video_feed')
def video_feed():
    """HTML의 <img> 태그가 영상 데이터를 달라고 요청하는 주소"""
    # 일반 텍스트(Response)가 아닌, 계속해서 이어지는 다중 파트(multipart) 데이터임을 명시
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 7. 서버 가동
if __name__ == '__main__':
    print("=============================================")
    print(" 🤖 AGV YOLO 스트리밍 서버가 가동되었습니다.")
    print(" 브라우저 주소창에 아래 주소를 입력하세요.")
    print(" 👉 http://자신의IP주소:5000")
    print(" (IP 확인 명령어: hostname -I)")
    print("=============================================")

    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        picam2.stop()
        print("카메라를 안전하게 종료했습니다.")
