# file name : water_led.py
# 물 수위 센서 값에 따라 LED 밝기 조절

from gpiozero import MCP3008, LED
from time import sleep

# MCP3008 채널 4에 연결된 물 수위 센서
mcp = MCP3008(channel=4)

# GPIO 17번에 연결된 경고용 LED
led = LED(17)

print('냉각수 수위 모니터링 시작... Press Ctrl+C to exit')
print('-'*30)

while True:
    value = mcp.value
    print(f'현재 수위(비율) : {value:.3f}')
    
    # 수위 센서 값이 10% 미만이면 LED 켜기
    if value < 0.1:
        led.on()
    else:
        led.off()
        
    sleep(0.5)
