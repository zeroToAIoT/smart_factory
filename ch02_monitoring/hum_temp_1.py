# file: hum_temp_1.py
# 온도, 습도 측정

import board, adafruit_dht
from time import sleep

dht = adafruit_dht.DHT11(board.D21, use_pulseio=False)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    temp = dht.temperature
    print(f'Temperature: {temp:.1f}C')

    hum = dht.humidity
    print(f'Humidity: {hum:.1f}%')
    
    print(f'Temperature : {temp:.1f}C, Humidity : {hum:.1f}%')
    print('-'*30)

    sleep(2)