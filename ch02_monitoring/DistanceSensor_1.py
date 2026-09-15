# file name : DistanceSensor_1.py
# 거리 센서 값 출력

from gpiozero import DistanceSensor
from time import sleep

#ultra = DistanceSensor(echo=24, trigger=23)
ultra = DistanceSensor(24, 23)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    print(f'Distance : {ultra.distance :.3f} m')

    sleep(1)