# file name : fnd_1.py
# FND 표시

from gpiozero import LEDCharDisplay
from signal import pause

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
#display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26, active_high=False)

print('Press Ctrl+C to exit')
print('-'*30)

display.source_delay = 1
display.source ='8FAH'

pause()