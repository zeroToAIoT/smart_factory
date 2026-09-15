# file: Potentiometer_led.py
# 회전 저항 값에 따라 LED 밝기 조절

from gpiozero import MCP3008, PWMLED
from signal import pause

mcp = MCP3008(channel=1)
led = PWMLED(17)

print('Press Ctrl+C to exit')
print('-'*30)

led.source = mcp

pause()