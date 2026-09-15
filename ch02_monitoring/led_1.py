# file name : led_1.py
# 두 개의 LED 점등 프로그램

from gpiozero import LED
from time import sleep

led1 = LED(17)
led2 = LED(27)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    led1.on()
    led2.on()
    sleep(1)
    
    led1.off()
    led2.off()
    sleep(1)