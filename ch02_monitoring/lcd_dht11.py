# file: lcd_dht11.py
# 온도 센서 DHT11 모듈을 사용하여 온도와 습도를 측정하고 LCD 화면에 출력하는 프로그램

import board, adafruit_dht
from RPLCD.i2c import CharLCD
from time import sleep

# 1. 객체 생성
dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)

lcd = CharLCD(i2c_expander='PCF8574', 
              address=0x27, 
              port=1,
              cols=16, 
              rows=2,
              charmap='A00')

# 2. 초기화
lcd.clear()
lcd.backlight_enabled = True

print('Press Ctrl+C to exit')
print('-'*30)

try:
    while True:
        # 3. DHT 센서 특유의 읽기 에러로 인한 프로그램 강제 종료 방지
        try:
            temp = dht.temperature
            hum = dht.humidity
            
            if hum is not None and temp is not None:
                # 4. lcd.clear() 대신 뒤에 공백을 주어 글자를 덮어씌움 (깜빡임 방지)
                # \xDF는 LCD에 출력되는 온도(°) 기호입니다.
                lcd.cursor_pos = (0, 0)
                lcd.write_string(f'Temp : {temp:.1f} \xDFC   ')
                lcd.cursor_pos = (1, 0)
                lcd.write_string(f'Hum  : {hum:.1f} %   ')
                
                print(f'Temperature : {temp:.1f}C, Humidity : {hum:.1f}%')
                print('-'*30)
            else:
                lcd.cursor_pos = (0, 0)
                lcd.write_string('Sensor Error    ')
                lcd.cursor_pos = (1, 0)
                lcd.write_string('Retrying...     ')
                print('Failed to read sensor data.')
                
        except RuntimeError as error:
            # 에러가 발생해도 멈추지 않고 2초 대기 후 다시 측정
            print(error.args[0])
            
        sleep(2)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")

finally:
    # 5. 종료 시 화면 지우고 센서 핀 자원 반환
    lcd.clear()
    lcd.backlight_enabled = False
    dht.exit()