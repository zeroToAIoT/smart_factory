# file name: led_button_buzzer.py
# LED, 버튼, 버저 테스트 프로그램

from gpiozero import LED, Button, Buzzer
from signal import pause

# LED 핀 번호 설정
ledRed = LED(17)
ledGreen = LED(27)

# 버튼 핀 번호 설정
btnRed = Button(23, bounce_time=0.05)
btnGreen = Button(24, bounce_time=0.05)

# 부저 핀 번호 설정
bz = Buzzer(13)

print('Press Ctrl+C to exit')
print('-'*30)

def btnRed_pressed():
    print('Red button pressed')
    ledRed.on()
    ledGreen.off()
    bz.beep(on_time=0.3, off_time=0.2, n=None)
   
def btnGreen_pressed():
    print('Green button pressed')
    ledGreen.on()
    bz.off()
    ledRed.off()

btnRed.when_pressed = btnRed_pressed
btnGreen.when_pressed = btnGreen_pressed

print('Press Ctrl+C to exit')
print('-'*30)

pause()
