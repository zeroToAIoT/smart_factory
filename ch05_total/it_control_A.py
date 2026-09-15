# file name : it_control_A.py
# 관제(IT) 파트 : Flask 웹 서버, AGV 자율주행(AEB) 및 실시간 스트리밍 통합

from flask import Flask, Response, request, jsonify, render_template_string
import cv2
from picamera2 import Picamera2
from gpiozero import Motor, DistanceSensor
from time import sleep

# 1. 전역 변수 : 조원 B(현장)로부터 받을 데이터를 저장할 공간
factory_status = {
    "temperature" : 0.0,
    "humidity" : 0.0,
    "defect_count" : 0
}

# 2. 하드웨어 초기화 (카메라 및 AGV 모터/센서)
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size" : (640, 480)}))
picam2.start()

motor1 = Motor(26, 19)
motor2 = Motor(27, 22)
motor3 = Motor(20, 21)
motor4 = Motor(24, 23)

front_ultra = DistanceSensor(echo=12, trigger=13, threshold_distance=0.2)

def stop_agv():
    motor1.stop(); motor2.stop(); motor3.stop(); motor4.stop()
    print('[AEB 작동] 전방 장애물 감지! AGV 정지')

def move_agv():
    motor1.forward(0.5); motor2.forward(0.5); motor3.forward(0.5); motor4.forward(0.5)
    print('[주행 재개] 안전 확보. 전진합니다.')

# 이벤트 구동 방식 연결 (웹 서버와 충돌 없이 독립적으로 작동)
front_ultra.when_in_range = stop_agv
front_ultra.when_out_of_range = move_agv

# 3. Flask 웹 서버 설정
app = Flask(__name__)

# --- [웹 대시보드 UI (HTML/JS 템플릿)] ---
# 복잡한 파일 구성 없이 1개의 파일로 실행되도록 HTML을 파이썬 안에 품었습니다.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>마이크로 스마트 팩토리 대시보드</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f4f7f6; text-align: center; }
        h1 { color: #2c3e50; }
        .dashboard { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); min-width: 300px; }
        .data-text { font-size: 24px; font-weight: bold; color: #e74c3c; }
        img { max-width: 100%; border-radius: 5px; }
    </style>
    <script>
        // 1초마다 조원 B의 최신 데이터를 가져와서 화면을 몰래(비동기로) 새로고침 합니다.
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temp').innerText = data.temperature.toFixed(1) + ' °C';
                    document.getElementById('humid').innerText = data.humidity.toFixed(1) + ' %';
                    document.getElementById('defect').innerText = data.defect_count + ' 개';
                });
        }, 1000);
    </script>
</head>
<body>
    <h1>🏭 통합 관제 대시보드</h1>
    <div class="dashboard">
        <div class="card">
            <h3>🎥 AGV 1인칭 주행 영상</h3>
            <img src="/video_feed" alt="Video Stream">
        </div>
        <div class="card">
            <h3>📊 공장 현장 (OT) 데이터 보고</h3>
            <p>현재 온도 : <span id="temp" class="data-text">0.0 °C</span></p>
            <p>현재 습도 : <span id="humid" class="data-text">0.0 %</span></p>
            <hr>
            <p>🚨 누적 불량품 : <span id="defect" class="data-text">0 개</span></p>
        </div>
    </div>
</body>
</html>
"""

# --- [Flask 라우팅 (경로 설정)] ---

@app.route('/')
def index():
    """스마트폰으로 접속 시 가장 먼저 보여지는 메인 화면(HTML)을 렌더링합니다."""
    return render_template_string(HTML_TEMPLATE)

def generate_frames():
    """카메라 영상을 스마트폰으로 끊임없이 보내주는(스트리밍) 엔진 역할"""
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        # MJPEG 포맷으로 이미지들을 하나로 묶어 송신
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """HTML의 <img> 태그가 이 주소를 호출하여 영상을 받아갑니다."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/update', methods=['POST'])
def update_data():
    """조원 B(현장)가 requests.post()로 쏘아 보낸 데이터를 받아 저장합니다."""
    data = request.get_json()
    factory_status.update(data)
    print(f"📥 [데이터 수신] 온도:{data['temperature']} / 불량:{data['defect_count']}개")
    return jsonify({"status" : "success"})

@app.route('/api/status', methods=['GET'])
def get_status():
    """스마트폰(웹 브라우저)이 1초마다 최신 데이터를 가져갈 수 있도록 제공합니다."""
    return jsonify(factory_status)

# 4. 시스템 가동 시작
if __name__ == '__main__':
    print("=============================================")
    print(" 🚀 스마트 팩토리 통합 시스템 서버 가동을 시작합니다.")
    print(" 스마트폰 웹 브라우저를 열고 아래 주소로 접속하세요.")
    print(" 👉 주소 : http://자신의IP주소:5000")
    print("=============================================")
    
    # AGV 최초 출발
    move_agv()
    
    # Flask 웹 서버 실행 (0.0.0.0 : 외부 접속 허용)
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        pass
    finally:
        stop_agv()
        picam2.stop()
        print('관제 서버를 안전하게 종료했습니다.')