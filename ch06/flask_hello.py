# file name : flask_hello.py
# Flask 웹 서버 구동 기초 테스트

from flask import Flask

# 1. Flask 서버 객체 생성 (우리의 공장 웹 서버)
app = Flask(__name__)

# 2. 라우팅(Routing) 설정 : 접속할 주소와 화면 연결
# 사용자가 웹 브라우저 주소창에 아무것도 안 붙이고 기본 주소('/')로 접속했을 때 실행될 함수
@app.route('/')
def home():
    # 웹 브라우저 화면에 띄워줄 글자(HTML)를 반환합니다.
    return "<h1>Hello, Smart Factory!</h1><p>이 화면이 보인다면 서버 접속 성공입니다.</p>"

# 3. 서버 구동
if __name__ == '__main__':
    print("스마트 팩토리 웹 서버를 시작합니다...")
    # host='0.0.0.0' : 외부(스마트폰 등)의 접속을 허용하겠다는 마법의 옵션
    # port=5000 : Flask의 기본 접속 포트(출입문 번호)
    app.run(host='0.0.0.0', port=5000)