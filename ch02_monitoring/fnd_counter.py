# file name : fnd_counter.py
# FND 카운터 프로그램
# 버튼을 누를 때마다 카운트가 올라갑니다.
# 카운터가 9를 넘으면 0으로 초기화합니다.

from gpiozero import Button, LEDCharDisplay
from signal import pause

display = LEDCharDisplay(20, 21, 19, 13, 6, 16, 12, dp=26)
btn_plus = Button(23)

count = 0
display.value = str(count)

print("스마트 팩토리 불량품 카운터 가동 (Press Ctrl+C to exit)")
print("버튼을 누를 때마다 카운트가 올라갑니다.")
print('-'*30)

def add_count():
    global count
    count = count + 1

    # 카운터가 9을 넘으면 0으로 초기화
    if count > 9:
        count = 0
        print('카운터가 9를 넘었습니다. 0으로 초기화합니다.')

    # FND 표시
    display.value = str(count)
    print(f'불량품 카운트: {count}')

btn_plus.when_pressed = add_count

pause()