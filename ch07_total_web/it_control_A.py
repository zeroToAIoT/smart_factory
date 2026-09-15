# file name : it_control_A.py
# 관제(IT) 파트 : 마스터 대시보드 (영상 스트리밍 + 데이터 수신 + 원격 제어 + AEB)

from flask import Flask, Response, request, jsonify, render_template_string
import cv2
from picamera2 import Picamera2
from gpiozero import Motor, DistanceSensor

# 1. 조원 B로부터 받을 데이터를 저장할 전역 변수
factory_status = {
    "temperature": 0.0,
    "humidity": 0.0,
    "defect_count": 0
}

# 2. 하드웨어 초기화 (카메라, 모터, 초음파 센서)
picam2 = Picamera2()
# 스트리밍 딜레이 방지를 위해 해상도를 낮춤
picam2.configure(picam2.create_preview_configuration(main={"size": (320, 240)}))
picam2.start()

motor1 = Motor(26, 19); motor2 = Motor(27, 22)
motor3 = Motor(20, 21); motor4 = Motor(24, 23)

sensor = DistanceSensor(echo=12, trigger=13, threshold_distance=0.2)
obstacle_detected = False # 장애물 감지 상태 변수

def stop_agv():
    global obstacle_detected
    obstacle_detected = True
    motor1.stop(); motor2.stop(); motor3.stop(); motor4.stop()
    print('[AEB 작동] 전방 장애물 감지! 강제 제동합니다.')

def clear_agv():
    global obstacle_detected
    obstacle_detected = False
    print('[안전 확보] 장애물이 사라졌습니다. 이동 가능합니다.')

# 이벤트 구동 방식: 초음파 센서가 거리를 감지하면 자동으로 함수 실행
sensor.when_in_range = stop_agv
sensor.when_out_of_range = clear_agv

# 3. Flask 웹 서버 및 사용자 UI(HTML) 설정
app = Flask(__name__)

HTML_MASTER = """
<!DOCTYPE html>
<html>
<head>
    <title>마이크로 스마트 팩토리 마스터</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #f4f7f6; text-align: center; margin: 0; padding: 10px;}
        h2 { color: #2c3e50; margin-bottom: 5px;}
        .card { background: white; margin: 10px auto; padding: 10px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 400px; }
        .data-text { font-size: 20px; font-weight: bold; color: #e74c3c; }
        img { width: 100%; border-radius: 5px; }
        .btn { width: 70px; height: 70px; font-size: 24px; margin: 5px; border-radius: 15px; background-color: #3498db; color: white; border: none; font-weight: bold;}
        .btn:active { background-color: #2980b9; }
        .btn-stop { background-color: #95a5a6; }
        table { margin: 0 auto; }
    </style>
    <script>
        // 1. 조원 B의 데이터를 1초마다 몰래 가져오는 AJAX 통신
        setInterval(() => {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temp').innerText = data.temperature.toFixed(1) + ' °C';
                    document.getElementById('humid').innerText = data.humidity.toFixed(1) + ' %';
                    document.getElementById('defect').innerText = data.defect_count + ' 개';
                });
        }, 1000);

        // 2. 조이스틱 버튼 신호를 서버로 보내는 함수
        function sendCmd(cmd) { fetch('/move/' + cmd); }
    </script>
</head>
<body>
    <h2>🏭 스마트 팩토리 통합 시스템 마스터 대시보드</h2>
    
    <!-- 첫 번째 칸: 조원 B의 현장 데이터 모니터링 -->
    <div class="card">
        <p>온도: <span id="temp" class="data-text">0.0 °C</span> | 습도: <span id="humid" class="data-text">0.0 %</span></p>
        <p>🚨 누적 불량품: <span id="defect" class="data-text">0 개</span></p>
    </div>

    <!-- 두 번째 칸: 로봇 FPV 영상 스트리밍 -->
    <div class="card">
        <img src="/video_feed" alt="Video Stream">
    </div>

    <!-- 세 번째 칸: AGV 조이스틱 -->
    <div class="card">
        <table>
            <tr>
                <td></td>
                <td><button class="btn" onmousedown="sendCmd('forward')" onmouseup="sendCmd('stop')" ontouchstart="sendCmd('forward')" ontouchend="sendCmd('stop')">▲</button></td>
                <td></td>
            </tr>
            <tr>
                <td><button class="btn" onmousedown="sendCmd('left')" onmouseup="sendCmd('stop')" ontouchstart="sendCmd('left')" ontouchend="sendCmd('stop')">◀</button></td>
                <td><button class="btn btn-stop" onclick="sendCmd('stop')">■</button></td>
                <td><button class="btn" onmousedown="sendCmd('right')" onmouseup="sendCmd('stop')" ontouchstart="sendCmd('right')" ontouchend="sendCmd('stop')">▶</button></td>
            </tr>
            <tr>
                <td></td>
                <td><button class="btn" onmousedown="sendCmd('backward')" onmouseup="sendCmd('stop')" ontouchstart="sendCmd('backward')" ontouchend="sendCmd('stop')">▼</button></td>
                <td></td>
            </tr>
        </table>
    </div>
</body>
</html>
"""

# 4. Flask 라우팅 설정
@app.route('/')
def index():
    return render_template_string(HTML_MASTER)

# --- [영상 스트리밍] ---
def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --- [데이터 송수신 API] ---
@app.route('/api/update', methods=['POST'])
def update_data():
    """조원 B가 쏘아 보내는 데이터를 받음"""
    data = request.get_json()
    factory_status.update(data)
    print(f'[데이터 수신] 불량품 누적: {data['defect_count']}개')
    return jsonify({"status": "success"})

@app.route('/api/status', methods=['GET'])
def get_status():
    """스마트폰 화면을 업데이트하기 위해 데이터를 내어줌"""
    return jsonify(factory_status)

# --- [AGV 조종 및 AEB 개입 로직] ---
@app.route('/move/<direction>')
def move_agv(direction):
    if direction == 'stop':
        motor1.stop(); motor2.stop(); motor3.stop(); motor4.stop()
    elif obstacle_detected and direction == 'forward':
        # [안전 로직] 장애물이 감지되었을 때는 전진 명령을 무시함!
        print('장애물이 있어 전진할 수 없습니다!')
    else:
        if direction == 'forward':
            motor1.forward(); motor2.forward(); motor3.forward(); motor4.forward()
        elif direction == 'backward':
            motor1.backward(); motor2.backward(); motor3.backward(); motor4.backward()
        elif direction == 'left':
            motor1.backward(); motor2.forward(); motor3.backward(); motor4.forward()
        elif direction == 'right':
            motor1.forward(); motor2.backward(); motor3.forward(); motor4.backward()
            
    return "OK"

# 5. 서버 가동
if __name__ == '__main__':
    print("=============================================")
    print(" 🚀 스마트 팩토리 통합 시스템 서버가 열렸습니다.")
    print(" 👉 접속 주소 : http://자신의IP주소:5000")
    print("=============================================")
    app.run(host='0.0.0.0', port=5000)