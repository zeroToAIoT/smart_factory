# file: MotionSensor_3.py

from gpiozero import MotionSensor, LED
from signal import pause

pir = MotionSensor(25)
led = LED(17)

print('스마트 창고 자동 조명 시스템 가동 중... (Press Ctrl+C to exit)')
print('센서 앞에서 손을 흔들어 보세요!')
print('-'*30)

# 센서에 움직임이 감지되면 LED를 켜고, 움직임이 감지되지 않으면 LED를 끈다.
pir.when_motion = led.on
pir.when_no_motion = led.off

pause()