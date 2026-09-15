# file name : DistanceSensor_led.py
# 거리 센서 값에 따라 LED on/off
# 거리 센서 값이 0.3m 이하일 때 red_led on, green_led off
# 거리 센서 값이 0.3m 초과일 때 red_led off, green_led on

from gpiozero import DistanceSensor, LED
from signal import pause

red_led = LED(17)
green_led = LED(27)
ultra = DistanceSensor(24, 23, max_distance=2.0, threshold_distance=0.3)

red_led.off()
green_led.off()

def object_detected():
    print('Object detected')
    print(f'Distance: {ultra.distance:.3f} m')
    red_led.on()
    green_led.off()

def object_not_detected():
    print('Object not detected')
    print(f'Distance: {ultra.distance:.3f} m')
    red_led.off()
    green_led.on()

print('Press Ctrl+C to exit')
print('-'*30)

ultra.when_in_range = object_detected
ultra.when_out_of_range = object_not_detected

pause()