# file name : flask_fpv_camera.py
# Flask 기반 실시간 FPV 카메라 스트리밍 서버

import cv2
from flask import Flask, Response, render_template_string
from picamera2 import Picamera2

# 1. 카메라 초기화 (빠른 전송을 위해 해상도를 640x480으로 설정)
print("[System] 카메라 초기화 중...")
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# 2. Flask 서버 초기화
app = Flask(__name__)

# 3. 사용자 화면(HTML) 구성
# <img> 태그의 src(출처)를 일반 이미지 파일이 아닌 '/video_feed' 주소로 연결합니다.
HTML_VIDEO = """
<!DOCTYPE html>
<html>
<head>
    <title>AGV FPV Camera</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { text-align: center; background-color: #2c3e50; color: white; margin-top: 20px; font-family: sans-serif; }
        img { width: 90%; max-width: 640px; border: 5px solid #34495e; border-radius: 10px; }
        .recording { color: #e74c3c; font-weight: bold; animation: blink 1s step-start 0s infinite; }
        @keyframes blink { 50% { opacity: 0.0; } }
    </style>
</head>
<body>
    <h2>🎥 AGV 1인칭 관제 화면</h2>
    <p class="recording">● LIVE STREAMING</p>
    
    <!-- 이 이미지 태그가 파이썬이 보내주는 영상을 끊임없이 받아옵니다 -->
    <img src="/video_feed" alt="Camera Video Stream">
</body>
</html>
"""

# 4. 카메라 프레임 생성 엔진 (플립북 제작소)
def generate_frames():
    """카메라가 찍은 사진을 JPEG로 압축하여 웹 브라우저로 끊임없이 밀어내는(yield) 함수"""
    while True:
        # 카메라에서 한 장면(Frame) 찰칵!
        frame = picam2.capture_array()
        
        # 이미지를 전송하기 쉬운 JPEG 포맷으로 압축
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # MJPEG 포맷 규격에 맞게 포장하여 브라우저로 전송 (yield: 끊기지 않고 계속 보냄)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# 5. 접속 라우팅
@app.route('/')
def index():
    """스마트폰 접속 시 HTML 화면 제공"""
    return render_template_string(HTML_VIDEO)

@app.route('/video_feed')
def video_feed():
    """HTML의 <img> 태그가 영상 데이터를 달라고 요청하는 주소"""
    # 일반 텍스트(Response)가 아닌, 계속해서 이어지는 다중 파트(multipart) 데이터임을 명시
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 6. 서버 가동
if __name__ == '__main__':
    print("=============================================")
    print(" 🎥 FPV 영상 스트리밍 서버가 가동되었습니다.")
    print(" 스마트폰 주소창에 아래 주소를 입력하세요.")
    print(" 👉 http://자신의IP주소:5000")
    print("=============================================")
    
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        picam2.stop()
        print("카메라를 안전하게 종료했습니다.")