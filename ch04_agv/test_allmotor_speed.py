# file name : test_allmotor_speed.py
# Test All Motor Forward with Speed Control

from gpiozero import Motor
from time import sleep

motor1 = Motor(26, 19)
motor2 = Motor(20, 21)
motor3 = Motor(22, 27)
motor4 = Motor(24, 23)

print('Press Ctrl+C to stopped')
print('-'*30)

try:
    speed = 0.0
    step = 0.1
    is_increasing = True

    while True:
        print(f'Motor Forwarding. speed : {speed:.1f}', end='\r')
        motor1.forward(speed=speed)
        motor2.forward(speed=speed)
        motor3.forward(speed=speed)
        motor4.forward(speed=speed)

        if is_increasing:
            speed = round(speed + step, 1)

            if speed >= 1.0:
                is_increasing = False
        else:
            speed = round(speed - step, 1)
            if speed <= 0.0:
                is_increasing = True

        sleep(2)

except KeyboardInterrupt:
    print('Stopped. ctrl+c pressed.')
except Exception as err:
    print(f'Error : {err}')
finally:
    print('Motor stopped')
    motor1.stop()
    motor2.stop()
    motor3.stop()
    motor4.stop()