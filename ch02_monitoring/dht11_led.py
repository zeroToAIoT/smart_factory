# file: dht11_led.py
# 스마트 팩토리 환경 모니터링 시스템

import board, adafruit_dht
from time import sleep
from gpiozero import LED

# 1. 객체 생성
dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)
red_led = LED(17)
green_led = LED(27)

def check_temperature(temp):
    if temp is not None:
        if temp >= 28:
            print(f'Temperature: {temp:.1f}C, [경고] 온도가 너무 높습니다.')
            return False
        elif temp <= 20:
            print(f'Temperature: {temp:.1f}C, [경고] 온도가 너무 낮습니다.')
            return False
        else:
            print(f'Temperature: {temp:.1f}C, [정상] 최적 온도입니다.')
            return True
    else:
        print('온도 데이터가 없습니다.')
        return False

def check_humidity(hum):
    if hum is not None:
        if hum >= 60:
            print(f'Humidity: {hum:.1f}%, [경고] 습도가 너무 높습니다.')
            return False
        elif hum <= 40:
            print(f'Humidity: {hum:.1f}%, [경고] 습도가 너무 낮습니다.')
            return False
        else:
            print(f'Humidity: {hum:.1f}%, [정상] 최적 습도입니다.')
            return True
    else:
        print('습도 데이터가 없습니다.')
        return False

print('스마트 팩토리 환경 모니터링 시작 (Press Ctrl+C to exit)')
print('-'*30)

try:
    while True:
        try:
            temp = dht.temperature
            hum = dht.humidity

            temp_ok = check_temperature(temp)
            hum_ok = check_humidity(hum)

            if temp_ok and hum_ok:
                green_led.on()
                red_led.off()
            else:
                green_led.off()
                red_led.on()

        except RuntimeError as error:
            print(f"센서 읽기 오류 (재시도 중): {error.args[0]}")
            
        print('-'*30)
        sleep(2)

except KeyboardInterrupt:
    print("\n프로그램을 사용자가 강제 종료했습니다.")

finally:
    print('센서 종료')
    dht.exit()