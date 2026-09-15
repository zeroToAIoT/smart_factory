# file name : flask_dht.py
# Flask 웹 서버와 DHT11 온습도 센서 연동 대시보드

from flask import Flask, render_template_string, jsonify
import adafruit_dht
import board

# 1. Flask 서버 및 DHT11 센서 초기화
app = Flask(__name__)
# 라즈베리파이 4/5 호환을 위해 use_pulseio=False 옵션 사용 (GPIO 21번)
dht_device = adafruit_dht.DHT11(board.D21, use_pulseio=False)

# 2. 대시보드 화면(HTML/CSS/JS) 디자인
# 화면의 틀을 잡고, 1초마다 '/api/sensor' 주소에 몰래 접속해 데이터를 받아옵니다.
HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>환경 모니터링 대시보드</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; background-color: #2c3e50; color: white; text-align: center; padding-top: 50px; }
        .card { background-color: #34495e; margin: 20px auto; padding: 30px; border-radius: 15px; width: 80%; max-width: 400px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        .value { font-size: 40px; font-weight: bold; color: #f1c40f; margin: 10px 0; }
        .label { font-size: 18px; color: #bdc3c7; }
    </style>
    <script>
        // 1초(1000ms)마다 데이터를 새로고침 없이 가져오는 마법의 코드
        setInterval(function() {
            fetch('/api/sensor')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temp_value').innerText = data.temperature + " °C";
                    document.getElementById('humid_value').innerText = data.humidity + " %";
                })
                .catch(error => console.log("데이터 수신 에러"));
        }, 1000);
    </script>
</head>
<body>
    <h2>🏭 실시간 공장 환경 관제</h2>
    
    <div class="card">
        <div class="label">현재 온도 (Temperature)</div>
        <div class="value" id="temp_value">로딩 중...</div>
    </div>
    
    <div class="card">
        <div class="label">현재 습도 (Humidity)</div>
        <div class="value" id="humid_value">로딩 중...</div>
    </div>
</body>
</html>
"""

# 3. 라우팅 1 : 스마트폰으로 최초 접속 시 HTML 화면(껍데기)을 띄워줌
@app.route('/')
def index():
    return render_template_string(HTML_DASHBOARD)

# 4. 라우팅 2 : 자바스크립트(fetch)가 1초마다 몰래 데이터를 요청하는 주소
@app.route('/api/sensor')
def get_sensor_data():
    try:
        # 센서에서 데이터 읽기
        t = dht_device.temperature
        h = dht_device.humidity
        
        # 정상적으로 읽혔다면 JSON(딕셔너리) 형태로 변환하여 스마트폰으로 전송
        if t is not None and h is not None:
            return jsonify({"temperature": t, "humidity": h})
        else:
            return jsonify({"temperature": "오류", "humidity": "오류"})
            
    except RuntimeError as e:
        # DHT 센서는 타이밍 문제로 읽기 에러가 잦음. 에러 시 서버가 죽지 않도록 예외 처리
        return jsonify({"temperature": "측정중..", "humidity": "측정중.."})

# 5. 서버 구동
if __name__ == '__main__':
    print("=============================================")
    print(" 📊 환경 모니터링 대시보드가 가동되었습니다.")
    print(" 스마트폰 웹 브라우저 접속 주소 : http://자신의IP주소:5000")
    print("=============================================")
    app.run(host='0.0.0.0', port=5000)