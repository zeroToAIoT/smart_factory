# file name : MotionSensor_led_2.py
# 동작 감지 센서 값에 따라 LED on/off
# 작업자 동작 감시시 LED on, 작업자 미동작시 LED off

from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(25)
red_led = LED(17)
green_led = LED(27)

red_led.off()
green_led.on()

def motion_detected():
    red_led.on()
    green_led.off()
    print('움직임 감지: red_led ON, green_led OFF')
    
def no_motion_detected():
    red_led.off()
    green_led.on()
    print('움직임 감지 안됨: red_led OFF, green_led ON')

print('Press Ctrl+C to exit')
print('-'*30)

pir.when_motion = motion_detected
pir.when_no_motion = no_motion_detected

pause()