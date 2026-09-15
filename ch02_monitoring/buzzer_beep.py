# file name: buzzer_beep.py
# 능동 부저 경고음 발생 프로그램

from gpiozero import Buzzer
from time import sleep

bz = Buzzer(13)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    bz.on()
    sleep(1)
    bz.off()
    sleep(1)

    bz.beep(on_time=0.3, off_time=0.2)
    sleep(1)