# file: Potentiometer_led.py
# 가변 저항 값에 따라 LED 밝기 조절

from gpiozero import MCP3008, PWMLED
from time import sleep

mcp = MCP3008(channel=1)
led = PWMLED(17)

print('Press Ctrl+C to exit')
print('-'*30)

while True:
    print(f'mcp value : {mcp.value :.3f}')
    led.value = mcp.value

    sleep(0.1)