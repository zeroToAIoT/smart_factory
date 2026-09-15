# file name : fnd_3.py
# 0부터 9까지 표시

from gpiozero import LEDCharDisplay
from time import sleep

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    for i in range(10):
        display.value = str(i)
        print(f'Display: {i}')
        sleep(1)