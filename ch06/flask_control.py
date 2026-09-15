# file name : web_agv_controller.py
# Flask 기반 AGV 스마트폰 원격 제어 (Teleoperation)

from flask import Flask, render_template_string
from gpiozero import Motor

# 1. 하드웨어 세팅 : AGV 모터 핀 번호 설정
# (자신의 4장 회로도 배선에 맞게 핀 번호를 확인하세요)
motor1 = Motor(26, 19) # 좌측 전륜
motor2 = Motor(27, 22) # 우측 전륜
motor3 = Motor(20, 21) # 좌측 후륜
motor4 = Motor(24, 23) # 우측 후륜

# 주행 제어 함수 정의
def agv_forward():
    motor1.forward(); motor2.forward(); motor3.forward(); motor4.forward()

def agv_backward():
    motor1.backward(); motor2.backward(); motor3.backward(); motor4.backward()

def agv_left():
    motor1.backward(); motor2.forward(); motor3.backward(); motor4.forward()

def agv_right():
    motor1.forward(); motor2.backward(); motor3.forward(); motor4.backward()

def agv_stop():
    motor1.stop(); motor2.stop(); motor3.stop(); motor4.stop()

# 2. Flask 서버 초기화
app = Flask(__name__)

# 3. 조이스틱 화면 (HTML/CSS/JS)
# 버튼을 누르는 동안만 로봇이 움직이도록 터치(Touch)와 마우스(Mouse) 이벤트를 모두 적용했습니다.
HTML_JOYSTICK = """
<!DOCTYPE html>
<html>
<head>
    <title>AGV 무선 원격 제어</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <style>
        body { text-align: center; margin-top: 30px; font-family: sans-serif; background-color: #2c3e50; color: white; }
        .btn { width: 80px; height: 80px; font-size: 30px; margin: 10px; border-radius: 15px; background-color: #3498db; color: white; border: none; font-weight: bold; }
        .btn:active { background-color: #e74c3c; } /* 버튼을 누르면 빨간색으로 변경 */
        .btn-stop { background-color: #95a5a6; }
        table { margin: 0 auto; }
    </style>
    <script>
        // 서버로 이동 명령을 몰래 보내는 함수
        function sendCmd(cmd) {
            fetch('/move/' + cmd);
        }
    </script>
</head>
<body>
    <h2>🚀 AGV Remote Control</h2>
    <p>버튼을 누르고 있는 동안만 이동합니다.</p>
    
    <!-- 십자 모양 방향키 배열 -->
    <table>
        <tr>
            <td></td>
            <td><button class="btn" 
                onmousedown="sendCmd('forward')" onmouseup="sendCmd('stop')"
                ontouchstart="sendCmd('forward')" ontouchend="sendCmd('stop')">▲</button></td>
            <td></td>
        </tr>
        <tr>
            <td><button class="btn" 
                onmousedown="sendCmd('left')" onmouseup="sendCmd('stop')"
                ontouchstart="sendCmd('left')" ontouchend="sendCmd('stop')">◀</button></td>
            <td><button class="btn btn-stop" onclick="sendCmd('stop')">■</button></td>
            <td><button class="btn" 
                onmousedown="sendCmd('right')" onmouseup="sendCmd('stop')"
                ontouchstart="sendCmd('right')" ontouchend="sendCmd('stop')">▶</button></td>
        </tr>
        <tr>
            <td></td>
            <td><button class="btn" 
                onmousedown="sendCmd('backward')" onmouseup="sendCmd('stop')"
                ontouchstart="sendCmd('backward')" ontouchend="sendCmd('stop')">▼</button></td>
            <td></td>
        </tr>
    </table>
</body>
</html>
"""

# 4. 웹 페이지 접속 라우팅
@app.route('/')
def index():
    return render_template_string(HTML_JOYSTICK)

# 5. 모터 제어 신호 수신 라우팅 (URL의 <direction> 부분을 변수로 받음)
@app.route('/move/<direction>')
def move_agv(direction):
    if direction == 'forward':
        agv_forward()
    elif direction == 'backward':
        agv_backward()
    elif direction == 'left':
        agv_left()
    elif direction == 'right':
        agv_right()
    elif direction == 'stop':
        agv_stop()
        
    return "OK" # 정상 처리됨을 브라우저에 알림

# 6. 서버 가동
if __name__ == '__main__':
    print("=============================================")
    print(" 🎮 AGV 원격 제어 서버가 가동되었습니다.")
    print(" 스마트폰 주소창에 아래 주소를 입력하세요.")
    print(" 👉 http://자신의IP주소:5000")
    print("=============================================")
    app.run(host='0.0.0.0', port=5000)