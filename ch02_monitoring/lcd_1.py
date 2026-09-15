# file name : lcd_1.py
# LCD 표시

from RPLCD.i2c import CharLCD
from signal import pause

# 1. I2C 설정 및 초기화
lcd = CharLCD(i2c_expander='PCF8574',
              address=0x27,
              port=1,
              cols=16,
              rows=2,
              charmap='A00')

lcd.clear()
lcd.backlight_enabled = True

# 2. LCD 화면에 텍스트 출력
lcd.cursor_pos = (0, 0)
lcd.write_string('Zero To AI !!')

lcd.cursor_pos = (1, 0)
lcd.write_string('Physical AI !!')

print('LCD 출력 완료. (Press Ctrl+C to exit)')
print('-'*30)

# 3. 프로그램 대기 (글자가 계속 떠 있도록 유지)
pause()