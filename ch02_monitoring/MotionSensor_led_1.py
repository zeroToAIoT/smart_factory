# file: MotionSensor_led.py
# 동작 감지 센서 값에 따라 LED on/off
# 작업자 동작 감시시 LED on, 작업자 미동작시 LED off

from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(25)
led = LED(17)

print('Press Ctrl+C to exit')
print('-'*30)

pir.when_motion = led.on
pir.when_no_motion = led.off

pause()