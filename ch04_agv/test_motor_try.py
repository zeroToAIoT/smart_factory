# file name: test_motor.py

from gpiozero import Motor

motor1 = Motor(26, 19)
motor2 = Motor(22, 27)
motor3 = Motor(20, 21)
motor4 = Motor(24, 23)

print('Press Ctrl+C to stop')
print('-'*30)

try:
    while True:
        print('Motor 1,2,3,4 Forward', end='\r')
        motor1.forward()
        motor2.forward()
        motor3.forward()
        motor4.forward()
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
