# file name : button_1.py
# 2개 버튼 눌렀를 때 메시지 출력

from gpiozero import Button
from signal import pause

btn1 = Button(23, bounce_time=0.1)
btn2 = Button(24, bounce_time=0.1)

def btn1_pressed():
    print('Button 1 was pressed')

def btn2_pressed():
    print('Button 2 was pressed')

print('Press Ctrl+C to exit')
print('-'*30)

btn1.when_pressed = btn1_pressed
btn2.when_pressed = btn2_pressed

pause()